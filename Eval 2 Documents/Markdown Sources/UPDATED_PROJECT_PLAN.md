# Updated Project Plan: Multi-Agent Delivery Fleet Coordination System
## Progress vs. Plan Analysis & Evaluation Phase 2 Deliverable Blueprint

**Course Code:** CSE3101 — Agentic Artificial Intelligence  
**Academic Year:** 2026–2027 | 7th Semester B.Tech Computer Science & Engineering  
**Group:** 8 | **Evaluation Phase:** Phase 2 (Mid-Term Evaluation — ~73% Milestone: 8 Core Modules Completed & Verified | 3 Staged Research Novelties)  
**Authors:** Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)  
**Faculty Mentors:** Dr. Soharab Hossain Shaikh, Mr. Pranshu Tiwari  
**Date of Milestone Audit:** October 31, 2026  

***

## 1. Executive Context & Phase 1 to Phase 2 Architectural Evolution

In Phase 1, Group 8 proposed a preliminary multi-agent delivery logistics model. Following faculty feedback, viva cross-examination, and the formal distribution of the **11 Minimum Evaluation Criteria**, our architecture underwent a systematic engineering overhaul.

### 1.1 Formal Problem Decomposition & Agent Justification Invariant
To satisfy the faculty directive against arbitrary agent proliferation (*"Whatever number of agents you decide to use, you must justify each one by the specific problem it solves"*), our revised problem formulation formally partitions urban fleet logistics into **four decoupled computational sub-problems**, each resolved by a dedicated Domain Worker Agent under a Lead Supervisory Orchestrator:
1. **Sub-Problem 1 (Multi-Objective Driver Assignment & Fatigue Arbitration):** Resolved by **Worker 1: CrewAI Dispatch Agent** (`src/agents/crew_dispatch_agent.py`) using ReAct reasoning loops and statutory 9.0h fatigue guardrails.
2. **Sub-Problem 2 (Volatile Environmental Zoning & Enterprise Data Sovereignty):** Resolved by **Worker 2: ChromaDB Retrieval Agent** (`src/agents/crew_retrieval_agent.py`) using air-gapped local Vector RAG in <15ms with zero cloud data leakage.
3. **Sub-Problem 3 (Continuous Spatial Graph Routing & Stochastic Delay Modeling):** Resolved by **Worker 3: Google ADK Route Agent** (`src/agents/adk_route_agent.py`) using declarative AgentCards over A2A (JSON-RPC 2.0), Dijkstra graph search, and Scikit-Learn Random Forest regression ($R^2 = 0.901$).
4. **Sub-Problem 4 (Real-Time Mid-Transit Disruption & Deadlock Recovery):** Resolved by **Worker 4: CrewAI Dynamic Exception Agent** (`src/agents/crew_exception_agent.py`) operating on event-driven standby to achieve an average 18.5-minute delay savings.
5. **The Coordination Matrix (Concurrency & Perimeter Defense):** Resolved by the **Lead Supervisory Orchestrator** (`src/orchestration/hierarchical_orchestrator.py`) managing thread-safe `BlackboardState` under `threading.RLock()` and executing front-door `InputGuard` regex screening in 0.0004s.

### 1.2 Minimum Criteria Gap Analysis and Architectural Refinements:
* **Dual-Framework Heterogeneity (Criteria 6 & 7):** Upgraded from a single-framework design to a heterogeneous dual-framework architecture. Google ADK powers spatial routing; CrewAI powers cognitive dispatch, retrieval, and exception handling.
* **Context Sharing & State Updates (Criterion 1):** Introduced a centralized, typed **Blackboard Shared State (`BlackboardState`)** with reentrant `threading.RLock()` protection, eliminating conversational prompt bloat.
* **Pydantic v2 Strict Typing (Criterion 3):** Standardized all agent decisions (`DispatchDecision`, `RoutePlan`, `ExceptionReplan`) and final deliverables (`FinalDeliveryReport`) with Pydantic v2 algebraic data schemas.
* **Decoupled Tooling via FastMCP (Criterion 2):** Consolidated external capabilities into a formal FastMCP server exposing 5 tools: Driver DB, Routing Engine, Random Forest Delay Predictor, ChromaDB Vector RAG, and Blackboard State Tool.
* **AI Observability & Heatmaps (Criteria 5 & 9):** Deliberately rejected redundant LLM monitoring agents in favor of high-frequency programmatic **Callback hooks (`MASCallbackHandler`)** and OpenTelemetry distributed trace spans.
* **Multi-Tier Guardrails (Criterion 8):** Engineered an input security gateway defending against prompt injections (regex patterns from LAB-06 in 0.0004s) and masking abusive customer personas into `[REDACTED_HOSTILE]`.

***

## 2. 11 Minimum Criteria Ownership & Implementation Ledger

| # | Prescribed Criterion | Implementation Architecture & Exact File Reference | Student Lead / Owner | Phase 2 Milestone Status |
| :- | :--- | :--- | :--- | :---: |
| **C01** | **Blackboard Shared State** | Centralized `BlackboardState` in `src/schemas/blackboard.py`, managed by `src/orchestration/blackboard_manager.py` with `threading.RLock()` concurrency control and FastMCP tool binding. | **Bhumika Yadav** (Schema)<br>**Aadit Bassi** (Store) | **100% Verified (Phase 2)** |
| **C02** | **FastMCP Tool Integration ($\ge 2$)** | FastMCP server (`src/mcp/server.py`) exposing 5 tools: Driver DB, Routing Engine, ML Delay Forecaster, ChromaDB Vector RAG, and Blackboard State. | **Aadit Bassi** | **100% Verified (Phase 2)** |
| **C03** | **Structured Pydantic Outputs** | Strongly typed models (`DispatchDecision`, `RoutePlan`, `ExceptionReplan`, `FinalDeliveryReport`) in `src/schemas/`. Formatted as JSON & Markdown tables. | **Bhumika Yadav** | **100% Verified (Phase 2)** |
| **C04** | **Agentic Design Patterns (Hierarchical MAS)** | Comparative implementation of **Hierarchical Orchestration** (`hierarchical_orchestrator.py`) vs. **Sequential Pipeline** (`sequential_orchestrator.py`) with parallel context gathering. | **Bhumika Yadav** | **100% Verified (Phase 2)** |
| **C05** | **Callbacks & Latency Heatmaps** | `MASCallbackHandler` (`src/observability/callbacks.py`) tracking lifecycle events (`on_agent_start`, `on_tool_start`, `on_agent_end`, `on_exception`). Generated 2D density heatmaps across 72 runs. | **Sahil Mudgil** | **100% Verified (Phase 2)** |
| **C06** | **A2A Interoperability (JSON-RPC 2.0)** | `A2ABridge` (`src/agents/a2a_bridge.py`) routing structured `A2AMessage` envelopes between CrewAI agents and the Google ADK Route Agent via HTTP `/api/a2a/route`. | **Aadit Bassi** | **100% Verified (Phase 2)** |
| **C07** | **CrewAI + Google ADK Dual Framework** | Google ADK powers `adk_route_agent.py`; CrewAI powers `crew_dispatch_agent.py`, `crew_retrieval_agent.py`, `crew_exception_agent.py`, and `hierarchical_orchestrator.py`. | **Aadit Bassi** (ADK)<br>**Bhumika Yadav** (CrewAI) | **100% Verified (Phase 2)** |
| **C08** | **Security & Multi-Tier Guardrails** | Multi-tier defense in `src/guardrails/`: `InputGuard` (regex injection defense in 0.0004s + abusive masking), `ToolValidator`, and `BusinessGuardrails` (hours <= 9.0h). | **Akshat Nagori** (Input)<br>**Sahil Mudgil** (Rules) | **100% Verified (Phase 2)** |
| **C09** | **AI Observability & Tracing** | OpenTelemetry trace tree in `src/observability/tracing.py` linking root order IDs to sub-spans. Multi-host OTel Collector daemon export to Jaeger dashboard staged for End-Term. | **Sahil Mudgil** | **Staged: Phase 3 Research Novelty** |
| **C10** | **Cloud-Scale Benchmarks & Pareto Analysis** | Baseline 72 factorial runs completed with boxplots and heatmaps. Cloud-scale 100+ factorial evaluation matrix across 3 architectures with Pareto frontier optimization staged for End-Term. | **Sahil Mudgil**<br>**Akshat Nagori** | **Staged: Phase 3 Research Novelty** |
| **C11** | **Cloud Platform Deployment** | Production Dockerfile and docker-compose.yml configured. Live multi-cloud VM deployment (AWS EC2 / GCP) with Cloudflare edge worker bridge staged for End-Term. | **Aadit Bassi** | **Staged: Phase 3 Research Novelty** |

**Overall Project Milestone Status:** **~73% Complete** (Exactly 8 of 11 Criteria 100% Verified for Eval-2 | 3 Staged Research Novelties Reserved for End-Term Defense).

***

## 3. Phase-by-Phase Roadmap & Milestone Timeline

```
PHASE 1: Foundations & Architecture  ──>  PHASE 2: Core Engineering & Proof  ──>  PHASE 3: Polish & Defense
(Aug 15 - Oct 10) [COMPLETED]             (Oct 11 - Oct 31) [ACHIEVED: ~73%]      (Nov 01 - Nov 20) [PLANNED]
• Topic definition & PEAS                • Google ADK + CrewAI Integration       • Multi-cloud production deployment
• Initial synopsis & role matrix         • FastMCP server (5 tools)              • Final report in university format
• Synthetic dataset curation             • Blackboard State & A2A Bridge         • Live interactive dashboard (Streamlit)
• Baseline literature review             • 72-run benchmark & boxplots           • Viva practice across all modules
                                         • Multi-tier guardrails & heatmaps
```

### Detailed Sprint Execution Ledger:

| Window | Milestone / Deliverable | Key Technical Objectives & Artifacts | Status |
| :--- | :--- | :--- | :---: |
| **Oct 11 – Oct 18** | **Infrastructure & Schemas** | Pydantic v2 schemas (`BlackboardState`, `A2AMessage`, `FinalDeliveryReport`); FastMCP server; synthetic datasets (`orders.csv`, `drivers.csv`, `traffic.csv`, `delivery_history.csv`). | **Completed** |
| **Oct 19 – Oct 24** | **Agent Development & A2A** | Implement Google ADK Route Agent; CrewAI Dispatch & Retrieval Agents; A2A communication bridge; Random Forest delay predictor training ($R^2 = 0.901$). | **Completed** |
| **Oct 25 – Oct 29** | **Guardrails & Orchestration** | `InputGuard` (injection defense + abusive masking); `BusinessGuardrails` (9.0h rule); Hierarchical Manager and Sequential Orchestrators; Exception recovery loop. | **Completed** |
| **Oct 30 – Oct 31** | **Eval-2 Benchmark & Artifacts** | Run 72-run benchmark matrix; generate publication-quality boxplots and heatmaps; execute pytest suite (49/49 passing); author Eval-2 documentation. | **Completed** |
| **Nov 01 – Nov 08** | **Production Cloud Containerization** | Docker Compose orchestration; health check endpoints; live cloud VM deployment; latency profiling under cloud network conditions. | **Planned** |
| **Nov 09 – Nov 15** | **UI Dashboard & Full Report** | Interactive Streamlit operations dashboard; comprehensive Phase 3 project report (approx. 25–30 pages) matching the provided university thesis template. | **Planned** |
| **Nov 16 – Nov 20** | **Final Defense & Viva Readiness** | Peer cross-examination; code walkthrough rehearsals ensuring every member can modify and defend any component under evaluation. | **Planned** |

***

## 4. Team Responsibility Matrix

| Member | Roll No. | Primary Role | Core Modules Owned | Eval Criteria |
| :--- | :---: | :--- | :--- | :---: |
| **Bhumika Yadav** | 230732 | **Dispatch & Orchestration Lead** | Hierarchical Orchestrator, Sequential Pipeline, CrewAI Dispatch Agent, Blackboard Schema, Pydantic Structured Outputs. | 1, 3, 4, 7 |
| **Aadit Bassi** | 230728 | **Routing, Tooling & Integration Lead** | Google ADK Route Agent, A2A Protocol Bridge, FastMCP Server (5 tools), Docker Containerization, Cloud Deployment. | 1, 2, 6, 7, 11 |
| **Akshat Nagori** | 230682 | **Retrieval, Prompts & Security Lead** | Local Vector RAG Retrieval Agent, ChromaDB Knowledge Base, Input Guard (Prompt Injection & Abusive Masking), Persona Variance Prompts. | 8, 10 |
| **Sahil Mudgil** | 230743 | **ML, Observability & Evaluation Lead** | Random Forest Delay Prediction Model, Business Compliance Guardrails, Callbacks & OpenTelemetry Tracing, 72-Run Benchmark, Boxplots & Heatmaps. | 5, 8, 9, 10 |

***

## 5. Risk Assessment & Contingency Fallback Plan

| Risk Description | Probability | Severity | Mitigation & Contingency Strategy |
| :--- | :---: | :---: | :--- |
| **Google ADK & CrewAI A2A Link Disruption** | Low | High | Pinned exact package versions in `requirements.txt`. Tested in-process and HTTP transport. Fallback to direct Python A2A client wrapper already verified. |
| **ChromaDB Embedding Download Latency** | Low | Medium | High-speed in-memory keyword-relevance fallback built into `ChromaRAGTool` ensures zero disruption if network is unavailable. |
| **Cloud VM CPU Bottleneck for Local LLM** | Medium | Medium | Quantized small model or lightweight embeddings selected; retrieval calls execute in parallel gathering step, hiding inference latency. |
| **API Quota Exceedance during Benchmarking** | Low | Low | Built-in offline deterministic simulation mode exercises all agent callbacks, tools, guardrails, and telemetry without burning API quotas. |

***
