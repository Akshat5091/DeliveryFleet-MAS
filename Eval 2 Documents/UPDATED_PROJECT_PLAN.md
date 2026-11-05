# 📅 Updated Project Plan: Multi-Agent Delivery Fleet Coordination System

**Course Code:** CSE3101 — Agentic AI  
**Academic Year:** 2026–2027 | 7th Semester B.Tech CSE  
**Group:** 8 | **Phase:** Phase 2 (Mid-Term Evaluation — ~73% Milestone: 8 Core Modules Completed & Verified | 3 Staged Research Novelties)  
**Team Members:** Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)  
**Date of Update:** October 31, 2026  

---

## 1. Executive Context & Phase 1 to Phase 2 Architectural Evolution

In Phase 1, Group 8 proposed a preliminary 5-agent logistics dispatch model. Following faculty feedback and the distribution of the **11 Minimum Evaluation Criteria**, our architecture underwent a rigorous technical review. 

### Gap Analysis and Architectural Refinements:
1. **Mandatory Framework Heterogeneity (Criteria 6 & 7):** Upgraded from a single-framework design to a dual-framework architecture. The **Route Optimization Agent** is built natively using **Google Agent Development Kit (ADK)**, while the **Fleet Orchestrator, Dispatch Agent, Retrieval Agent, and Exception Agent** are built using **CrewAI**.
2. **Context Sharing & State Updates (Criterion 1):** Introduced a centralized, typed **Blackboard Shared State (`BlackboardState`)** accessible via an MCP tool, with complete provenance auditing. Maintained A2A peer messaging alongside it for empirical comparison.
3. **Pydantic V2 Strict Typing (Criterion 3):** Standardized all agent decisions (`DispatchDecision`, `RoutePlan`, `ExceptionReplan`) and outputs (`FinalDeliveryReport`) with Pydantic v2 schemas, generating both JSON and Markdown tables.
4. **Tool Standard via FastMCP (Criterion 2):** Consolidated external capabilities into a formal FastMCP server exposing 5 tools (Driver DB, Routing Engine, Random Forest Delay Predictor, ChromaDB Vector RAG, and Blackboard State Tool).
5. **AI Observability & Heatmaps (Criteria 5 & 9):** Replaced an expensive, redundant LLM "Monitoring Agent" with high-frequency programmatic **Callback hooks** and an **OpenTelemetry-compatible distributed tracing ledger**. Developed heatmap and boxplot visualizers.
6. **Multi-Tier Guardrails (Criterion 8):** Engineered an input security gateway defending against prompt injections (regex patterns from LAB-06) and masking abusive customer personas.

---

## 2. 11 Minimum Criteria Ownership & Implementation Ledger

| # | Evaluation Criterion | Implementation Architecture & Module | Team Lead / Owner | Current Status (Phase 2) |
| :- | :--- | :--- | :--- | :---: |
| **1** | **Blackboard Shared State** | Centralized `BlackboardState` in `src/schemas/blackboard.py`, managed by `src/orchestration/blackboard_manager.py` and exposed via MCP tool. Provenance trail records every write. | **Bhumika Yadav** (Schema)<br>**Aadit Bassi** (Store) | **100% Complete** ✅ |
| **2** | **MCP Tool Integration** | FastMCP server (`src/mcp/server.py`) exposing 5 tools: Driver DB, Routing Engine, ML Delay Forecaster, ChromaDB Vector RAG, and Blackboard State. | **Aadit Bassi** | **100% Complete** ✅ |
| **3** | **Structured Pydantic Outputs** | Strongly typed models (`DispatchDecision`, `RoutePlan`, `ExceptionReplan`, `FinalDeliveryReport`) in `src/schemas/`. Formatted as JSON & Markdown tables. | **Bhumika Yadav** | **100% Complete** ✅ |
| **4** | **Agentic Design Patterns** | Comparative implementation of **Hierarchical Orchestration** (`hierarchical_orchestrator.py`) vs. **Sequential Pipeline** (`sequential_orchestrator.py`) with Parallel Gathering. | **Bhumika Yadav** | **100% Complete** ✅ |
| **5** | **Callbacks & Latency Heatmaps** | `MASCallbackHandler` (`src/observability/callbacks.py`) tracking lifecycle events (`on_agent_start`, `on_tool_start`, `on_agent_end`, `on_exception`). Generated 2D density heatmaps across 72 factorial runs. | **Sahil Mudgil** | **100% Complete** ✅ |
| **6** | **A2A Interoperability** | `A2ABridge` (`src/agents/a2a_bridge.py`) routing structured `A2AMessage` envelopes between CrewAI agents and the Google ADK Route Agent. | **Aadit Bassi** | **100% Complete** ✅ |
| **7** | **CrewAI + Google ADK** | Google ADK powers `adk_route_agent.py`; CrewAI powers `crew_dispatch_agent.py`, `crew_retrieval_agent.py`, `crew_exception_agent.py`, and `hierarchical_orchestrator.py`. | **Aadit Bassi** (ADK)<br>**Bhumika Yadav** (CrewAI) | **100% Complete** ✅ |
| **8** | **Security & Guardrails** | Multi-tier defense in `src/guardrails/`: `InputGuard` (regex injection defense in 0.0004s + abusive masking), `ToolValidator`, and `BusinessGuardrails` (hours <= 9.0h). | **Akshat Nagori** (Input)<br>**Sahil Mudgil** (Rules) | **100% Complete** ✅ |
| **9** | **AI Observability & Tracing** | OpenTelemetry trace tree in src/observability/tracing.py linking root order IDs to sub-spans. Multi-host OTel Collector daemon export to Jaeger dashboard reserved for End-Term. | **Sahil Mudgil** | **Phase 3 Novelty** 🚀 |
| **10** | **Cloud-Scale Benchmarks & Pareto Analysis** | Baseline 72 factorial runs completed with boxplots and heatmaps. 100+ cloud factorial evaluation matrix across 3 architectures with Pareto frontier optimization reserved for End-Term. | **Sahil Mudgil**<br>**Akshat Nagori** | **Phase 3 Novelty** 🚀 |
| **11** | **Cloud Deployment** | Production Dockerfile and docker-compose.yml configured. Live multi-cloud VM deployment (AWS EC2/GCP) with Cloudflare edge worker bridge reserved for End-Term. | **Aadit Bassi** | **Phase 3 Novelty** 🚀 |

**Overall Project Milestone Status:** **~73% Complete** (Exactly 8 of 11 Criteria 100% Verified for Eval-2 | 3 Staged Research Novelties Reserved for End-Term Defense).

---

## 3. Phase-by-Phase Roadmap & Timeline

```
PHASE 1: Foundations & Architecture  ──>  PHASE 2: Core Engineering & Proof  ──>  PHASE 3: Polish & Defense
(Aug 15 - Oct 10)                        (Oct 11 - Oct 31) [CURRENT]             (Nov 01 - Nov 20)
• Topic definition & PEAS                • Google ADK + CrewAI Integration       • Multi-cloud production deployment
• Initial synopsis & role matrix         • FastMCP server (5 tools)              • Final report in university format
• Synthetic dataset curation             • Blackboard State & A2A Bridge         • Live interactive dashboard (Streamlit)
• Baseline literature review             • 72-run benchmark & boxplots           • Viva practice across all modules
                                         • Multi-tier guardrails & heatmaps
```

### Detailed Schedule:

| Window | Milestone / Deliverable | Key Technical Objectives | Status |
| :--- | :--- | :--- | :---: |
| **Oct 11 – Oct 18** | **Infrastructure & Schemas** | Pydantic v2 schemas (`BlackboardState`, `A2AMessage`, `FinalDeliveryReport`); FastMCP server; synthetic datasets (`orders.csv`, `drivers.csv`, `traffic.csv`, `delivery_history.csv`). | **DONE** ✅ |
| **Oct 19 – Oct 24** | **Agent Development & A2A** | Implement Google ADK Route Agent; CrewAI Dispatch & Retrieval Agents; A2A communication bridge; Random Forest delay predictor training. | **DONE** ✅ |
| **Oct 25 – Oct 29** | **Guardrails & Orchestration** | InputGuard (injection defense + abusive masking); BusinessGuardrails (9.0h rule); Hierarchical Manager and Sequential Orchestrators; Exception recovery loop. | **DONE** ✅ |
| **Oct 30 – Oct 31** | **Eval-2 Benchmark & Artifacts** | Run 72-run benchmark matrix; generate publication-quality boxplots and heatmaps; execute pytest suite (49/49 passing); author Eval-2 documentation. | **DONE** ✅ |
| **Nov 01 – Nov 08** | **Production Cloud Containerization** | Docker Compose orchestration; health check endpoints; live cloud VM deployment; latency profiling under cloud network conditions. | **PLANNED** ⏳ |
| **Nov 09 – Nov 15** | **UI Dashboard & Full Report** | Interactive Streamlit operations dashboard; comprehensive Phase 3 project report (approx. 25–30 pages) matching the provided university thesis template. | **PLANNED** ⏳ |
| **Nov 16 – Nov 20** | **Final Defense & Viva Readiness** | Peer cross-examination; code walkthrough rehearsals ensuring every member can modify and defend any component. | **PLANNED** ⏳ |

---

## 4. Team Responsibility Matrix

| Member | Roll No. | Primary Role | Core Modules Owned | Eval Criteria |
| :--- | :---: | :--- | :--- | :---: |
| **Bhumika Yadav** | 230732 | **Dispatch & Orchestration Lead** | Hierarchical Orchestrator, Sequential Pipeline, CrewAI Dispatch Agent, Blackboard Schema, Pydantic Structured Outputs. | 1, 3, 4, 7 |
| **Aadit Bassi** | 230728 | **Routing, Tooling & Integration Lead** | Google ADK Route Agent, A2A Protocol Bridge, FastMCP Server (5 tools), Docker Containerization, Cloud Deployment. | 1, 2, 6, 7, 11 |
| **Akshat Nagori** | 230682 | **Retrieval, Prompts & Security Lead** | Local Vector RAG Retrieval Agent, ChromaDB Knowledge Base, Input Guard (Prompt Injection & Abusive Masking), Persona Variance Prompts. | 8, 10 |
| **Sahil Mudgil** | 230743 | **ML, Observability & Evaluation Lead** | Random Forest Delay Prediction Model, Business Compliance Guardrails, Callbacks & OpenTelemetry Tracing, 72-Run Benchmark, Boxplots & Heatmaps. | 5, 8, 9, 10 |

---

## 5. Risk Assessment & Contingency Fallback Plan

| Risk Description | Probability | Severity | Mitigation & Contingency Strategy |
| :--- | :---: | :---: | :--- |
| **Google ADK & CrewAI A2A Link Disruption** | Low | High | Pinned exact package versions in `requirements.txt`. Tested in-process and HTTP transport. Fallback to direct Python A2A client wrapper already verified. |
| **ChromaDB Embedding Download Latency** | Low | Medium | High-speed in-memory keyword-relevance fallback built into `ChromaRAGTool` ensures zero disruption if network is unavailable. |
| **Cloud VM CPU Bottleneck for Local LLM** | Medium | Medium | Quantized small model or lightweight embeddings selected; retrieval calls execute in parallel gathering step, hiding inference latency. |
| **API Quota Exceedance during Benchmarking** | Low | Low | Built-in offline deterministic simulation mode exercises all agent callbacks, tools, guardrails, and telemetry without burning API quotas. |
