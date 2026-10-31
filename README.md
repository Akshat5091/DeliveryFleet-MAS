# 🚚 Autonomous Multi-Agent Delivery Fleet Coordination & Dispatch System
**Course:** CSE3101: Agentic AI — B.Tech CSE Semester VII  
**Evaluation Phase:** Phase 2 (75% Milestone — Actual Progress: **~78% Complete**)  
**Group Number:** 9  
**Team Members:** Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)  
**Faculty Mentors:** Dr. Soharab Hossain Shaikh, Mr. Pranshu Tiwari  

---

## 🎯 Project Overview & Core Philosophy

This platform implements an enterprise-grade autonomous Multi-Agent System (MAS) designed to solve the critical volatility, multi-factor trade-offs, and dynamic disruptions of last-mile logistics dispatch. 

Built strictly on **Google Agent Development Kit (ADK)** and **CrewAI**, the system features:
1. **Centralized Blackboard Architecture:** Single source of truth with `threading.RLock()` reentrant concurrency protection and comprehensive provenance audit trails.
2. **Model Context Protocol (FastMCP):** 5 production MCP tools exposing fleet lookups, routing engines, Random Forest ML delay forecasting, ChromaDB Vector RAG, and blackboard state synchronization.
3. **Agent-to-Agent (A2A) Protocol Bridge:** Framework-agnostic JSON-RPC messaging linking CrewAI dispatch and exception agents to the Google ADK route optimization agent.
4. **Multi-Tier Safety Guardrails:** Sub-millisecond prompt injection screening, toxic customer language sanitization (`[REDACTED_HOSTILE]`), and statutory 9.0-hour maximum shift limit enforcement (`BLOCK > FLAG_FOR_REVIEW > ALLOW`).
5. **Interactive Web Dashboard & Browser Testing:** Production FastAPI web interface with automated Selenium browser test coverage (13/13 scenarios verified).

---

## 🏛️ Directory Layout

```
DeliveryFleet-MAS/
├── artifacts/                               # Visual Diagnostic Assets & Telemetry
│   ├── browser_screenshots/                 # 13 verified Selenium browser UI screenshots
│   ├── latency_boxplot.png                  # Latency distribution by architecture & prompt style
│   ├── cost_boxplot.png                     # Cost distribution across customer personas
│   ├── agent_metric_heatmap.png             # Operational metrics correlation matrix
│   ├── agent_run_heatmap.png                # Per-agent execution density across 48 benchmark runs
│   ├── evaluation_metrics_heatmap.png       # Shannon Entropy H(X), Sensitivity, and Specificity
│   ├── benchmark_results.json               # Full JSON telemetry dump of 48 benchmark runs
│   └── benchmark_summary.csv                # Tabular summary of 48 factorial runs
├── data/                                    # Datasets & Local Vector Knowledge Base
│   ├── orders.csv                           # 20 benchmark delivery consignment orders
│   ├── drivers.csv                          # 10 active driver profiles with hours and vehicle capacities
│   ├── traffic.csv                          # Congestion speed factors across 12 inter-zone corridors
│   ├── weather.csv                          # Precipitation and visibility readings
│   ├── delivery_history.csv                 # 500 historical transit logs for ML delay training
│   ├── chroma_db/                           # Local ChromaDB vector database storage
│   └── knowledge_base/                      # Municipal delivery bylaws and shift policies
├── Eval 2 Documents/                        # Official Phase 2 Evaluation Deliverables
│   ├── Work_In_Progress_Report.docx         # Publication-grade technical report (10 embedded figures)
│   ├── Updated_Problem_Statement.docx       # Project Charter, PEAS formulation, and agent rationale
│   ├── Updated_Project_Plan.docx            # Revised project plan, timeline, WBS, and risk ledger
│   ├── 1_Slide_Coverage_Matrix_Group8.pptx  # 16:9 widescreen presentation slide linking all criteria
│   ├── EVAL2_WORK_IN_PROGRESS_REPORT.md     # Markdown equivalent of WIP Report
│   ├── UPDATED_PROBLEM_STATEMENT.md         # Markdown equivalent of Problem Statement
│   ├── UPDATED_PROJECT_PLAN.md              # Markdown equivalent of Project Plan
│   └── EVAL2_1_SLIDE_COVERAGE_MATRIX.md     # Markdown equivalent of 1-slide matrix
├── logs/                                    # Distributed trace spans and telemetry logs
│   └── run_events.jsonl                     # OpenTelemetry trace event ledger
├── scripts/                                 # Build & documentation generation scripts
│   ├── build_all_eval2_documents.py         # Unified master generator for all deliverables
│   ├── create_formal_docs.py                # Generator for Problem Statement & Project Plan .docx
│   ├── update_formal_wip_report.py          # Generator for enhanced WIP Report .docx with figures
│   └── sync_markdown_report.py              # Markdown report synchronizer
├── src/                                     # Core Source Code
│   ├── config.py                            # Central settings, constants, and paths
│   ├── agents/                              # Core Agent Implementations
│   │   ├── adk_route_agent.py               # Google ADK Route Optimization Agent
│   │   ├── crew_dispatch_agent.py           # CrewAI Dispatch Agent (ReAct reasoning)
│   │   ├── crew_retrieval_agent.py          # CrewAI Retrieval Agent (Local ChromaDB RAG)
│   │   ├── crew_exception_agent.py          # CrewAI Exception Agent (Dynamic contingency replan)
│   │   └── a2a_bridge.py                    # A2A Inter-Framework Protocol Bridge
│   ├── evaluation/                          # Benchmark & Analytics Suite
│   │   ├── agent_evaluator.py               # Shannon entropy, sensitivity, and specificity metrics
│   │   ├── benchmark_runner.py              # 48-run factorial benchmark runner
│   │   ├── personas.py                      # 4 customer persona prompt variations
│   │   └── visualizer.py                    # Boxplot and heatmap generator
│   ├── guardrails/                          # Multi-Tier Safety Layer
│   │   ├── input_guard.py                   # Regex prompt injection defense & hostile token masking
│   │   ├── tool_validator.py                # Return schema validation contracts
│   │   └── business_guardrails.py           # Statutory 9.0h driving limits & municipal freight caps
│   ├── mcp/                                 # Model Context Protocol
│   │   ├── server.py                        # FastMCP server exposing 5 tools
│   │   └── tools/                           # Tool implementations (DriverDB, Routing, Delay, RAG)
│   ├── observability/                       # Monitoring & Tracing
│   │   ├── callbacks.py                     # Unified CrewAI & ADK lifecycle hooks
│   │   ├── run_logger.py                    # Run event logger recording latency, tokens, cost
│   │   └── tracing.py                       # OpenTelemetry trace tree generator
│   ├── orchestration/                       # Multi-Agent Workflow Patterns
│   │   ├── hierarchical_orchestrator.py     # Supervised Hierarchical Manager MAS Pattern
│   │   ├── sequential_orchestrator.py       # Sequential Pipeline Pattern
│   │   └── blackboard_manager.py            # Blackboard state coordinator with RLock
│   ├── schemas/                             # Pydantic v2 schemas
│   │   ├── a2a.py                           # A2A message envelopes and AgentCard
│   │   ├── blackboard.py                    # Blackboard shared state schema
│   │   ├── decisions.py                     # Decision models (Dispatch, Route, Exception)
│   │   └── reports.py                       # FinalDeliveryReport (JSON & Markdown table)
│   └── web/                                 # Interactive Web Dashboard
│       ├── app.py                           # FastAPI backend server
│       └── index.html                       # Studio-grade dark mode interactive frontend
├── tests/                                   # Pytest Test Suite (40 tests, 100% passing)
│   ├── conftest.py                          # Pytest fixtures and environment setup
│   ├── test_academic_metrics_and_resilience.py
│   ├── test_concurrency_blackboard.py
│   ├── test_edge_case_dispatch.py
│   ├── test_end_to_end_pipeline.py
│   ├── test_guardrails.py
│   ├── test_math_and_float_boundaries.py
│   └── test_mcp_tools.py
├── demo.py                                  # Live interactive CLI demonstration script
├── docker-compose.yml                       # Multi-service container orchestration
├── Dockerfile                               # Production multi-stage Docker container
├── pytest.ini                               # Pytest root configuration
├── requirements.txt                         # Pinned production dependencies
├── run_dashboard.py                         # 1-command Web UI Dashboard launcher
├── SETUP_GUIDE.md                           # Team quickstart & execution guide
└── test_browser_suite.py                    # Automated Selenium browser verification suite
```

---

## 🚀 Quickstart & Verification Guide

### 1. Installation
Navigate to `DeliveryFleet-MAS/` and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run Automated Pytest Suite (40 of 40 Passing)
Verify that all unit tests, concurrency locks, A2A messages, MCP tools, guardrails, and metrics pass:
```bash
pytest -v
```
*Expected Result:* `40 passed in ~10.5s` with 0 warnings and 0 errors.

### 3. Launch Interactive Web Dashboard
Start the production web interface:
```bash
python run_dashboard.py
```
Open your browser to: **http://127.0.0.1:8000**
- Execute 8 curated operational and edge case scenarios with 1 click.
- Experiment with custom consignments in the Interactive Sandbox.
- Inspect diagnostic heatmaps, latency boxplots, and the active driver fleet database.

### 4. Run Automated Browser Verification Suite
Execute headless Chrome via Selenium to empirically verify the web dashboard:
```bash
python test_browser_suite.py
```
*Expected Result:* All 13 test scenarios and UI interfaces verified with fresh screenshot artifacts saved in `artifacts/browser_screenshots/`.

### 5. Run Interactive CLI Demonstration
Execute the full terminal-based demonstration and 48-run benchmark:
```bash
python demo.py
```

---

## 👥 Authors & Academic Attribution
**Course:** CSE3101: Agentic AI — Semester VII B.Tech CSE  
**Group 8:**
* **Bhumika Yadav (230732):** Dispatch & Orchestration Lead (Hierarchical Orchestrator, CrewAI Dispatch Agent, Blackboard State)
* **Aadit Bassi (230728):** Routing, Tooling & Integration Lead (Google ADK Route Agent, A2A Bridge, FastMCP Server, Docker)
* **Akshat Nagori (230682):** Retrieval, Prompts & Security Lead (ChromaDB Vector RAG, Input Security Guard, Persona Prompts, Web Dashboard)
* **Sahil Mudgil (230743):** ML, Observability & Evaluation Lead (Random Forest Delay Model, Business Guardrails, MASTracer, 48-Run Benchmark)
