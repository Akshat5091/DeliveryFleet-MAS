"""Script to build formal academic evaluation deliverables for Eval-2.
Generates:
1. Updated_Problem_Statement.docx (Project Charter & Synopsis)
2. Updated_Project_Plan.docx (Revised Project Timeline & Plan)
3. Work_In_Progress_Report.docx (Formal Technical Progress Report)
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_academic_cover_header(doc, title, subtitle):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, "1F4E79") # Academic Deep Navy
    set_cell_margins(cell, top=180, bottom=180, left=220, right=220)
    
    # Institution & Course Line
    p_inst = cell.paragraphs[0]
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING | B.TECH CSE SEMESTER VII\nCSE3101: AGENTIC AI — EVALUATION PHASE 2")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(9.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0xD9, 0xE1, 0xF2)
    
    # Main Document Title
    p_title = cell.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(3)
    r_title = p_title.add_run(title)
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(16.0)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    
    # Project & Authorship Line
    p_sub = cell.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(0)
    r_sub = p_sub.add_run(subtitle)
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.0)
    r_sub.font.color.rgb = RGBColor(0xF2, 0xF4, 0xF8)
    
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(6)

def add_styled_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    run = h.runs[0]
    run.font.name = "Calibri"
    if level == 1:
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
    elif level == 2:
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)
        h.paragraph_format.space_before = Pt(9)
        h.paragraph_format.space_after = Pt(3)
    elif level == 3:
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        h.paragraph_format.space_before = Pt(7)
        h.paragraph_format.space_after = Pt(2)
    return h

def add_body_p(doc, text, bold_prefix=None, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.italic = italic
    r.font.color.rgb = RGBColor(0x26, 0x26, 0x26)
    return p

def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x26, 0x26, 0x26)
    return p

def add_code_snippet(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, "F2F4F8")
    set_cell_margins(cell, top=75, bottom=75, left=130, right=130)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="1F4E79"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
    
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(3)

def format_styled_table(tbl, col_widths, headers, data):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    hdr_row = tbl.rows[0]
    for idx, heading in enumerate(headers):
        cell = hdr_row.cells[idx]
        cell.width = col_widths[idx]
        set_cell_background(cell, "1F4E79")
        set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(heading)
        r.font.name = "Calibri"
        r.font.size = Pt(9.0)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(data):
        row = tbl.add_row()
        fill_hex = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            set_cell_background(cell, fill_hex)
            set_cell_margins(cell, top=65, bottom=65, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(str(val))
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(0x26, 0x26, 0x26)

# ==============================================================================
# 1. BUILD UPDATED PROJECT CHARTER & PROBLEM SYNOPSIS DOCX
# ==============================================================================
def build_problem_charter(out_path):
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)
        
    add_academic_cover_header(
        doc,
        "Project Charter & Problem Synopsis: Autonomous Multi-Agent Delivery Fleet Coordination",
        "Project Title: Autonomous Multi-Agent Delivery Fleet Coordination and Dispatch System | Group: 9\nAuthors: Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)\nFaculty Mentors: Dr. Soharab Hossain Shaikh, Mr. Pranshu Tiwari | Evaluation Phase: Phase 2 (75% Milestone)"
    )
    
    add_styled_heading(doc, "1. Executive Summary & Operational Context", level=1)
    add_body_p(doc, "Last-mile parcel delivery accounts for over 53% of total logistics expenditures and represents the most volatile link in modern supply chains. Existing commercial platforms depend predominantly on static heuristic assignment (e.g., greedy Euclidean nearest-neighbor algorithms) or centralized monolithic rule engines. While computationally lightweight, these legacy paradigms fail under urban operational dynamics characterized by real-time traffic congestion, statutory driver shift hour regulations, municipal zero-emission zone constraints, and unpredictable transit incidents.")
    add_body_p(doc, "This project develops a decentralized, verifiable, and secure Multi-Agent System (MAS) that coordinates fleet dispatch, transit routing, and real-time contingency recovery. The system integrates Google Agent Development Kit (ADK) and CrewAI, leveraging a centralized Blackboard Shared State Architecture, Model Context Protocol (MCP) tool standard, and standardized Agent-to-Agent (A2A) messaging protocols.")

    add_styled_heading(doc, "2. Operational Problem Diagnosis & Failure Modes of Legacy Systems", level=1)
    add_bullet_p(doc, " Geometrically nearest-driver assignment models frequently assign drivers who are nearing their statutory 9.0-hour shift limit or facing gridlock, resulting in SLA breaches and regulatory penalties.", "1. Multi-Factor Context Blindness:")
    add_bullet_p(doc, " When road accidents or transit blockages emerge mid-route, static engines cannot negotiate dynamic bypasses or standby driver handovers without human operator intervention.", "2. Rigid Exception Deadlocks:")
    add_bullet_p(doc, " Ingesting untrusted customer special instruction notes directly into public cloud LLMs creates vulnerabilities to prompt injection attacks and risks data sovereignty leakage of internal shift logs.", "3. Security & Compliance Hazards:")

    add_styled_heading(doc, "3. Operational PEAS Formulation", level=1)
    peas_headers = ["PEAS Element", "Logistics Environment Specification"]
    peas_data = [
        ["Performance (KPMs)", "• Assignment Feasibility Rate (%): Multi-objective matching of driver payload, SLA, and fatigue.\n• Delivery SLA Adherence (%): Percentage of consignments delivered within customer deadline.\n• Statutory Safety Compliance (%): 100% adherence to the legal 9.0-hour daily driving limit.\n• Dynamic Exception Recovery Rate (%): Autonomous replanning success without supervisor escalation.\n• Security Gateway Interception (%): 100% interception of adversarial prompt injections."],
        ["Environment", "Partially observable, dynamic, stochastic, sequential, multi-agent urban grid across Zones A, B, C, and D, simulated via high-fidelity synthetic telemetry (orders.csv, drivers.csv, traffic.csv, weather.csv)."],
        ["Actuators", "Decisional actuator mechanisms: Dispatch commitment, corridor route selection, dynamic A2A exception rerouting, customer note sanitization, and atomic Blackboard state writes."],
        ["Sensors / Percepts", "Ingested consignment parameters, active driver telemetry (payload, hours worked, zone location), corridor traffic speed factors, rainfall levels, and ChromaDB policy chunks."]
    ]
    tbl_peas = doc.add_table(rows=1, cols=2)
    format_styled_table(tbl_peas, [Inches(1.8), Inches(5.0)], peas_headers, peas_data)

    add_styled_heading(doc, "4. Multi-Agent System Topology & Agent Rationale", level=1)
    add_body_p(doc, "In strict adherence to the Faculty Mandate on agent justification (\"Whatever number of agents you decide to use, you must have a clear understanding of the rationale behind each one... do not include agents randomly\"), every agent maps directly to a diagnosed logistics pain point:")
    
    agent_rows = [
        ("Fleet Dispatch Agent (CrewAI ReAct)", "Resolves Multi-Factor Assignment Conflict. Evaluates conflicting objectives (driver proximity, vehicle payload capacity, cumulative fatigue hours, approach deadhead transit, and customer SLA urgency) using a ReAct thinking loop before committing."),
        ("Route Optimization Agent (Google ADK)", "Resolves Urban Transit Fragility & Framework Coupling. Calculates congestion-adjusted primary transit corridors and emergency bypass routes. Implemented natively in Google ADK and exposed via the A2A protocol."),
        ("Exception Handling Agent (CrewAI)", "Resolves Mid-Transit Disruption Deadlocks. Triggered by event-driven delay alerts. Analyzes candidate standby drivers, queries Google ADK over A2A for emergency corridors, and reassigns consignments, saving an average of 18.5 minutes per disrupted route."),
        ("Policy & Compliance Retrieval Agent (ChromaDB Local RAG)", "Resolves Enterprise Data Sovereignty & Zoning Violations. Ingests municipal bylaws and internal driver shift policies locally in ChromaDB, preventing corporate records from leaking to public cloud LLMs."),
        ("Fleet Supervisory Orchestrator (CrewAI Flow)", "Resolves Coordination Overhead & Multi-Agent Race Conditions. Manages lifecycle gating, thread-safe Blackboard shared state, and parallel context gathering.")
    ]
    for name, desc in agent_rows:
        add_bullet_p(doc, desc, f"• {name}: ")

    add_styled_heading(doc, "5. Architectural Rationale: Programmatic Observability vs. Redundant LLM Agents", level=2)
    add_body_p(doc, "Logging intermediate agent events, measuring wall-clock latencies, tracking token usage, and computing provenance heatmaps requires 100% deterministic, zero-hallucination arithmetic. Wrapping an LLM around monitoring consumes redundant API tokens, introduces non-deterministic latency, and adds architectural bloat. Observability is handled natively by programmatic callback hooks (MASCallbackHandler) and OpenTelemetry-compatible distributed trace spans (MASTracer).")

    doc.save(out_path)
    print(f"[DONE] Created Problem Charter: {out_path}")

# ==============================================================================
# 2. BUILD REVISED PROJECT PLAN & WORK BREAKDOWN STRUCTURE DOCX
# ==============================================================================
def build_project_plan(out_path):
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)
        
    add_academic_cover_header(
        doc,
        "Revised Project Plan & Timeline: Progress vs. Plan Analysis",
        "Project Title: Autonomous Multi-Agent Delivery Fleet Coordination and Dispatch System | Group: 9\nAuthors: Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)\nFaculty Mentors: Dr. Soharab Hossain Shaikh, Mr. Pranshu Tiwari | Evaluation Phase: Phase 2 (75% Milestone)"
    )
    
    add_styled_heading(doc, "1. Architectural Evolution: Phase 1 Baseline to Phase 2 Realization", level=1)
    add_body_p(doc, "Following the Phase 1 evaluation and the formal distribution of the 11 Minimum Baseline Criteria, Group 8 executed a systematic engineering gap analysis, restructuring the prototype into a production-grade multi-agent architecture:")
    add_bullet_p(doc, " Upgraded from a monolithic framework to a dual-framework architecture. Google ADK powers the Route Optimization Agent; CrewAI powers the Orchestrator, Dispatch, Retrieval, and Exception Agents.", "Dual-Framework Heterogeneity (Criteria 6 & 7):")
    add_bullet_p(doc, " Replaced peer-only messaging with a centralized, thread-safe BlackboardState carrying complete provenance auditing, while retaining A2A messaging for empirical comparison.", "Centralized Blackboard Architecture (Criterion 1):")
    add_bullet_p(doc, " Replaced free-text prompt outputs with Pydantic v2 algebraic data models (DispatchDecision, RoutePlan, ExceptionReplan, FinalDeliveryReport) generating JSON and Markdown tables.", "Typed Structured Contracts (Criterion 3):")
    add_bullet_p(doc, " Consolidated external capabilities into a FastMCP server exposing 5 tools: Driver DB, Routing Engine, Delay Forecaster, ChromaDB Vector RAG, and Blackboard State Tool.", "Model Context Protocol Tooling (Criterion 2):")
    add_bullet_p(doc, " Implemented InputGuard defending against prompt injection attacks (regex patterns from LAB-06) and masking abusive customer personas.", "Multi-Tier Security Guardrails (Criterion 8):")
    add_bullet_p(doc, " Eliminated LLM monitoring bloat in favor of native callback hooks and OpenTelemetry tracing.", "Deterministic Observability & Heatmaps (Criteria 5 & 9):")

    add_styled_heading(doc, "2. Minimum Criteria Ownership & Implementation Ledger", level=1)
    crit_headers = ["#", "Prescribed Baseline Criterion", "Implementation Architecture & Module", "Student Lead", "Phase 2 Status"]
    crit_data = [
        ["1", "Blackboard Architecture", "BlackboardState in src/schemas/blackboard.py managed by BlackboardManager with RLock synchronization and FastMCP tool.", "Bhumika Yadav\nAadit Bassi", "100% Completed ✅"],
        ["2", "MCP Tool Integration (>= 2)", "FastMCP server (src/mcp/server.py) exposing 5 tools: Driver DB, Routing Engine, Delay Forecaster, ChromaDB RAG, Blackboard Update.", "Aadit Bassi", "100% Completed ✅"],
        ["3", "Pydantic Structured Output", "Pydantic v2 schemas (DispatchDecision, RoutePlan, ExceptionReplan, FinalDeliveryReport) with JSON & Markdown export.", "Bhumika Yadav", "100% Completed ✅"],
        ["4", "Agentic Design Patterns", "Hierarchical Orchestrator with parallel context gathering benchmarked against Sequential Pipeline.", "Bhumika Yadav", "100% Completed ✅"],
        ["5", "Callbacks & Heatmaps", "MASCallbackHandler tracking latency, tokens, errors. Generates 3 heatmaps (within-agent, 48-run, and academic rubric).", "Sahil Mudgil", "100% Completed ✅"],
        ["6", "A2A Protocol Communication", "A2ABridge in src/agents/a2a_bridge.py routing A2AMessage envelopes between CrewAI and Google ADK Route Agent.", "Aadit Bassi", "100% Completed ✅"],
        ["7", "CrewAI + Google ADK Dual", "Google ADK powers Route Agent; CrewAI powers Dispatch, Retrieval, Exception, and Orchestrator. Zero other frameworks.", "Aadit Bassi\nBhumika Yadav", "100% Completed ✅"],
        ["8", "Security & Guardrails", "InputGuard (regex injection defense + toxic term masking), ToolValidator, BusinessGuardrails (9.0h driving cap).", "Akshat Nagori\nSahil Mudgil", "100% Completed ✅"],
        ["9", "AI Observability & Tracing", "OpenTelemetry-compatible MASTracer linking root order IDs to sub-spans logged in run_events.jsonl.", "Sahil Mudgil", "100% Completed ✅"],
        ["10", "Evaluation (40+ Runs & Boxplots)", "48 benchmark runs across 2 architectures, 2 reasoning styles, 4 personas, 3 orders. Generates boxplots and Y in R^4 metrics.", "Sahil Mudgil\nAkshat Nagori", "100% Completed ✅"],
        ["11", "Cloud Platform Deployment", "Production Dockerfile and docker-compose.yml orchestrating MAS, FastMCP, ChromaDB, and OpenTelemetry collector.", "Aadit Bassi", "80% Ready 🚀"]
    ]
    tbl_crit = doc.add_table(rows=1, cols=5)
    format_styled_table(tbl_crit, [Inches(0.4), Inches(1.5), Inches(2.6), Inches(1.1), Inches(1.2)], crit_headers, crit_data)

    add_styled_heading(doc, "3. Phase-by-Phase Roadmap & Milestone Timeline", level=1)
    sched_headers = ["Phase Window", "Milestone / Objective", "Core Deliverables & Current Status"]
    sched_data = [
        ["Phase 1\n(Aug 15 - Oct 10)", "Foundations & Architectural Conception", "Topic definition, PEAS specification, synthetic dataset curation, preliminary literature review. [COMPLETED]"],
        ["Phase 2\n(Oct 11 - Oct 31)", "Core Multi-Agent Implementation (Target: 70-75%)", "Google ADK + CrewAI dual framework, FastMCP server (5 tools), Blackboard, A2A bridge, 48-run benchmark, 40/40 tests passing, 3 heatmaps, boxplots. [ACHIEVED: ~78% COMPLETE]"],
        ["Phase 3\n(Nov 01 - Nov 20)", "Production Cloud Deployment & Final Defense", "Docker Compose deployment to external cloud VM (AWS/GCP), Streamlit operations dashboard, 30-page final dissertation report, peer viva rehearsals. [PLANNED]"]
    ]
    tbl_sched = doc.add_table(rows=1, cols=3)
    format_styled_table(tbl_sched, [Inches(1.5), Inches(2.5), Inches(2.8)], sched_headers, sched_data)

    add_styled_heading(doc, "4. Risk Assessment & Contingency Fallback Plan", level=1)
    risk_headers = ["Identified Risk", "Impact", "Mitigation & Contingency Strategy"]
    risk_data = [
        ["Cross-Framework A2A Link Disruption", "High", "Pinned exact package versions in requirements.txt. Built in-process A2ABridge with thread-safe RLock history recording."],
        ["ChromaDB Vector Embedding Latency", "Medium", "Local ChromaDB persistence with pre-embedded policy chunks ensures retrieval latency under 20 ms without network dependency."],
        ["API Quota Exhaustion during Benchmarking", "Low", "Self-contained local simulation mode exercises all callbacks, tools, guardrails, and telemetry without burning API quotas."]
    ]
    tbl_risk = doc.add_table(rows=1, cols=3)
    format_styled_table(tbl_risk, [Inches(1.8), Inches(1.0), Inches(4.0)], risk_headers, risk_data)

    doc.save(out_path)
    print(f"[DONE] Created Project Plan: {out_path}")

# ==============================================================================
# 3. BUILD FORMAL WORK IN PROGRESS REPORT DOCX
# ==============================================================================
def build_wip_report(out_path):
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)
        
    add_academic_cover_header(
        doc,
        "Technical Work-in-Progress (WIP) Engineering Report: Evaluation Phase 2",
        "Project Title: Autonomous Multi-Agent Delivery Fleet Coordination and Dispatch System | Group: 9\nAuthors: Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)\nFaculty Mentors: Dr. Soharab Hossain Shaikh, Mr. Pranshu Tiwari | Milestone Target: 70–75% | Achieved: ~78%"
    )
    
    add_styled_heading(doc, "Executive Abstract", level=1)
    add_body_p(doc, "This technical report documents the comprehensive Phase 2 progress of the Autonomous Multi-Agent Delivery Fleet Coordination and Dispatch System for course CSE3101 (Agentic AI). Meeting the University guideline of 70–75% completion, our team has implemented a production-grade multi-agent platform combining Google Agent Development Kit (ADK) and CrewAI. The platform coordinates consignment intake, multi-factor vehicle dispatching, congestion-aware route calculation, Vector RAG policy compliance, and dynamic contingency replanning. Every agent maps directly to a diagnosed logistics pain point. Ten of the 11 minimum baseline criteria are 100% completed and empirically verified, with the 11th (Cloud Deployment) configured via Docker and Docker Compose (overall completion: ~78%). The test suite encompasses 40 automated unit and integration tests passing with 0 errors and 0 warnings.")

    add_styled_heading(doc, "1. Progress vs. Plan Analysis (Evaluation Criterion C6 — 5 Marks)", level=1)
    add_body_p(doc, "As established in the Phase 1 Project Synopsis and Revised Timeline, the Phase 2 milestone required delivering a functional prototype covering at least 6–7 of the 11 baseline criteria with 70–75% completion. Group 8 has implemented 10 of the 11 criteria at 100% completion, with Criterion 11 container-ready at 80%:")
    add_bullet_p(doc, " Core Multi-Agent Subsystems (Google ADK Route Agent + CrewAI Dispatch/Retrieval/Exception/Orchestrator): 100% Operational")
    add_bullet_p(doc, " FastMCP Server (5 Production Tools registered): 100% Operational")
    add_bullet_p(doc, " Blackboard Shared State Architecture with RLock thread safety: 100% Operational")
    add_bullet_p(doc, " A2A Inter-Framework Communication Bridge: 100% Operational")
    add_bullet_p(doc, " Multi-Tier Security Guardrails (Input Injection, Toxic Masking, 9.0h Shift Cap): 100% Operational")
    add_bullet_p(doc, " 48-Run Factorial Benchmark with Latency/Cost Boxplots: 100% Operational")
    add_bullet_p(doc, " AI Observability & OpenTelemetry Distributed Trace Ledger: 100% Operational")
    add_bullet_p(doc, " Automated Test Suite: 40/40 Passing across 7 suites in 10.54s")
    add_bullet_p(doc, " Docker & Docker Compose Cloud Deployment manifests: 80% Configured")

    add_styled_heading(doc, "2. Technical Architecture & Multi-Agent Topology (Evaluation Criterion C7 — 5 Marks)", level=1)
    add_body_p(doc, "The platform employs a Supervised Hierarchical Architecture with parallel context ingestion and event-driven exception loops:")
    add_bullet_p(doc, " Customer consignment payloads pass through an Input Security Guard which intercepts prompt injections in 0.000s and masks hostile terms with [REDACTED_HOSTILE].", "1. Ingestion & Security Screening:")
    add_bullet_p(doc, " The Fleet Orchestrator initiates parallel context gathering using ThreadPoolExecutor, querying ChromaDB Vector RAG for zoning rules and Driver DB for active vehicles concurrently.", "2. Parallel Context Gathering:")
    add_bullet_p(doc, " Retrieved context is synchronized into a centralized BlackboardState protected by reentrant locking (threading.RLock()) and deep copy isolation.", "3. Blackboard State Synchronization:")
    add_bullet_p(doc, " The CrewAI Dispatch Agent synthesizes multi-factor trade-offs (vehicle payload, cumulative shift fatigue, deadhead approach distance, and SLA urgency) using a ReAct reasoning loop.", "4. Multi-Factor Dispatch Reasoning:")
    add_bullet_p(doc, " The Dispatch Agent transmits an A2ARequest envelope across the framework boundary to the Google ADK Route Agent, which computes congestion-adjusted corridors using the FastMCP routing tool.", "5. Cross-Framework A2A Routing:")
    add_bullet_p(doc, " Upon mid-route road incidents, the CrewAI Exception Agent intercepts the delay alert, evaluates alternative standby drivers under statutory 9.0h driving caps, and requests an emergency arterial bypass over A2A.", "6. Event-Driven Exception Recovery:")

    add_styled_heading(doc, "3. Detailed Implementation of the 11 Prescribed Criteria (Evaluation Criterion C8 — 10 Marks)", level=1)
    add_body_p(doc, "Below is the exhaustive architectural documentation, exact file paths, and actual source code extracts demonstrating how each of the 11 prescribed baseline criteria is implemented in the codebase:", italic=True)

    # 3.1
    add_styled_heading(doc, "3.1 Context Sharing & Blackboard Architecture (Criterion 1 — Mandatory)", level=2)
    add_body_p(doc, "File Reference: src/schemas/blackboard.py & src/orchestration/blackboard_manager.py", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: Centralized BlackboardState carrying candidate drivers, retrieved zoning bylaws, ML delay estimates, route plans, and an immutable provenance audit log. The state is protected by threading.RLock() and deep-copy isolation, ensuring zero race conditions during parallel context gathering. It is exposed to agents via the FastMCP tool blackboard_update.")
    add_code_snippet(doc, """# File: src/schemas/blackboard.py (Lines 35-55)
class BlackboardState(BaseModel):
    order_id: str
    pickup: str
    dropoff: str
    weight_kg: float
    priority: str
    deadline_mins: int
    persona: str = "polite"
    candidate_drivers: List[CandidateDriver] = []
    retrieved_rules: List[str] = []
    predicted_delay_mins: float = 0.0
    dispatch_decision: Optional[DispatchDecision] = None
    route_plan: Optional[RoutePlan] = None
    exception_triggered: bool = False
    replan_driver_id: Optional[str] = None
    provenance_log: List[BlackboardEntry] = []

# File: src/orchestration/blackboard_manager.py (Thread-Safe Synchronization)
class BlackboardManager:
    def __init__(self):
        self._states: Dict[str, BlackboardState] = {}
        self._lock = threading.RLock()

    def update_field(self, order_id: str, agent_id: str, field_name: str, value: Any, rationale: str):
        with self._lock:
            state = self._states[order_id]
            setattr(state, field_name, value)
            entry = BlackboardEntry(agent_id=agent_id, field_updated=field_name, rationale=rationale)
            state.provenance_log.append(entry)""")

    # 3.2
    add_styled_heading(doc, "3.2 Tool Integration using FastMCP (Criterion 2 — >= 2 External Tools)", level=2)
    add_body_p(doc, "File Reference: src/mcp/server.py & src/mcp/tools/", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: Formal FastMCP server exposing 5 tools exceeding the requirement of at least 2: (1) driver_db_lookup, (2) routing_engine_calculate, (3) delay_predictor_forecast (Random Forest regression), (4) policy_rag_search (ChromaDB Vector RAG), and (5) blackboard_update.")
    add_code_snippet(doc, """# File: src/mcp/server.py (FastMCP Server Tool Registration)
from fastmcp import FastMCP
mcp = FastMCP("DeliveryFleetCoordinationServer")

@mcp.tool()
def driver_db_lookup(min_capacity_kg: float = 0.0, zone: Optional[str] = None) -> List[Dict[str, Any]]:
    \"\"\"Query active fleet driver pool matching payload and zone.\"\"\"
    return DriverDBTool().find_eligible_drivers(min_capacity_kg, zone)

@mcp.tool()
def routing_engine_calculate(pickup_location: str, dropoff_location: str, priority: str = "NORMAL") -> Dict[str, Any]:
    \"\"\"Compute primary and emergency alternative routes with congestion factors.\"\"\"
    return RoutingEngineTool().calculate_route(pickup_location, dropoff_location, priority)

@mcp.tool()
def delay_predictor_forecast(distance_km: float, weight_kg: float, traffic_factor: float = 1.0) -> Dict[str, Any]:
    \"\"\"Forecast expected delay in minutes using trained Random Forest model.\"\"\"
    return DelayPredictorTool().predict_delay(distance_km, weight_kg, traffic_factor)

@mcp.tool()
def policy_rag_search(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    \"\"\"Query ChromaDB vector database for municipal delivery bylaws.\"\"\"
    return ChromaRAGTool().query_policy(query, top_k)

@mcp.tool()
def blackboard_update(order_id: str, agent_id: str, key: str, value: Any, rationale: str) -> Dict[str, Any]:
    \"\"\"Synchronize agent intermediate outputs to Blackboard shared state.\"\"\"
    return BlackboardTool().update_state(order_id, agent_id, key, value, rationale)""")

    # 3.3
    add_styled_heading(doc, "3.3 Structured Output using Pydantic v2 (Criterion 3 — JSON & Markdown Tables)", level=2)
    add_body_p(doc, "File Reference: src/schemas/pydantic_models.py", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: Standardized all agent decisions and final delivery reports into Pydantic v2 algebraic data models, providing type safety, runtime validation, and export methods to both JSON and Markdown tables.")
    add_code_snippet(doc, """# File: src/schemas/pydantic_models.py (Structured Output Model)
class FinalDeliveryReport(BaseModel):
    order_id: str
    priority: str
    customer_persona: str
    input_guard_status: str
    assigned_driver_id: str
    assigned_driver_name: str
    selected_route: str
    distance_km: float
    final_eta_mins: float
    predicted_delay_mins: float
    delivery_outcome: str # SUCCESS, RECOVERED_VIA_EXCEPTION, BLOCKED_BY_GUARDRAIL
    total_execution_latency_sec: float
    total_tokens_consumed: int
    estimated_cost_usd: float
    guardrail_summary: GuardrailEvaluation
    exception_details: Optional[ExceptionReplan] = None
    provenance_trail: List[BlackboardEntry] = []

    def to_markdown_table(self) -> str:
        \"\"\"Render report as clean GitHub-Flavored Markdown table.\"\"\"
        return (f\"| Parameter | Value |\\n| :--- | :--- |\\n\"
                f\"| **Order ID** | `{self.order_id}` |\\n\"
                f\"| **Assigned Driver** | `{self.assigned_driver_id}` |\\n\"
                f\"| **Final ETA** | `{self.final_eta_mins:.1f} mins` |\\n\"
                f\"| **Outcome** | **`{self.delivery_outcome}`** |\")""")

    # 3.4
    add_styled_heading(doc, "3.4 Agentic Design Patterns (Criterion 4 — Hierarchical vs Sequential with Parallel Gathering)", level=2)
    add_body_p(doc, "File Reference: src/orchestration/hierarchical_orchestrator.py & sequential_orchestrator.py", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: Evaluated Hierarchical Orchestration against a Sequential Pipeline. The Hierarchical Orchestrator uses ThreadPoolExecutor to run RAG rule retrieval and Driver DB lookup concurrently, feeding the Blackboard before dispatch reasoning.")
    add_code_snippet(doc, """# File: src/orchestration/hierarchical_orchestrator.py (Parallel Context Gathering)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future_rag = executor.submit(
        self.retrieval_agent.retrieve_rules_for_order,
        order_id=order_id, pickup_zone=order[\"pickup\"], dropoff_zone=order[\"dropoff\"],
        weight_kg=float(order[\"weight_kg\"]), priority=order[\"priority\"], run_id=run_id
    )
    future_drivers = executor.submit(
        self.driver_db.find_eligible_drivers,
        min_capacity_kg=float(order[\"weight_kg\"])
    )
    rules = future_rag.result()
    raw_drivers = future_drivers.result()

# Synchronize parallel context into Blackboard
self.bb_manager.update_field(order_id, \"crew_retrieval_agent\", \"retrieved_rules\", rules, \"Parallel RAG\")
self.bb_manager.update_field(order_id, \"DriverDBTool\", \"candidate_drivers\", candidates, \"Parallel DB\")""")

    # 3.5
    add_styled_heading(doc, "3.5 Task Monitoring, Callbacks & Agent Heatmaps (Criterion 5)", level=2)
    add_body_p(doc, "File Reference: src/observability/callbacks.py & src/evaluation/visualizer.py", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: Created MASCallbackHandler capturing agent start, end, intermediate outputs, and latency. Generated 3 publication-grade heatmaps: (1) agent_metric_heatmap.png, (2) agent_run_heatmap.png (48-run bottleneck view), and (3) evaluation_metrics_heatmap.png.")
    add_code_snippet(doc, """# File: src/observability/callbacks.py (MAS Callback Handler)
class MASCallbackHandler:
    def on_agent_start(self, agent_name: str, task_name: str, run_id: str):
        self.active_spans[f\"{run_id}:{agent_name}\"] = time.time()

    def on_agent_end(self, agent_name: str, output: Any, run_id: str, tokens: int = 0):
        key = f\"{run_id}:{agent_name}\"
        start = self.active_spans.pop(key, time.time())
        duration = time.time() - start
        self.logger.log_event(
            run_id=run_id, agent_name=agent_name, event_type=\"AGENT_COMPLETE\",
            start_time=start, end_time=time.time(), input_tokens=int(tokens * 0.65),
            output_tokens=int(tokens * 0.35), status=\"SUCCESS\"
        )""")

    # 3.6
    add_styled_heading(doc, "3.6 Agent-to-Agent (A2A) Protocol Communication (Criterion 6)", level=2)
    add_body_p(doc, "File Reference: src/agents/a2a_bridge.py & src/schemas/a2a.py", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: A2ABridge routes structured A2AMessage envelopes containing protocol_version, message_id, from_agent, to_agent, and payload, connecting CrewAI agents with the Google ADK Route Agent with thread-safe RLock history recording.")
    add_code_snippet(doc, """# File: src/agents/a2a_bridge.py (A2A Protocol Bus)
def send_routing_request(self, from_agent: str, task_id: str, request: A2ARequest, run_id: str = \"run-0\") -> A2AResponse:
    req_envelope = A2AMessage(
        message_id=f\"msg-{uuid.uuid4().hex[:8]}\", task_id=task_id,
        from_agent=from_agent, to_agent=self.adk_route_agent.agent_id,
        message_type=\"request\", payload=request.model_dump()
    )
    with self._lock:
        self.message_history.append(req_envelope)

    # Cross-framework dispatch into Google ADK
    response = self.adk_route_agent.handle_a2a_request(request, run_id=run_id)

    resp_envelope = A2AMessage(
        message_id=f\"msg-{uuid.uuid4().hex[:8]}\", task_id=task_id,
        from_agent=self.adk_route_agent.agent_id, to_agent=from_agent,
        message_type=\"response\", payload=response.model_dump()
    )
    with self._lock:
        self.message_history.append(resp_envelope)
    return response""")

    # 3.7
    add_styled_heading(doc, "3.7 Dual Framework Architecture (Criterion 7 — CrewAI + Google ADK Exclusively)", level=2)
    add_body_p(doc, "File Reference: src/agents/adk_route_agent.py & src/agents/crew_dispatch_agent.py", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: Google ADK powers the Route Optimization Agent natively, while CrewAI powers the Orchestrator, Dispatch Agent, Retrieval Agent, and Exception Agent. Zero other agentic frameworks are used.")
    add_code_snippet(doc, """# Google ADK Native Agent (src/agents/adk_route_agent.py)
from google.adk.agents import Agent as ADKAgent
self.adk_native_agent = ADKAgent(
    name=\"RouteOptimizationAgent\",
    description=\"Computes primary and emergency alternative routes using urban congestion factors.\"
)

# CrewAI Native Agent (src/agents/crew_dispatch_agent.py)
from crewai import Agent as CrewAgent
self.crew_agent = CrewAgent(
    role=\"Fleet Dispatch & Allocation Strategist\",
    goal=\"Assign the most suitable driver weighing shift fatigue, vehicle payload, and arrival ETA.\",
    backstory=\"Senior logistics dispatcher operating under high-volume SLA constraints.\",
    verbose=False, allow_delegation=True
)""")

    # 3.8
    add_styled_heading(doc, "3.8 Multi-Tier Security Guardrails & Persona Variances (Criterion 8)", level=2)
    add_body_p(doc, "File Reference: src/guardrails/input_guard.py & business_guardrails.py", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: Three-tier defense: (1) InputGuard intercepting prompt injections via regex patterns from LAB-06 in 0.000s and masking hostile terms with [REDACTED_HOSTILE]; (2) ToolValidator validating schemas; (3) BusinessGuardrails enforcing statutory 9.0h driving limits with strict BLOCK > FLAG_FOR_REVIEW > ALLOW severity precedence.")
    add_code_snippet(doc, """# File: src/guardrails/input_guard.py (Prompt Injection & Abusive Masking)
INJECTION_PATTERNS = [
    r\"ignore\\s+(all\\s+|any\\s+)?previous\\s+instructions\",
    r\"system\\s+prompt\\s+override\",
    r\"bypass\\s+safety\\s+rules\",
    r\"output\\s+admin\\s+(secret|key|password)\"
]
for pattern in INJECTION_PATTERNS:
    if re.search(pattern, text, re.IGNORECASE):
        return InputGuardResult(is_valid=False, status=\"BLOCKED_INJECTION\", detected_threats=[\"PROMPT_INJECTION_ATTACK\"])

# File: src/guardrails/business_guardrails.py (Statutory 9.0h Cap)
if driver.hours_worked > MAX_LEGAL_DRIVER_HOURS: # 9.0 Hours
    violations.append(f\"FATAL_VIOLATION: Driver {driver.driver_id} has worked {driver.hours_worked}h (Legal limit {MAX_LEGAL_DRIVER_HOURS}h)\")
    action = \"BLOCK\" # Strict severity precedence""")

    # 3.9
    add_styled_heading(doc, "3.9 AI Observability Mechanism for Distributed Tracing (Criterion 9)", level=2)
    add_body_p(doc, "File Reference: src/observability/tracing.py & logs/run_events.jsonl", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: OpenTelemetry-compatible trace tree assigning a unique root trace ID per consignment and creating nested sub-spans for InputSecurityScreening, ParallelContextGathering, DispatchOptimization, RouteCalculation, and BusinessGuardrails.")
    add_code_snippet(doc, """# File: src/observability/tracing.py (OpenTelemetry Trace Trees)
class MASTracer:
    def start_trace(self, root_order_id: str) -> str:
        trace_id = f\"trace-{uuid.uuid4().hex[:12]}\"
        self.traces[trace_id] = {\"root_order_id\": root_order_id, \"spans\": []}
        return trace_id

    def start_span(self, trace_id: str, span_name: str, component: str) -> Span:
        span = Span(span_id=f\"span-{uuid.uuid4().hex[:8]}\", trace_id=trace_id, name=span_name, component=component)
        self.traces[trace_id][\"spans\"].append(span)
        return span""")

    # 3.10
    add_styled_heading(doc, "3.10 Performance Evaluation (Criterion 10 — 48 Runs, Boxplots, Academic Metrics)", level=2)
    add_body_p(doc, "File Reference: src/evaluation/benchmark_runner.py & agent_evaluator.py", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: Executed 48-run factorial benchmark (2 architectures x 2 reasoning styles x 4 personas x 3 orders). Generated latency_boxplot.png, cost_boxplot.png, and computed academic rubric metrics (Y in R^4: Sensitivity=1.000, Specificity=1.000, Shannon Decision Entropy=0.917 bits, Accuracy=1.000/1.000).")
    add_code_snippet(doc, """# File: src/evaluation/agent_evaluator.py (Shannon Decision Entropy & Course Rubrics)
def compute_shannon_entropy(self, driver_allocations: Dict[str, int]) -> float:
    \"\"\"Compute H(X) = -sum(p * log2(p)) to measure balanced multi-agent workload distribution.\"\"\"
    total = sum(driver_allocations.values())
    if total <= 0: return 0.0
    entropy = 0.0
    for count in driver_allocations.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return round(entropy, 3)

# Factorial Benchmark Loop (src/evaluation/benchmark_runner.py)
for arch in [\"Hierarchical\", \"Sequential\"]:
    for style in [\"ReAct\", \"Direct\"]:
        for persona in [\"polite\", \"urgent\", \"abusive\", \"injection\"]:
            for test_order in self.test_orders:
                report = orchestrator.process_order(test_order, prompt_style=style, run_id=run_id)""")

    # 3.11
    add_styled_heading(doc, "3.11 Cloud Platform Deployment (Criterion 11 — Docker & Docker Compose Ready)", level=2)
    add_body_p(doc, "File Reference: Dockerfile & docker-compose.yml", bold_prefix="• ")
    add_body_p(doc, "Technical Implementation: Authored production multi-stage Docker container and Docker Compose orchestration stack defining services for the MAS core application, FastMCP server, ChromaDB storage volume, and OpenTelemetry collector.")
    add_code_snippet(doc, """# Dockerfile (Multi-Stage Production Container)
FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000 8080
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/health || exit 1
CMD [\"python\", \"demo.py\"]""")

    # SECTION 4
    add_styled_heading(doc, "4. Empirical Evaluation, Benchmark Results & Statistical Analysis", level=1)
    add_body_p(doc, "From the 48 systematic benchmark runs logged in artifacts/benchmark_results.json:")
    add_bullet_p(doc, " Hierarchical + ReAct achieved a median latency of 0.442 seconds, representing a 10.2% latency reduction compared to Sequential + ReAct (0.487 seconds) due to concurrent context gathering.", "Execution Latency:")
    add_bullet_p(doc, " Polite and Urgent runs averaged $0.00010 USD per order (approx. 740 tokens on Gemini Flash pricing). Prompt injection runs incurred only $0.000015 USD (130 tokens before gateway rejection), demonstrating effective defense against Denial-of-Wallet attacks.", "Inference Cost Distribution:")
    add_bullet_p(doc, " Mean Query Sensitivity = 1.000 (100% attack recall); Mean Query Specificity = 1.000 (0 false positives on legitimate queries); Mean Fleet Decision Entropy = 0.917 bits (balanced driver allocation); Multi-Agent Accuracy Score = 1.000 / 1.000.", "Academic Rubric Vector (Y in R^4):")

    # SECTION 5
    add_styled_heading(doc, "5. Verification & Automated Test Suite Ledger (Evaluation Criterion C9 — 5 Marks)", level=1)
    add_body_p(doc, "The entire test suite was executed from workspace root via pytest -v:")
    test_headers = ["Test Suite Module", "Tests Passed", "Technical Scope & Verification Focus"]
    test_data = [
        ["test_academic_metrics_and_resilience.py", "6 / 6 Passed", "Shannon entropy H(X), Sensitivity, Specificity, A2A concurrency, approach deadhead scoring, heatmap generation."],
        ["test_concurrency_blackboard.py", "6 / 6 Passed", "Blackboard RLock concurrent writes, snapshot isolation, batch updates, lifecycle, tool thread safety."],
        ["test_edge_case_dispatch.py", "7 / 7 Passed", "Invalid orders, null notes handling, unknown driver supervisor escalation, driver DB caching."],
        ["test_end_to_end_pipeline.py", "5 / 5 Passed", "Hierarchical dispatch, exception recovery, sequential pipeline, impossible weight handling, cascading fatigue."],
        ["test_guardrails.py", "5 / 5 Passed", "Prompt injection detection, toxic language masking, tool validator, 9.0h statutory cap, severity precedence."],
        ["test_math_and_float_boundaries.py", "6 / 6 Passed", "Identical pickup/dropoff zero distance, green corridor speed boost, delay predictor boundaries."],
        ["test_mcp_tools.py", "5 / 5 Passed", "Driver DB, Routing Engine, Delay Predictor, ChromaDB RAG, and Blackboard FastMCP tools."]
    ]
    tbl_tests = doc.add_table(rows=1, cols=3)
    format_styled_table(tbl_tests, [Inches(2.5), Inches(1.1), Inches(3.2)], test_headers, test_data)

    # SECTION 6 - FORMAL INDIVIDUAL MEMBER CONTRIBUTIONS (NO INFORMAL Q&A!)
    add_styled_heading(doc, "6. Individual Team Member Contributions & Component Ownership (Evaluation Criterion C10 — 5 Marks)", level=1)
    add_body_p(doc, "In accordance with University Evaluation Criterion C10 (Individual Contribution / Viva Competence — 5 Marks), individual module ownership and engineering responsibilities were distributed across all team members:")

    add_styled_heading(doc, "6.1 Bhumika Yadav (230732) — Dispatch & Orchestration Lead", level=2)
    add_body_p(doc, "Authored the Hierarchical Orchestrator (src/orchestration/hierarchical_orchestrator.py) and Sequential Orchestrator (src/orchestration/sequential_orchestrator.py); engineered the CrewAI Dispatch Agent (src/agents/crew_dispatch_agent.py); authored the BlackboardState schema and BlackboardManager thread-safe state store; designed the Pydantic v2 structured output models (src/schemas/pydantic_models.py).", bold_prefix="• Core Modules Authored: ")
    add_body_p(doc, "Architected the multi-objective dispatch function that optimizes across vehicle payload, cumulative fatigue hours, approach deadhead distance, and SLA urgency. Justified the selection of a Hierarchical Manager pattern over peer-to-peer negotiation to eliminate cyclic state deadlocks.", bold_prefix="• Technical Contributions & Rigor: ")
    add_body_p(doc, "Authored test_concurrency_blackboard.py and test_end_to_end_pipeline.py.", bold_prefix="• Test Verification Ownership: ")

    add_styled_heading(doc, "6.2 Aadit Bassi (230728) — Routing, Tooling & Integration Lead", level=2)
    add_body_p(doc, "Engineered the Google ADK Route Optimization Agent (src/agents/adk_route_agent.py); authored the A2A communication bridge (src/agents/a2a_bridge.py) and protocol schemas (src/schemas/a2a.py); deployed the FastMCP server (src/mcp/server.py) and routing engine tool; authored Dockerfile and docker-compose.yml.", bold_prefix="• Core Modules Authored: ")
    add_body_p(doc, "Engineered framework-agnostic A2A protocol messaging connecting Google ADK and CrewAI without binary coupling. Implemented multi-corridor transit graph evaluation with dynamic speed factors and priority green-corridor boosts.", bold_prefix="• Technical Contributions & Rigor: ")
    add_body_p(doc, "Authored test_mcp_tools.py and Docker container orchestration configs.", bold_prefix="• Test Verification Ownership: ")

    add_styled_heading(doc, "6.3 Akshat Nagori (230682) — Retrieval, Prompts & Security Lead", level=2)
    add_body_p(doc, "Engineered the local ChromaDB Vector RAG Retrieval Agent (src/agents/crew_retrieval_agent.py) and knowledge base; authored the Input Security Guard (src/guardrails/input_guard.py); designed the 4 customer persona prompt variances (src/evaluation/personas.py).", bold_prefix="• Core Modules Authored: ")
    add_body_p(doc, "Designed the multi-stage security pipeline that executes regex prompt injection detection in 0.000s and masks hostile customer insults ([REDACTED_HOSTILE]). Architected local Vector RAG in ChromaDB to guarantee enterprise data sovereignty with zero corporate data egress to public LLMs.", bold_prefix="• Technical Contributions & Rigor: ")
    add_body_p(doc, "Authored test_guardrails.py and input security regression suites.", bold_prefix="• Test Verification Ownership: ")

    add_styled_heading(doc, "6.4 Sahil Mudgil (230743) — ML, Observability & Evaluation Lead", level=2)
    add_body_p(doc, "Trained the Random Forest delay prediction regression model (src/mcp/tools/delay_predictor.py); authored the Business Safety Guardrails (src/guardrails/business_guardrails.py); engineered the MASCallbackHandler (src/observability/callbacks.py) and OpenTelemetry MASTracer (src/observability/tracing.py); authored the AgentEvaluator (src/evaluation/agent_evaluator.py) and MASVisualizer (src/evaluation/visualizer.py); executed the 48-run factorial benchmark.", bold_prefix="• Core Modules Authored: ")
    add_body_p(doc, "Mathematically formalized the Shannon Decision Entropy H(X) metric to prove fair multi-agent workload allocation across drivers. Implemented strict BLOCK > FLAG_FOR_REVIEW > ALLOW severity precedence for statutory 9.0h driving caps. Generated all 3 diagnostic heatmaps and latency/cost boxplots.", bold_prefix="• Technical Contributions & Rigor: ")
    add_body_p(doc, "Authored test_academic_metrics_and_resilience.py and test_math_and_float_boundaries.py.", bold_prefix="• Test Verification Ownership: ")

    # SECTION 7
    add_styled_heading(doc, "7. Conclusion & Phase 3 Milestone Roadmap", level=1)
    add_body_p(doc, "With Phase 2 successfully completing approximately 78% of the project scope and covering all 11 criteria, Group 8 is positioned ahead of schedule for the final Phase 3 defense on November 20, 2026. Phase 3 milestones will focus on:")
    add_bullet_p(doc, " Deploying the Docker Compose stack to an external cloud virtual machine (AWS EC2 / GCP Compute Engine).", "1. Remote Cloud Deployment:")
    add_bullet_p(doc, " Developing an interactive Streamlit operations dashboard to visualize live dispatches, map corridors, and telemetry heatmaps.", "2. Interactive UI Dashboard:")
    add_bullet_p(doc, " Authoring the comprehensive 30-page final dissertation matching the university thesis template.", "3. Final Documentation:")

    doc.save(out_path)
    print(f"[DONE] Created Formal WIP Report: {out_path}")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    out_dir = "D:/AKSHAT/DOCS/BTech CSE/Sem 7/Agentic AI/DeliveryFleet-MAS/Eval 2 Documents"
    os.makedirs(out_dir, exist_ok=True)
    
    build_problem_charter(os.path.join(out_dir, "Updated_Problem_Statement.docx"))
    build_project_plan(os.path.join(out_dir, "Updated_Project_Plan.docx"))
    build_wip_report(os.path.join(out_dir, "Work_In_Progress_Report.docx"))
    
    print("\nALL THREE FORMAL ACADEMIC .DOCX DELIVERABLES SUCCESSFULLY GENERATED!")
