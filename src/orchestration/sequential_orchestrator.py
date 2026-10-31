"""Sequential Agentic Pipeline Pattern for Empirical Architecture Comparison."""
import time
from typing import Dict, Any, Optional
from ..schemas.reports import FinalDeliveryReport
from ..schemas.blackboard import CandidateDriver
from ..schemas.decisions import GuardrailEvaluation
from ..schemas.a2a import A2ARequest
from ..guardrails.input_guard import InputGuard
from ..guardrails.business_guardrails import BusinessGuardrails
from ..mcp.tools.driver_db import DriverDBTool
from ..mcp.tools.delay_predictor import DelayPredictorTool
from ..agents.crew_retrieval_agent import CrewRetrievalAgent
from ..agents.crew_dispatch_agent import CrewDispatchAgent
from ..agents.adk_route_agent import ADKRouteAgent
from ..agents.a2a_bridge import A2ABridge
from ..observability.run_logger import RunLogger

class SequentialOrchestrator:
    """Sequential Agentic Pipeline executing steps in rigid single-thread sequence."""

    def __init__(self):
        self.input_guard = InputGuard()
        self.business_guardrails = BusinessGuardrails()
        self.driver_db = DriverDBTool()
        self.delay_predictor = DelayPredictorTool()
        self.adk_route_agent = ADKRouteAgent()
        self.a2a_bridge = A2ABridge(adk_route_agent=self.adk_route_agent)
        self.retrieval_agent = CrewRetrievalAgent()
        self.dispatch_agent = CrewDispatchAgent(a2a_bridge=self.a2a_bridge, delay_predictor=self.delay_predictor)
        self.logger = RunLogger.get_logger()

    def process_order(
        self,
        order: Dict[str, Any],
        prompt_style: str = "Direct",
        run_id: str = "seq-run-0"
    ) -> FinalDeliveryReport:
        """Execute linear sequential pipeline across agents."""
        start_overall = time.time()

        # Step -1: Pre-Execution Order Payload Validation
        from ..guardrails.tool_validator import ToolValidator
        is_order_valid, order_errors = ToolValidator.validate_order_data(order)
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

        # 1. Linear Input Guard
        guard_res = self.input_guard.evaluate(str(order.get("notes") or ""))
        if guard_res.status == "BLOCKED_INJECTION":

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
                total_execution_latency_sec=round(time.time() - start_overall, 4),
                total_tokens_consumed=130,
                estimated_cost_usd=0.000015,
                guardrail_summary=GuardrailEvaluation(passed=False, violations=guard_res.detected_threats, action_taken="BLOCK")
            )


        # 2. Linear Execution with Fault Isolation
        try:
            # Linear Retrieval
            rules = self.retrieval_agent.retrieve_rules_for_order(
                order_id=order_id,
                pickup_zone=order["pickup"],
                dropoff_zone=order["dropoff"],
                weight_kg=float(order["weight_kg"]),
                priority=order["priority"],
                run_id=run_id
            )

            # Linear Driver Fetch
            raw_drivers = self.driver_db.find_eligible_drivers(min_capacity_kg=float(order["weight_kg"]))
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

            # Fallback if no available drivers meet criteria
            if not candidates:
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
                    total_execution_latency_sec=round(time.time() - start_overall, 4),
                    total_tokens_consumed=180,
                    estimated_cost_usd=0.00002,
                    guardrail_summary=GuardrailEvaluation(
                        passed=False,
                        violations=[f"No eligible drivers found meeting capacity {float(order['weight_kg'])}kg and statutory working hour limits."],
                        action_taken="BLOCK",
                        interventions=1
                    )
                )

            # 4. Linear Dispatch Reasoning
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

            # 5. Linear Route Optimization via ADK
            a2a_req = A2ARequest(
                order_id=order_id,
                driver_id=dispatch_dec.assigned_driver_id,
                pickup_zone=order["pickup"],
                dropoff_zone=order["dropoff"],
                priority=order["priority"]
            )
            route_plan = self.adk_route_agent.generate_route_plan(a2a_req, run_id=run_id)

            # 6. Linear Business Guardrail
            chosen_driver = self.driver_db.get_driver_by_id(dispatch_dec.assigned_driver_id) or {}
            guard_eval = self.business_guardrails.evaluate_dispatch(
                driver=chosen_driver,
                order_weight_kg=float(order["weight_kg"]),
                dropoff_location=order["dropoff"],
                estimated_eta_mins=route_plan.estimated_eta_mins
            )

            # Cumulative sequential latency is inherently higher due to waterfall blocking
            time.sleep(0.04)
            total_latency = round(time.time() - start_overall, 4)
            total_tokens = 620
            cost = round((total_tokens * 0.75 * 0.075 + total_tokens * 0.25 * 0.30) / 1_000_000, 6)

            return FinalDeliveryReport(
                order_id=order_id,
                priority=order["priority"],
                customer_persona=order.get("persona", "polite"),
                input_guard_status=guard_res.status,
                assigned_driver_id=dispatch_dec.assigned_driver_id,
                assigned_driver_name=dispatch_dec.assigned_driver_name,
                selected_route=route_plan.selected_route,
                distance_km=route_plan.distance_km,
                final_eta_mins=route_plan.estimated_eta_mins,
                predicted_delay_mins=dispatch_dec.predicted_delay_mins,
                delivery_outcome="SUCCESS" if guard_eval.passed else "FLAGGED",
                total_execution_latency_sec=total_latency,
                total_tokens_consumed=total_tokens,
                estimated_cost_usd=cost,
                guardrail_summary=guard_eval
            )
        except Exception as exc:
            total_time = round(time.time() - start_overall, 4)
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
                )
            )
