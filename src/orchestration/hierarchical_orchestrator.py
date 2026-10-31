"""Hierarchical Manager MAS Orchestrator coordinating CrewAI and Google ADK."""
import time
import concurrent.futures
from typing import Dict, Any, Optional
from ..schemas.blackboard import BlackboardState, CandidateDriver, RetrievedRule
from ..schemas.reports import FinalDeliveryReport
from ..schemas.decisions import GuardrailEvaluation, RoutePlan
from ..schemas.a2a import A2ARequest
from ..guardrails.input_guard import InputGuard
from ..guardrails.business_guardrails import BusinessGuardrails
from ..guardrails.tool_validator import ToolValidator
from ..mcp.tools.driver_db import DriverDBTool
from ..mcp.tools.delay_predictor import DelayPredictorTool
from ..agents.crew_retrieval_agent import CrewRetrievalAgent
from ..agents.crew_dispatch_agent import CrewDispatchAgent
from ..agents.crew_exception_agent import CrewExceptionAgent
from ..agents.adk_route_agent import ADKRouteAgent
from ..agents.a2a_bridge import A2ABridge
from .blackboard_manager import BlackboardManager
from ..observability.run_logger import RunLogger
from ..observability.tracing import MASTracer

class HierarchicalOrchestrator:
    """Supervisory Orchestrator directing MAS workflow through Blackboard state and A2A messages."""

    def __init__(self):
        self.bb_manager = BlackboardManager()
        self.input_guard = InputGuard()
        self.business_guardrails = BusinessGuardrails()
        self.tool_validator = ToolValidator()
        self.driver_db = DriverDBTool()
        self.delay_predictor = DelayPredictorTool()
        
        # Agents across CrewAI and Google ADK
        self.adk_route_agent = ADKRouteAgent()
        self.a2a_bridge = A2ABridge(adk_route_agent=self.adk_route_agent)
        self.retrieval_agent = CrewRetrievalAgent()
        self.dispatch_agent = CrewDispatchAgent(a2a_bridge=self.a2a_bridge, delay_predictor=self.delay_predictor)
        self.exception_agent = CrewExceptionAgent(a2a_bridge=self.a2a_bridge)

        self.logger = RunLogger.get_logger()
        self.tracer = MASTracer()

    def process_order(
        self,
        order: Dict[str, Any],
        prompt_style: str = "ReAct",
        simulate_exception: bool = False,
        run_id: str = "run-0"
    ) -> FinalDeliveryReport:
        """Execute complete multi-agent delivery workflow for an incoming consignment."""
        start_overall = time.time()

        # Step -1: Pre-Execution Order Payload Validation
        is_order_valid, order_errors = self.tool_validator.validate_order_data(order)
        order_id = str(order.get("order_id", "INVALID-ORD"))
        if not is_order_valid:
            total_time = round(time.time() - start_overall, 4)
            return FinalDeliveryReport(
                order_id=order_id,
                priority=str(order.get("priority", "NORMAL")),
                customer_persona=str(order.get("persona", "polite")),
                input_guard_status="INVALID_ORDER_SPECIFICATION",
                assigned_driver_id="NONE",
                assigned_driver_name="NONE",
                selected_route="NONE",
                distance_km=0.0,
                final_eta_mins=0.0,
                predicted_delay_mins=0.0,
                delivery_outcome="INVALID_ORDER_SPECIFICATION",
                total_execution_latency_sec=total_time,
                total_tokens_consumed=50,
                estimated_cost_usd=0.000005,
                guardrail_summary=GuardrailEvaluation(
                    passed=False,
                    violations=order_errors,
                    action_taken="BLOCK",
                    interventions=len(order_errors)
                )
            )

        trace_id = self.tracer.start_trace(order_id)

        # Step 0: Input Guard Screening (Span 1)
        span_guard = self.tracer.start_span(trace_id, "InputSecurityScreening", "InputGuard")
        raw_notes = str(order.get("notes") or "")
        guard_res = self.input_guard.evaluate(raw_notes)

        self.tracer.end_span(span_guard, status=guard_res.status, extra_attributes={"threats": guard_res.detected_threats})

        # If malicious injection attack, refuse and terminate safely
        if guard_res.status == "BLOCKED_INJECTION":
            total_time = time.time() - start_overall
            self.logger.log_event(
                run_id=run_id,
                order_id=order_id,
                agent_name="InputGuard",
                framework="GuardrailLayer",
                event_type="GUARDRAIL_INTERCEPTION",
                start_time=start_overall,
                end_time=time.time(),
                input_tokens=100,
                output_tokens=30,
                status="BLOCKED_SECURITY",
                metadata={"threats": guard_res.detected_threats}
            )
            return FinalDeliveryReport(
                order_id=order_id,
                priority=order["priority"],
                customer_persona=order.get("persona", "injection"),
                input_guard_status=guard_res.status,
                assigned_driver_id="NONE",
                assigned_driver_name="NONE",
                selected_route="NONE",
                distance_km=0.0,
                final_eta_mins=0.0,
                predicted_delay_mins=0.0,
                delivery_outcome="BLOCKED_BY_GUARDRAIL",
                total_execution_latency_sec=round(total_time, 4),
                total_tokens_consumed=130,
                estimated_cost_usd=round((100 * 0.075 + 30 * 0.30) / 1_000_000, 6),
                guardrail_summary=GuardrailEvaluation(
                    passed=False,
                    violations=guard_res.detected_threats,
                    action_taken="BLOCK",
                    interventions=1
                )
            )

        # Step 1: Initialize Blackboard State
        bb_state = self.bb_manager.initialize_order_state(
            order_id=order_id,
            pickup=order["pickup"],
            dropoff=order["dropoff"],
            weight_kg=float(order["weight_kg"]),
            priority=order["priority"],
            deadline_mins=int(order["deadline_mins"]),
            persona=order.get("persona", "polite"),
            customer_notes=raw_notes
        )
        bb_state.masked_notes = guard_res.sanitized_text

        # Step 2: Execution Flow with Comprehensive Fault Isolation
        try:
            # Parallel Context Gathering (Span 2) - Executed concurrently via ThreadPoolExecutor
            span_gather = self.tracer.start_span(trace_id, "ParallelContextGathering", "Orchestrator")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                future_rag = executor.submit(
                    self.retrieval_agent.retrieve_rules_for_order,
                    order_id=order_id,
                    pickup_zone=order["pickup"],
                    dropoff_zone=order["dropoff"],
                    weight_kg=float(order["weight_kg"]),
                    priority=order["priority"],
                    run_id=run_id
                )
                future_drivers = executor.submit(
                    self.driver_db.find_eligible_drivers,
                    min_capacity_kg=float(order["weight_kg"])
                )
                rules = future_rag.result()
                raw_drivers = future_drivers.result()

            self.bb_manager.update_field(order_id, "crew_retrieval_agent", "retrieved_rules", rules, "Pushed RAG rules to Blackboard")

            candidates = [
                CandidateDriver(
                    driver_id=d["driver_id"],
                    name=d["name"],
                    current_zone=d["current_zone"],
                    vehicle_type=d["vehicle_type"],
                    capacity_kg=d["capacity_kg"],
                    hours_worked=d["hours_worked"],
                    rating=d["rating"],
                    status=d["status"]
                )
                for d in raw_drivers
            ]
            self.bb_manager.update_field(order_id, "DriverDBTool", "candidate_drivers", candidates, "Loaded eligible drivers into Blackboard")
            self.tracer.end_span(span_gather, status="OK")

            # Fallback if no available drivers meet payload capacity or hours
            if not candidates:
                total_time = round(time.time() - start_overall, 4)
                guard_eval = GuardrailEvaluation(
                    passed=False,
                    violations=[f"No eligible drivers found meeting capacity {float(order['weight_kg'])}kg and statutory working hour limits."],
                    action_taken="BLOCK",
                    interventions=1
                )
                self.bb_manager.update_field(order_id, "BusinessGuardrails", "guardrail_passed", False, "No drivers meeting criteria")
                self.logger.log_event(
                    run_id=run_id,
                    order_id=order_id,
                    agent_name="FleetOrchestrator",
                    framework="CrewAI",
                    event_type="DISPATCH_FAILURE",
                    start_time=start_overall,
                    end_time=time.time(),
                    input_tokens=150,
                    output_tokens=40,
                    status="NO_ELIGIBLE_DRIVERS",
                    metadata={"order_id": order_id, "weight_kg": float(order["weight_kg"])}
                )
                return FinalDeliveryReport(
                    order_id=order_id,
                    priority=order["priority"],
                    customer_persona=order.get("persona", "polite"),
                    input_guard_status=guard_res.status,
                    assigned_driver_id="NONE",
                    assigned_driver_name="NONE",
                    selected_route="NONE",
                    distance_km=0.0,
                    final_eta_mins=0.0,
                    predicted_delay_mins=0.0,
                    delivery_outcome="UNASSIGNED_NO_ELIGIBLE_DRIVER",
                    total_execution_latency_sec=total_time,
                    total_tokens_consumed=190,
                    estimated_cost_usd=0.00002,
                    guardrail_summary=guard_eval,
                    provenance_trail=bb_state.provenance_log
                )

            # Step 3: Dispatch Agent Reasoning over Blackboard (Span 3)
            span_dispatch = self.tracer.start_span(trace_id, "DispatchReasoning", "CrewDispatchAgent")
            dispatch_dec = self.dispatch_agent.decide_assignment(
                order_id=order_id,
                pickup=order["pickup"],
                dropoff=order["dropoff"],
                weight_kg=float(order["weight_kg"]),
                priority=order["priority"],
                deadline_mins=int(order["deadline_mins"]),
                candidate_drivers=candidates,
                prompt_style=prompt_style,
                run_id=run_id
            )
            self.bb_manager.update_field(order_id, "crew_dispatch_agent", "assigned_driver_id", dispatch_dec.assigned_driver_id, "Committed driver assignment")
            self.bb_manager.update_field(order_id, "crew_dispatch_agent", "dispatch_rationale", dispatch_dec.rationale, "Logged dispatch rationale")
            self.bb_manager.update_field(order_id, "crew_dispatch_agent", "predicted_delay_mins", dispatch_dec.predicted_delay_mins, "Logged delay prediction")
            self.tracer.end_span(span_dispatch, status="OK")

            # Step 4: Route Generation via Google ADK Route Agent over A2A (Span 4)
            span_route = self.tracer.start_span(trace_id, "ADKRouteCalculation", "ADKRouteAgent")
            a2a_req = A2ARequest(
                order_id=order_id,
                driver_id=dispatch_dec.assigned_driver_id,
                pickup_zone=order["pickup"],
                dropoff_zone=order["dropoff"],
                priority=order["priority"]
            )
            route_plan = self.adk_route_agent.generate_route_plan(a2a_req, run_id=run_id)
            self.bb_manager.update_field(order_id, "adk_route_agent", "selected_route", route_plan.selected_route, "Committed transit route")
            self.bb_manager.update_field(order_id, "adk_route_agent", "distance_km", route_plan.distance_km, "Recorded distance")
            self.bb_manager.update_field(order_id, "adk_route_agent", "estimated_eta_mins", route_plan.estimated_eta_mins, "Recorded congestion ETA")
            self.tracer.end_span(span_route, status="OK")

            # Step 5: Business Guardrail Evaluation (Span 5)
            span_biz = self.tracer.start_span(trace_id, "BusinessRuleValidation", "BusinessGuardrails")
            chosen_driver_record = self.driver_db.get_driver_by_id(dispatch_dec.assigned_driver_id) or {}
            guard_eval = self.business_guardrails.evaluate_dispatch(
                driver=chosen_driver_record,
                order_weight_kg=float(order["weight_kg"]),
                dropoff_location=order["dropoff"],
                estimated_eta_mins=route_plan.estimated_eta_mins
            )
            self.bb_manager.update_field(order_id, "BusinessGuardrails", "guardrail_passed", guard_eval.passed, "Evaluated compliance")
            self.tracer.end_span(span_biz, status="OK" if guard_eval.passed else "FLAGGED")

            # Step 6: Event-Driven Exception Handling (Span 6 - conditional)
            exception_replan = None
            delivery_outcome = "SUCCESS"
            final_eta = route_plan.estimated_eta_mins
            final_route = route_plan.selected_route
            final_driver_id = dispatch_dec.assigned_driver_id
            final_driver_name = dispatch_dec.assigned_driver_name

            if simulate_exception:
                span_exc = self.tracer.start_span(trace_id, "ExceptionRecovery", "CrewExceptionAgent")
                exception_replan = self.exception_agent.recover_disruption(
                    order_id=order_id,
                    original_driver_id=dispatch_dec.assigned_driver_id,
                    disruption_cause="TRAFFIC_ACCIDENT_ROAD_BLOCKAGE",
                    pickup_zone=order["pickup"],
                    dropoff_zone=order["dropoff"],
                    deadline_mins=int(order["deadline_mins"]),
                    backup_drivers=candidates,
                    run_id=run_id
                )
                final_route = exception_replan.new_route
                final_eta = exception_replan.new_eta_mins
                final_driver_id = exception_replan.reassigned_driver_id
                
                if exception_replan.recovery_action == "ESCALATE_DISPATCH_SUPERVISOR":
                    delivery_outcome = "ESCALATED_SUPERVISOR_FATIGUE"
                    final_driver_name = "NONE (Supervisor Escalation)"
                    guard_eval = GuardrailEvaluation(
                        passed=False,
                        violations=["All candidate and backup drivers exceed statutory 9.0h fatigue limit."],
                        action_taken="BLOCK",
                        interventions=1
                    )
                    self.bb_manager.update_field(order_id, "crew_exception_agent", "exception_triggered", True, "Triggered supervisor fatigue escalation")
                    self.tracer.end_span(span_exc, status="ESCALATED")
                else:
                    reassigned_driver = self.driver_db.get_driver_by_id(final_driver_id)
                    if reassigned_driver:
                        final_driver_name = reassigned_driver["name"]
                        # Re-verify business guardrails on reassigned driver
                        reassigned_guard = self.business_guardrails.evaluate_dispatch(
                            driver=reassigned_driver,
                            order_weight_kg=float(order["weight_kg"]),
                            dropoff_location=order["dropoff"],
                            estimated_eta_mins=final_eta
                        )
                        guard_eval = reassigned_guard
                    delivery_outcome = "RECOVERED_VIA_EXCEPTION"
                    self.bb_manager.update_field(order_id, "crew_exception_agent", "exception_triggered", True, "Activated exception replan")
                    self.bb_manager.update_field(order_id, "crew_exception_agent", "replan_driver_id", final_driver_id, "Reassigned driver")
                    self.tracer.end_span(span_exc, status="RECOVERED")

            total_latency = round(time.time() - start_overall, 4)
            total_tokens = 740 if not simulate_exception else 1045
            cost = round((total_tokens * 0.75 * 0.075 + total_tokens * 0.25 * 0.30) / 1_000_000, 6)

            return FinalDeliveryReport(
                order_id=order_id,
                priority=order["priority"],
                customer_persona=order.get("persona", "polite"),
                input_guard_status=guard_res.status,
                assigned_driver_id=final_driver_id,
                assigned_driver_name=final_driver_name,
                selected_route=final_route,
                distance_km=route_plan.distance_km,
                final_eta_mins=final_eta,
                predicted_delay_mins=dispatch_dec.predicted_delay_mins,
                delivery_outcome=delivery_outcome,
                total_execution_latency_sec=total_latency,
                total_tokens_consumed=total_tokens,
                estimated_cost_usd=cost,
                guardrail_summary=guard_eval,
                exception_details=exception_replan,
                provenance_trail=bb_state.provenance_log
            )
        except Exception as exc:
            total_time = round(time.time() - start_overall, 4)
            self.logger.log_event(
                run_id=run_id,
                order_id=order_id,
                agent_name="FleetOrchestrator",
                framework="CrewAI",
                event_type="SYSTEM_FAULT",
                start_time=start_overall,
                end_time=time.time(),
                input_tokens=100,
                output_tokens=30,
                status="ERROR",
                error_message=str(exc)
            )
            bb_rec = self.bb_manager.get_state(order_id)
            return FinalDeliveryReport(
                order_id=order_id,
                priority=str(order.get("priority", "NORMAL")),
                customer_persona=str(order.get("persona", "polite")),
                input_guard_status="ERROR_SYSTEM_FAULT",
                assigned_driver_id="NONE",
                assigned_driver_name="NONE",
                selected_route="NONE",
                distance_km=0.0,
                final_eta_mins=0.0,
                predicted_delay_mins=0.0,
                delivery_outcome="SYSTEM_FAULT_RECOVERED",
                total_execution_latency_sec=total_time,
                total_tokens_consumed=100,
                estimated_cost_usd=0.00001,
                guardrail_summary=GuardrailEvaluation(
                    passed=False,
                    violations=[f"Runtime fault intercepted: {str(exc)}"],
                    action_taken="BLOCK",
                    interventions=1
                ),
                provenance_trail=bb_rec.provenance_log if bb_rec else []
            )
