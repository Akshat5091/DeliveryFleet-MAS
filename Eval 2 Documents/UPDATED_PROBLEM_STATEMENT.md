# 🚚 Updated Problem Statement: Autonomous Multi-Agent Delivery Fleet Coordination & Dispatch System

**Course Code:** CSE3101 — Agentic AI  
**Academic Year:** 2026–2027 | 7th Semester B.Tech CSE  
**Group:** 8 | **Phase:** Evaluation 2 (~68% Milestone: 7 Core Criteria Verified | 4 End-Term Novelties)  
**Authors:** Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)  

---

## 1. Executive Summary & Context

Modern urban logistics networks operate under severe real-time uncertainty. Last-mile parcel delivery accounts for over **53% of overall shipping costs** and suffers from constant disruptions: sudden traffic congestion, inclement weather, municipal zero-emission zone constraints, driver fatigue regulations, and unexpected mid-transit vehicle breakdowns. 

Existing commercial dispatch platforms rely primarily on **static heuristic assignment** (e.g., greedy Euclidean nearest-neighbor algorithms) or monolithic rule engines. These conventional systems exhibit critical architectural vulnerabilities:
1. **Lack of Dynamic Contextual Reasoning:** A driver who is geometrically closest (e.g., 2 km away) may be trapped behind a major gridlock or nearing their legal 9.0-hour shift limit, rendering them suboptimal compared to a driver 4 km away on an open arterial bypass.
2. **Single-Point-of-Failure & Hallucination Risk:** Monolithic LLM prompt approaches suffer from unconstrained context bloating, non-deterministic latency, and security vulnerabilities to prompt injection.
3. **Rigid Exception Handling:** When a route is blocked or a driver is delayed, existing systems cannot autonomously negotiate dynamic recovery; they require human operator intervention, resulting in compounding delivery SLA violations.
4. **Data Privacy & Compliance Leakage:** Sensitive corporate driver shift logs and municipal zoning bylaws cannot be indiscriminately exposed to public third-party cloud APIs due to regulatory data protection laws.

To overcome these deficiencies, this project develops a **decentralized, verifiable, and secure Multi-Agent System (MAS)** that coordinates fleet dispatch, transit routing, and real-time contingency recovery. The system integrates **Google Agent Development Kit (ADK)** and **CrewAI**, leveraging **Blackboard Shared State Architecture**, **Model Context Protocol (MCP)** tool integration, and standardized **Agent-to-Agent (A2A)** messaging.

---

## 2. Operational PEAS Framing

Following the standard Russell & Norvig Multi-Agent System formalization:

| Element | Specification in Fleet Logistics System |
| :--- | :--- |
| **Performance Measures (KPMs)** | 1. **Assignment Accuracy (%):** Optimal driver selection matching capacity, deadline, and shift hours.<br>2. **SLA Delivery Success Rate (%):** Orders delivered within promised deadline.<br>3. **Mean Decision Latency (s):** Time elapsed from consignment ingestion to final route commitment.<br>4. **Driver Safety Adherence (%):** 100% compliance with statutory 9.0-hour daily driving limits.<br>5. **Dynamic Exception Recovery Rate (%):** Autonomous rerouting success without human supervisor intervention.<br>6. **Guardrail Interception Rate (%):** Defending system against toxic prompts and prompt injections. |
| **Environment** | **Partially Observable, Dynamic, Stochastic, Sequential, Multi-Agent:** Real-time traffic, fluctuating rainfall, dynamic driver shift hours, and unexpected transit accidents create continuous state drift. Simulated via high-fidelity synthetic datasets (`orders.csv`, `drivers.csv`, `traffic.csv`, `weather.csv`, `delivery_history.csv`). |
| **Actuators** | **Decisional Actions:** Dispatch commitment, primary corridor selection, speed regulation, dynamic exception reassignment, customer communication sanitization, and blackboard state write operations. (No physical mechanical actuation). |
| **Sensors / Percepts** | Ingested consignment profiles (weight, priority, deadline), live driver telemetry (GPS zone, vehicle payload capacity, cumulative hours worked), congestion speed factors from traffic sensors, weather precipitation readings, and Vector RAG policy chunks. |

---

## 3. Strict Architectural Justification: Pain Points vs. Agent Rationale

> *"Whatever number of agents you decide to use in your Agentic AI system, you must have a clear understanding of the rationale behind each one. You should be able to explain the purpose of every agent and the specific problem it is designed to address. Do not include agents randomly just to make your system appear more advanced or complex."* — Course Directive

To comply strictly with this mandate, every single agent in our system maps directly to an identifiable, non-trivial operational pain point. We categorically reject arbitrary agent proliferation.

```
OPERATIONAL PAIN POINT                                        RESOLVING AGENT IN MAS
┌───────────────────────────────────────────────┐             ┌───────────────────────────────────────────────┐
│ Pain Point 1: Multi-Factor Dispatch Conflict  │  ─────────> │ Dispatch Agent (CrewAI ReAct)                 │
│ Capacity, traffic, fatigue, and SLA deadlines │             │ Evaluates tradeoffs, queries ML delay model   │
└───────────────────────────────────────────────┘             └───────────────────────────────────────────────┘
┌───────────────────────────────────────────────┐             ┌───────────────────────────────────────────────┐
│ Pain Point 2: Dynamic Urban Route Congestion  │  ─────────> │ Route Optimization Agent (Google ADK)         │
│ Static shortest paths fail during peak traffic│             │ Uses A2A protocol & MCP Routing Tool          │
└───────────────────────────────────────────────┘             └───────────────────────────────────────────────┘
┌───────────────────────────────────────────────┐             ┌───────────────────────────────────────────────┐
│ Pain Point 3: Mid-Transit Disruption Deadlock │  ─────────> │ Exception Handling Agent (CrewAI)             │
│ Accidents/blockages cause cascading SLA failure│            │ Event-driven dynamic recovery & replanning    │
└───────────────────────────────────────────────┘             └───────────────────────────────────────────────┘
┌───────────────────────────────────────────────┐             ┌───────────────────────────────────────────────┐
│ Pain Point 4: Enterprise Policy Privacy Leak  │  ─────────> │ Retrieval Agent (Private Vector RAG)          │
│ Proprietary bylaws leaked if sent to cloud API│             │ Runs ChromaDB locally for data sovereignty    │
└───────────────────────────────────────────────┘             └───────────────────────────────────────────────┘
┌───────────────────────────────────────────────┐             ┌───────────────────────────────────────────────┐
│ Pain Point 5: Multi-Agent Race Conditions     │  ─────────> │ Fleet Orchestrator (Supervisory Manager)      │
│ State inconsistency and execution disorder    │             │ Manages Blackboard state & lifecycle gating   │
└───────────────────────────────────────────────┘             └───────────────────────────────────────────────┘
```

### Detailed Agent Justification Matrix:

### 1. Fleet Dispatch Agent (Framework: CrewAI)
- **Pain Point Addressed:** High-dimensional assignment conflict. Greedy nearest-driver algorithms pick nearby drivers who may be near legal shift limits (8.5+ hours) or stuck in severe traffic jams, resulting in missed delivery windows.
- **Why an Agent is Necessary:** Allocating orders requires reasoning under conflicting objectives (driver proximity vs. vehicle payload capacity vs. cumulative fatigue vs. customer SLA urgency). The agent uses a **ReAct (Reasoning + Acting)** loop to interleave driver database queries with Machine Learning delay predictions before committing.
- **Why a Rule Engine is Insufficient:** Rigid if-else trees cannot smoothly balance a 5-minute delay on an empty EV van against a 2-minute delay on a diesel truck facing municipal peak-hour restrictions.

### 2. Route Optimization Agent (Framework: Google ADK)
- **Pain Point Addressed:** Urban transit fragility and cross-framework interoperability. Route calculation must adapt to live speed factors and urban corridor restrictions without coupling routing logic to the dispatch framework.
- **Why an Agent is Necessary:** Built using **Google Agent Development Kit (ADK)** to establish framework diversity. It exposes an **A2A (Agent-to-Agent)** interface and interacts with the routing engine via the **Model Context Protocol (MCP)**. It dynamically evaluates primary arterial corridors against bypass options.

### 3. Exception Handling Agent (Framework: CrewAI)
- **Pain Point Addressed:** Mid-route operational disruption and deadlock. If a driver encounters an unexpected road accident or vehicle failure mid-transit, traditional dispatches fail completely.
- **Why an Agent is Necessary:** Operates on an **event-driven trigger**. When a delay-risk alert fires, the Exception Agent analyzes alternative standby drivers, queries the ADK Route Agent over A2A for emergency bypass corridors, and computes time-saved deltas without restarting the entire pipeline.

### 4. Policy & Compliance Retrieval Agent (Framework: CrewAI / Local RAG)
- **Pain Point Addressed:** Enterprise data sovereignty, privacy protection, and adherence to complex municipal bylaws (e.g., Zone B heavy freight bans after 17:00, Zone A low-emission vehicle rules).
- **Why an Agent is Necessary:** Sending proprietary driver shift logs and internal delivery contracts to external public LLM endpoints violates enterprise security policies. The Retrieval Agent queries an isolated **ChromaDB vector store** locally, grounding dispatch decisions in verified policy chunks.

### 5. Fleet Supervisory Orchestrator (Framework: CrewAI Flow / Manager)
- **Pain Point Addressed:** Multi-agent coordination overhead, race conditions, and unstructured messaging chaos.
- **Why an Agent is Necessary:** Coordinates the execution phases, initializes and maintains the **Blackboard Shared State**, supervises parallel context gathering, and enforces safety gates.

### 💡 Why Monitoring is NOT an LLM Agent (Senior Architectural Decision)
In early brainstorming, a "Monitoring Agent" was proposed. However, **we deliberately rejected an LLM for monitoring**. 
- Logging intermediate agent events, computing token counts, tracking latency, and generating provenance heatmaps is a **deterministic, zero-hallucination operational task**. 
- Wrapping an LLM around monitoring consumes unnecessary API tokens, introduces non-deterministic latency, and adds architectural bloat.
- Instead, AI Observability is implemented via **native programmatic Callbacks (CrewAI step callbacks + ADK lifecycle hooks)** and **OpenTelemetry-compatible distributed trace spans**.

---

## 4. Minimum Evaluation Criteria Mapping

This updated problem statement establishes baseline compliance across 7 completed Phase 2 core criteria and 4 Phase 3 research novelty extensions:
1. **Blackboard Architecture:** Centralized typed `BlackboardState` with provenance logging; benchmarked against direct peer A2A messaging.
2. **Tool Integration via MCP:** 5 production MCP tools (Driver DB, Routing Engine, ML Delay Forecaster, ChromaDB Vector RAG, Blackboard State Tool).
3. **Pydantic Structured Output:** Every decision validated via Pydantic v2 (`DispatchDecision`, `RoutePlan`, `ExceptionReplan`, `FinalDeliveryReport` in JSON and Markdown table).
4. **Agentic Design Patterns:** Hierarchical vs. Sequential architectures benchmarked across identical test orders.
5. **[Phase 3 Novelty] Callbacks & Heatmaps:** Longitudinal 24h telematics drift tracking, tokens, cost, and errors, generating agent-level heatmaps.
6. **A2A Protocol:** ADK Route Agent exposed via A2A; CrewAI agents communicate via typed JSON envelopes.
7. **Dual-Framework Invariant:** Strict integration of Google ADK and CrewAI.
8. **Security & Guardrails:** Multi-tier defense (Input Guard for prompt injection/abusive masking, tool return validation, business working-hour bylaws).
9. **[Phase 3 Novelty] AI Observability:** Distributed OpenTelemetry Collector export to Jaeger dashboard.
10. **[Phase 3 Novelty] Performance Evaluation:** Exhaustive 72+ run factorial optimization matrix across 3 architectures with Pareto cost-latency frontiers.
11. **[Phase 3 Novelty] Cloud Deployment:** Live cloud VM deployment (AWS/GCP) with Cloudflare edge security worker bridge.
