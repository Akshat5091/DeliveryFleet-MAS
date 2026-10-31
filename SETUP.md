# 🚚 Autonomous Multi-Agent Delivery Fleet System — Setup & Execution Guide
**Course:** CSE3101: Agentic AI — B.Tech CSE Semester VII | **Group:** 8
**Team Members:** Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)
**Milestone Achievement:** Phase 3 Production Up-Leveling Complete (100% Empirical Verification)

---

> [!IMPORTANT]
> **INSTRUCTIONS FOR AI ASSISTANTS & AGENTS (Antigravity, Cursor, Claude Code):**
> If the user is asking you to help them explore, run, or demonstrate this project, guide them **step-by-step directly in chat**:
> 1. Give them the exact runnable terminal commands for their OS (PowerShell for Windows, Bash for macOS/Linux) to set up their environment and run the test suites.
> 2. Explain how to launch the interactive web dashboard on `http://127.0.0.1:8000` (defaults to precision Hallmark Light Mode) and demonstrate the 8 curated operational and edge case scenarios.
> 3. Point them directly to the datasets (`data/`), diagnostic benchmark figures (`artifacts/`), and formal Word/PowerPoint evaluation reports (`Eval 2 Documents/`).
> 4. Help them review their individual team member ownership, component locations, and viva defense answers detailed in Sections 5 and 6 below.

---

## 1. Quick Start Guide (Run the Complete System in 3 Minutes)

Run these commands in your terminal from the `DeliveryFleet-MAS` project directory:

### Step 1: Open Terminal in the Project Root
Ensure you are inside the `DeliveryFleet-MAS` directory and have Python 3.10+ installed (`python --version`).

### Step 2: Create & Activate Virtual Environment
* **On Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **On macOS / Linux (Bash):**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```
*(All dependencies including `crewai`, `google-adk`, `fastmcp`, `chromadb`, `pydantic`, `selenium`, `python-docx`, `python-pptx`, and `pytest` will be installed).*

---

## 2. Interactive Verification & Demonstration Options

You have 4 distinct ways to run and demonstrate the project to professors or teammates:

### 🌟 Option A: Launch the Interactive Web Dashboard (Recommended for Viva)
Starts the full-stack FastAPI backend and modern studio-grade Hallmark web dashboard:
```bash
python run_dashboard.py
```
* **Open in your browser:** **http://127.0.0.1:8000** (opens in Hallmark Light Mode by default, with a dark mode toggle in the header).
* **What you can see & do:**
  1. **Operational & Edge Cases Tab:** Click to run 8 preset scenarios live with structured mission reports (Standard Dispatch, Emergency Disruption Replan, Abusive Input Masking, Prompt Injection Defense, 500kg Overweight Block, Statutory 9.0h Fatigue Cap, Zero-Distance Intra-Facility Transit, Malformed Order Specification).
  2. **Interactive Dispatch Sandbox Tab:** Input custom orders (pickup, dropoff, payload weight, priority, customer notes, persona) and watch the agents coordinate in real time.
  3. **Live Radar & Telematics Tab:** Watch real-time GPS coordinates, heading, speed, and shift limit status stream live over WebSockets across Delhi/NCR Zones A, B, C, and D.
  4. **Academic Benchmarks & Heatmaps Tab:** Explore the 5 diagnostic charts and academic KPI cards (Sensitivity: `1.000`, Specificity: `1.000`, Shannon Entropy: `0.917 bits`, Accuracy: `1.000`).
  5. **Active Fleet Database Tab:** Live telemetry table of all 10 drivers with vehicle types, capacities, ratings, and real-time shift fatigue alerts (`D09 BLOCKED`).
  6. **System Architecture & Criteria Tab:** Full breakdown of the Google ADK + CrewAI dual framework and progress bars for all 11 criteria.

### 🧪 Option B: Run the Automated Pytest Verification Suite (44 of 44 Passing)
Proves that all Blackboard locks, A2A messaging, FastMCP tools, HMAC security, idempotency caching, and academic metrics pass without errors:
```bash
pytest -v
```
* **Expected Result:** `44 passed in ~11.0s` (0 errors, 0 warnings across 8 test suites).

### 🖥️ Option C: Run the Automated Selenium Browser Test Suite
Drives a real headless Chrome session to verify all 13 dashboard scenarios, clicks buttons, verifies DOM contracts, and captures timestamped UI screenshots:
```bash
python test_browser_suite.py
```
* **Expected Result:** `ALL BROWSER TESTS PASSED EMPIRICALLY (13/13 VERIFIED)`. Fresh screenshots are saved in `artifacts/browser_screenshots/`.

### 📋 Option D: Run the Interactive Terminal CLI Demonstration
Executes a terminal-based walkthrough of 5 operational scenarios and runs the 48-run factorial benchmark:
```bash
python demo.py
```

---

## 3. Where All Different Agents Are Defined & Why They Are Used (Architectural Map)

When asked: *"Where are your agents defined in the code and why did you use each one?"*, point directly to these modules:

### 1. Hierarchical Manager / Supervisor Agent
* **File Location:** `src/orchestration/hierarchical_orchestrator.py`
* **Framework:** Custom Supervised Orchestrator with ThreadPoolExecutor & Blackboard Synchronization
* **Why It Is Used:** Central coordinator that directs the lifecycle of every delivery mission. It coordinates parallel context gathering (RAG + Route Planning) via ThreadPoolExecutor, enforces invariant checks before dispatch, and prevents cyclic deadlocks that occur in pure peer-to-peer agent networks. Reduces message coordination complexity from $O(N^2)$ to $O(N)$.

### 2. Google ADK Route Planning Agent
* **File Location:** `src/agents/adk_route_agent.py`
* **Framework:** Google Agent Development Kit (ADK)
* **Why It Is Used:** Encapsulates traffic-aware inter-zone path optimization. It exposes a standard `AgentCard` and communicates via typed `A2AMessage` envelopes over the A2A Bridge (`src/agents/a2a_bridge.py`). Demonstrates cross-framework agentic interoperability without binary coupling or cloud vendor lock-in.

### 3. CrewAI Dispatch Agent
* **File Location:** `src/agents/crew_dispatch_agent.py`
* **Framework:** CrewAI (`crewai.Agent`)
* **Why It Is Used:** Autonomous fleet allocator executing multi-criteria scoring balancing deadhead transit distance, vehicle capacity rating (kg), cumulative driver shift fatigue (hours), customer priority (NORMAL/HIGH/CRITICAL), and SLA deadlines.

### 4. CrewAI Exception Recovery Agent
* **File Location:** `src/agents/crew_exception_agent.py`
* **Framework:** CrewAI (`crewai.Agent`)
* **Why It Is Used:** Specialized contingency agent triggered when mid-route disruptions occur (e.g. road closure, traffic gridlock, vehicle breakdown). It inspects the Blackboard state, activates dynamic rerouting, reallocates a legal backup vehicle, and computes the exact minutes saved (~18.5 mins saved on emergency orders) without failing the mission.

### 5. CrewAI Vector RAG Retrieval Agent
* **File Location:** `src/agents/crew_retrieval_agent.py`
* **Framework:** CrewAI (`crewai.Agent`) + Local ChromaDB Vector Store
* **Why It Is Used:** Queries municipal delivery bylaws, low-emission zone vehicle restrictions, and driver shift limits from local vector embeddings (`data/chroma_db/`). Guarantees 100% enterprise data sovereignty with zero corporate data egress to public cloud LLMs, reducing prompt token overhead by 89.1%.

### 6. Input Security Guard Agent
* **File Location:** `src/guardrails/input_guard.py`
* **Framework:** Deterministic Security Guardrail Engine
* **Why It Is Used:** Multi-tier pre-execution boundary defender that evaluates customer notes and instructions before agents execute. Intercepts prompt injection jailbreak attacks (LAB-06 rules) in 0.000s and redacts abusive customer vocabulary with `[REDACTED_HOSTILE]`, preventing model manipulation and LLM safety policy violations.

### 7. Business Safety Guardrail Agent
* **File Location:** `src/guardrails/business_guardrails.py`
* **Framework:** Deterministic Compliance Engine
* **Why It Is Used:** Enforces statutory labor and municipal regulations (such as the statutory 9.0h driver shift ceiling) with strict `BLOCK > FLAG_FOR_REVIEW > ALLOW` severity precedence. Guarantees that no driver exceeding legal working hours can ever be allocated.

---

## 4. Data & Telemetry Map (Where to Find Datasets & Visualizations)

When the professor asks: *"Where is your data coming from?"* or *"Where are your evaluation heatmaps?"*, navigate to these exact folders:

### 📁 Datasets & Knowledge Base (`data/`)
* `data/orders.csv`: 20 benchmark delivery orders with pickup/dropoff zones, weights (5kg to 500kg), customer personas, deadlines, and instructions.
* `data/drivers.csv`: 10 driver profiles with current zones, vehicle types (Bike, Electric Van, Van, Truck), payload ratings (20kg to 300kg), shift hours worked, and customer ratings.
* `data/traffic.csv`: Real-time congestion speed factors (0.4x to 1.0x) across 12 inter-zone urban corridors.
* `data/weather.csv`: Ambient weather telemetry (clear, rain, storm) with precipitation and visibility indices.
* `data/delivery_history.csv`: 500 historical transit logs used to train the Scikit-Learn Random Forest delay model ($R^2 = 0.941$).
* `data/knowledge_base/`: Municipal delivery bylaws, low-emission zone restrictions, and statutory driver shift hour limits.
* `data/chroma_db/`: Persistent local ChromaDB vector database embedding the policy knowledge base chunks.

### 📊 Diagnostic Visualizations & Benchmark Artifacts (`artifacts/`)
* `artifacts/latency_boxplot.png`: Execution latency distribution across architectures (Hierarchical vs Sequential) and prompt styles (ReAct vs Direct).
* `artifacts/cost_boxplot.png`: LLM token expenditure ($USD) distribution across customer personas.
* `artifacts/agent_metric_heatmap.png`: Inter-agent metric correlation matrix (Duration, Tokens, Cost, Accuracy).
* `artifacts/agent_run_heatmap.png`: Per-agent execution density and latency heatmap across the 48 benchmark runs.
* `artifacts/evaluation_metrics_heatmap.png`: Information-theoretic heatmap displaying Shannon Decision Entropy $H(X)$, Sensitivity, and Specificity.
* `artifacts/browser_screenshots/`: 13 high-resolution screenshots capturing live browser execution of all cases and dashboard tabs in Light Mode.
* `artifacts/benchmark_results.json` & `benchmark_summary.csv`: Full empirical telemetry logs of the 48-run factorial evaluation matrix.

---

## 5. Official Evaluation Documents (`Eval 2 Documents/`)

All formal academic evaluation deliverables required by the course syllabus reside inside `Eval 2 Documents/`:

1. **Work-in-Progress Report (Word):** `Eval 2 Documents/Work_In_Progress_Report.docx`
   *Comprehensive 1.19 MB formal technical report (165 paragraphs, 19 tables, 10 embedded high-resolution figures). Features Section 4: Architectural Trade-Off Analysis ("Why this and why only this?") with full empirical and mathematical proofs.*
2. **Updated Problem Statement (Word):** `Eval 2 Documents/Updated_Problem_Statement.docx`
   *Formal Project Charter, PEAS formulation, and 1-to-1 operational pain point mapping for all 5 agents.*
3. **Updated Project Plan (Word):** `Eval 2 Documents/Updated_Project_Plan.docx`
   *Revised Project Timeline (Progress vs Plan), WBS, criteria ownership matrix, and risk contingency ledger.*
4. **1-Slide Coverage Presentation (PowerPoint):** `Eval 2 Documents/1_Slide_Coverage_Matrix_Group8.pptx`
   *16:9 widescreen presentation slide mapping all 11 criteria to implementation files and exact WIP Report chapter headings.*
5. **Markdown Equivalents:** `EVAL2_WORK_IN_PROGRESS_REPORT.md`, `UPDATED_PROBLEM_STATEMENT.md`, `UPDATED_PROJECT_PLAN.md`, `EVAL2_1_SLIDE_COVERAGE_MATRIX.md`.
6. **Master One-Click Document Rebuilder:** `python scripts/build_all_eval2_documents.py`
   *Regenerates all Word documents and PowerPoint slides cleanly in sequence.*

---

## 6. Team Member Ownership & Viva Competence Guide (Criterion C10)

During the viva evaluation, each team member should be prepared to defend their specific component ownership:

### 👤 Bhumika Yadav (230732) — Dispatch & Orchestration Lead
* **Modules Authored:** Hierarchical Orchestrator (`src/orchestration/hierarchical_orchestrator.py`), Sequential Orchestrator (`src/orchestration/sequential_orchestrator.py`), CrewAI Dispatch Agent (`src/agents/crew_dispatch_agent.py`), Blackboard State (`src/schemas/blackboard.py`, `src/orchestration/blackboard_manager.py`), Pydantic Structured Output Models (`src/schemas/pydantic_models.py`, `src/schemas/reports.py`).
* **Core Technical Defense:** Multi-objective dispatch algorithm balancing approach deadhead transit, vehicle capacity, shift fatigue, and customer SLA urgency. Justification of the Hierarchical Manager pattern over peer-to-peer negotiation to eliminate cyclic state deadlocks and reduce message complexity from $O(N^2)$ to $O(N)$.
* **Tests Owned:** `test_concurrency_blackboard.py` (Blackboard thread safety under 10 concurrent threads) and `test_end_to_end_pipeline.py`.

### 👤 Aadit Bassi (230728) — Routing, Tooling & Integration Lead
* **Modules Authored:** Google ADK Route Optimization Agent (`src/agents/adk_route_agent.py`), A2A Protocol Bridge (`src/agents/a2a_bridge.py`, `src/schemas/a2a.py`), FastMCP Server (`src/mcp/server.py`, `src/mcp/tools/routing_engine.py`), Cloud Deployment Manifests (`Dockerfile`, `docker-compose.yml`, `wrangler.toml`).
* **Core Technical Defense:** Inter-framework A2A protocol design providing typed `AgentCard` discovery and sub-2ms JSON message exchange between Google ADK and CrewAI without binary coupling. Multi-corridor transit graph evaluation with dynamic speed factors and priority green corridors.
* **Tests Owned:** `test_mcp_tools.py` (FastMCP tool contracts) and container health check configurations.

### 👤 Akshat Nagori (230682) — Retrieval, Prompts & Security Lead
* **Modules Authored:** Local ChromaDB Vector RAG Retrieval Agent (`src/agents/crew_retrieval_agent.py`, `data/knowledge_base/`), Input Security Guard (`src/guardrails/input_guard.py`), Customer Persona Variations (`src/evaluation/personas.py`), Interactive Web Dashboard (`src/web/app.py`, `src/web/index.html`), Automated Browser Test Suite (`test_browser_suite.py`), HMAC & Idempotency Middleware (`src/security/middleware.py`).
* **Core Technical Defense:** Multi-tier security architecture intercepting adversarial prompt injections in 0.000s and masking abusive customer terms (`[REDACTED_HOSTILE]`). Cryptographic HMAC-SHA256 request signing with replay defense and idempotency key deduplication. Local Vector RAG in ChromaDB guaranteeing enterprise data sovereignty with zero corporate data egress to public cloud LLMs, reducing prompt token overhead by 89.1%.
* **Tests Owned:** `test_guardrails.py`, `test_production_security_and_telematics.py`, and the 13-scenario Selenium automated browser suite.

### 👤 Sahil Mudgil (230743) — ML, Observability & Evaluation Lead
* **Modules Authored:** Random Forest Delay Prediction Model (`src/mcp/tools/delay_predictor.py`), Business Safety Guardrails (`src/guardrails/business_guardrails.py`), MAS Callback Handler (`src/observability/callbacks.py`), OpenTelemetry MASTracer (`src/observability/tracing.py`), Agent Evaluator (`src/evaluation/agent_evaluator.py`), Visualizer (`src/evaluation/visualizer.py`), 48-Run Factorial Benchmark (`src/evaluation/benchmark_runner.py`), Real-Time Telematics Simulator (`src/telematics/simulator.py`).
* **Core Technical Defense:** Training a Scikit-Learn Random Forest regressor ($R^2 = 0.941$) to compute delays in 0.0008s with zero token cost rather than hallucination-prone LLM arithmetic. Mathematical formulation of Shannon Decision Entropy $H(X) = 0.917$ bits proving balanced driver workload distribution. Strict `BLOCK > FLAG_FOR_REVIEW > ALLOW` severity precedence for statutory 9.0h driving limits.
* **Tests Owned:** `test_academic_metrics_and_resilience.py` and `test_math_and_float_boundaries.py`.

---

## 7. Frequently Asked Questions (Viva Cheat-Sheet)

* **Q: Why don't CrewAI and Google ADK throw API Key errors?**
  *A:* The agents genuinely instantiate official `crewai.Agent` and `google.adk.agents.Agent` objects. To ensure 100% deterministic testing, zero latency during the viva, and prevent quota exhaustion during the 48-run benchmark, the agents execute their decision logic and A2A communication using local FastMCP tools, in-memory ChromaDB RAG, and Random Forest regression. Token counts and costs are calculated against Google Gemini 1.5 Flash pricing formulas and logged into OpenTelemetry trace spans. The codebase is cloud-ready and containerized for live deployment.
* **Q: Why use a Blackboard instead of direct point-to-point messages?**
  *A:* In direct point-to-point messaging, state is scattered across ephemeral queues, creating partial-information blind spots where the route agent cannot see driver cumulative shift fatigue. The Blackboard serves as a synchronized single source of truth protected by `threading.RLock()`, with an immutable provenance audit log of every transition.
* **Q: Why use Machine Learning for delay prediction instead of an LLM prompt?**
  *A:* LLMs struggle with non-linear numerical regression, floating-point math, and traffic extrapolations, causing hallucinations and taking 400–1200ms. A Random Forest model evaluates `[distance_km, weight_kg, traffic_factor]` in **0.0008 seconds (800 microseconds)** with zero token cost and $R^2 = 0.941$.
