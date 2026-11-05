"""Script to build formal academic evaluation deliverables for Eval-2.
Generates:
1. Updated_Problem_Statement.docx (Project Charter & Problem Formulation)
2. Updated_Project_Plan.docx (Revised Project Timeline & Criteria Ownership Plan)
"""
import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

COLOR_CRIMSON = RGBColor(153, 27, 27)    # #991B1B Academic Crimson
COLOR_BLACK = RGBColor(17, 24, 39)       # #111827 Pitch Black
COLOR_CHARCOAL = RGBColor(31, 41, 55)    # #1F2937 Dark Charcoal
COLOR_MUTED = RGBColor(75, 85, 99)       # #4B5563 Muted Gray
COLOR_GREEN = RGBColor(22, 101, 52)      # #166534 Forest Green
COLOR_BORDER = "D1D5DB"                  # Pencil Border
COLOR_CARD_BG = "F9FAFB"                 # Light Background

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
    set_cell_background(cell, COLOR_CARD_BG)
    set_cell_margins(cell, top=160, bottom=160, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="36" w:space="0" w:color="991B1B"/>'
        f'<w:top w:val="single" w:sz="8" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'<w:right w:val="single" w:sz="8" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    # Institution & Course Line
    p_inst = cell.paragraphs[0]
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(3)
    p_inst.paragraph_format.line_spacing = 1.15
    r_inst = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING | B.TECH CSE SEMESTER VII\nCSE3101: AGENTIC ARTIFICIAL INTELLIGENCE — EVALUATION PHASE 2")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(9.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_CRIMSON
    
    # Main Document Title
    p_title = cell.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run(title)
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(15.0)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_BLACK
    
    # Project & Authorship Line
    p_sub = cell.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(0)
    p_sub.paragraph_format.line_spacing = 1.15
    r_sub = p_sub.add_run(subtitle)
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.0)
    r_sub.font.color.rgb = COLOR_CHARCOAL
    
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
        run.font.color.rgb = COLOR_BLACK
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
    elif level == 2:
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_CRIMSON
        h.paragraph_format.space_before = Pt(9)
        h.paragraph_format.space_after = Pt(3)
    elif level == 3:
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_CHARCOAL
        h.paragraph_format.space_before = Pt(7)
        h.paragraph_format.space_after = Pt(2)
    return h

def add_body_p(doc, text, bold_prefix=None, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_CRIMSON
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.italic = italic
    r.font.color.rgb = COLOR_CHARCOAL
    return p

def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_CRIMSON
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.color.rgb = COLOR_CHARCOAL
    return p

def add_code_snippet(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, COLOR_CARD_BG)
    set_cell_margins(cell, top=75, bottom=75, left=130, right=130)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="991B1B"/>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = COLOR_BLACK
    
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

def format_styled_table(doc, tbl, col_widths, headers, data):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], "111827") # Pitch Black
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(h)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    # Data Rows
    for r_idx, row_data in enumerate(data):
        row = tbl.add_row()
        fill_hex = "FFFFFF" if r_idx % 2 == 0 else "F9FAFB"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            set_cell_background(cell, fill_hex)
            set_cell_margins(cell, top=70, bottom=70, left=110, right=110)
            
            # Subtle pencil border
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{COLOR_BORDER}"/>'
                f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{COLOR_BORDER}"/>'
                f'<w:left w:val="single" w:sz="4" w:space="0" w:color="{COLOR_BORDER}"/>'
                f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{COLOR_BORDER}"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)
            
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.10
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(9.0)
            run.font.color.rgb = COLOR_CHARCOAL

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(6)

def add_callout_box(doc, text, title="ACADEMIC NOTE & EMPIRICAL PROOF", fill_hex=COLOR_CARD_BG, border_hex="991B1B"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    r_t = p.add_run(f"📌 {title}: ")
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(9.5)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_CRIMSON
    
    r_b = p.add_run(text)
    r_b.font.name = "Calibri"
    r_b.font.size = Pt(9.5)
    r_b.font.color.rgb = COLOR_CHARCOAL
    
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

# ==============================================================================
# 1. BUILD UPDATED PROBLEM STATEMENT DOCX
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
        "Project Charter & Updated Problem Formulation: Autonomous Multi-Agent Delivery Fleet Coordination",
        "Project Title: Autonomous Multi-Agent Delivery Fleet Coordination and Dispatch System | Group: 8\nAuthors: Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)\nFaculty Mentors: Dr. Soharab Hossain Shaikh, Mr. Pranshu Tiwari | Evaluation Phase: Phase 2 (~73% Milestone: 8 Core Modules Completed)"
    )
    
    add_styled_heading(doc, "1. Executive Summary & Operational Context", level=1)
    add_body_p(doc, "Last-mile parcel delivery accounts for over 53% of total logistics expenditures and represents the most volatile, error-prone link in contemporary supply chain management. Urban delivery operations take place under continuous environmental stochasticity, governed by fluctuating arterial congestion, statutory driver shift hour ceilings, municipal low-emission zoning bylaws, and unexpected transit incidents. Conventional commercial logistics software depends almost exclusively on static heuristic assignment (such as greedy Euclidean nearest-neighbor dispatching) or centralized, monolithic rule engines. While computationally lightweight, these legacy paradigms fail fundamentally under dynamic operational conditions.")
    add_body_p(doc, "This project develops a decentralized, verifiable, and secure Multi-Agent System (MAS) that coordinates fleet dispatch, transit routing, and real-time contingency recovery. The system integrates Google Agent Development Kit (ADK) and CrewAI, leveraging a centralized Blackboard Shared State Architecture, Model Context Protocol (FastMCP) tool integration, and standardized Agent-to-Agent (A2A) messaging protocols. In Phase 2, Group 8 has realized a fully operational working prototype covering 8 core modules with 100% test verification across 49 unit tests and 72 factorial benchmark runs, achieving ~73% completion against university criteria.")

    add_styled_heading(doc, "2. Operational Problem Diagnosis & Failure Modes of Conventional Engines", level=1)
    add_body_p(doc, "Empirical analysis of existing commercial logistics platforms reveals three fatal failure modes that motivate a decentralized Multi-Agent Architecture:")
    add_bullet_p(doc, "Geometrically nearest-driver assignment models evaluate only Euclidean proximity, neglecting cumulative driver fatigue hours, vehicle payload limits, approach deadhead transit delays, and customer SLA urgency. A driver who is 2 km away but trapped behind severe gridlock or nearing their legal 9.0-hour shift limit is frequently selected over an unencumbered driver 4 km away on an open arterial bypass.", "1. Multi-Factor Context Blindness:")
    add_bullet_p(doc, "When road accidents or transit blockages emerge mid-route, static engines cannot negotiate dynamic bypasses or standby driver handovers without human operator intervention, resulting in compounding delivery SLA violations and driver exhaustion.", "2. Rigid Exception Deadlocks:")
    add_bullet_p(doc, "Ingesting untrusted customer special instruction notes directly into public cloud LLMs creates vulnerabilities to prompt injection attacks and risks data sovereignty leakage of internal corporate shift logs and municipal zoning bylaws.", "3. Security & Compliance Hazards:")

    add_styled_heading(doc, "3. Operational PEAS Formulation", level=1)
    add_body_p(doc, "Following the standard Russell & Norvig Multi-Agent System formalization, the delivery fleet environment is modeled across four foundational dimensions:")
    peas_headers = ["PEAS Element", "Logistics Environment Specification"]
    peas_data = [
        ["Performance (KPMs)", "• Assignment Feasibility Rate (%): Multi-objective matching of driver payload, SLA, and fatigue.\n• Delivery SLA Adherence (%): Percentage of consignments delivered within customer deadline.\n• Statutory Safety Compliance (%): 100% adherence to the legal 9.0-hour daily driving limit.\n• Dynamic Exception Recovery Rate (%): Autonomous replanning success without supervisor escalation.\n• Security Gateway Interception (%): 100% interception of adversarial prompt injections (0.0004s latency)."],
        ["Environment", "Partially observable, dynamic, stochastic, sequential, multi-agent urban grid across Zones A, B, C, and D, simulated via high-fidelity synthetic telemetry (orders.csv, drivers.csv, traffic.csv, weather.csv, delivery_history.csv)."],
        ["Actuators", "Decisional actuator mechanisms: Dispatch commitment, corridor route selection, dynamic A2A exception rerouting, customer note sanitization, and atomic Blackboard state writes. (No physical mechanical actuation)."],
        ["Sensors / Percepts", "Ingested consignment parameters (weight, priority, deadline), active driver telemetry (GPS zone, vehicle payload capacity, cumulative hours worked), corridor traffic speed factors, rainfall precipitation readings, and Vector RAG policy chunks."]
    ]
    tbl_peas = doc.add_table(rows=1, cols=2)
    format_styled_table(doc, tbl_peas, [Inches(1.8), Inches(5.0)], peas_headers, peas_data)

    add_styled_heading(doc, "4. Strict Architectural Justification: Pain Points vs. Multi-Agent Rationale", level=1)
    add_callout_box(
        doc,
        "\"Whatever number of agents you decide to use in your Agentic AI system, you must have a clear understanding of the rationale behind each one. You should be able to explain the purpose of every agent and the specific problem it is designed to address. Do not include agents randomly just to make your system appear more advanced or complex.\" — Faculty Evaluation Mandate",
        title="FACULTY EVALUATION MANDATE ON AGENT JUSTIFICATION"
    )
    add_body_p(doc, "In strict adherence to this mandate, every single agent in our system maps directly to an identifiable, non-trivial operational pain point. We categorically reject arbitrary agent proliferation. The table below delineates the exact operational alignment:")

    align_headers = ["Operational Pain Point", "Resolving MAS Agent", "Underlying Architectural Mechanism"]
    align_data = [
        ["Multi-Factor Dispatch Conflict\n(Capacity, fatigue, traffic, deadlines)", "Fleet Dispatch Agent\n(CrewAI ReAct)", "Synthesizes multi-factor trade-offs using a ReAct thinking loop before committing driver assignment."],
        ["Dynamic Urban Route Congestion\n(Corridor delays, arterial routing)", "Route Optimization Agent\n(Google ADK)", "Calculates Dijkstra corridors and ML traffic delays using declarative AgentCards over A2A."],
        ["Mid-Route Incidents & Blockages\n(Accidents, vehicle breakdowns)", "Dynamic Exception Agent\n(CrewAI Replan)", "Event-driven replanning: intercepts disruptions, reassigns standby drivers, updates Blackboard in <0.05s."],
        ["Data Sovereignty & Zoning Bylaws\n(Municipal EV zones, privacy)", "Policy Retrieval Agent\n(Local ChromaDB RAG)", "Local vector embeddings prevent corporate shift logs and zoning bylaws from leaking to cloud LLMs."],
        ["Coordination Overhead & Concurrency\n(Agent race conditions, lockouts)", "Fleet Supervisory Orchestrator\n(CrewAI Flow / Manager)", "Controls lifecycle gating, manages thread-safe Blackboard shared memory via threading.RLock()."]
    ]
    tbl_align = doc.add_table(rows=1, cols=3)
    format_styled_table(doc, tbl_align, [Inches(2.2), Inches(1.8), Inches(2.8)], align_headers, align_data)

    add_styled_heading(doc, "4.1 Fleet Supervisory Orchestrator (CrewAI Flow)", level=2)
    add_body_p(doc, "Implemented in src/orchestration/hierarchical_orchestrator.py. The Supervisory Orchestrator resolves coordination overhead and multi-agent race conditions. It governs the execution pipeline across three synchronized phases: (1) concurrent context gathering via ThreadPoolExecutor(max_workers=2) querying Driver DB and Vector RAG in parallel; (2) multi-factor dispatch reasoning and ADK route calculation; and (3) event-driven exception monitoring. It manages thread-safe Blackboard shared state under threading.RLock(), preventing race conditions during concurrent agent writes.")

    add_styled_heading(doc, "4.2 Fleet Dispatch Agent (CrewAI ReAct)", level=2)
    add_body_p(doc, "Implemented in src/agents/crew_dispatch_agent.py. Resolves multi-factor assignment conflict. Evaluates conflicting operational objectives (vehicle payload, driver shift hours, approach deadhead transit, customer SLA urgency) using a ReAct thinking loop before committing. Uses Driver DB, Policy RAG, and Blackboard tools, strictly enforcing vehicle weight capacity and statutory 9.0h driver fatigue limits.")

    add_styled_heading(doc, "4.3 Route Optimization Agent (Google ADK)", level=2)
    add_body_p(doc, "Implemented in src/agents/adk_route_agent.py. Resolves urban transit fragility and framework coupling. Built natively using Google Agent Development Kit (ADK) declarative AgentCard contracts, computing congestion-adjusted Dijkstra corridors and ML traffic delays. Exposed over the Agent-to-Agent (A2A) protocol via HTTP JSON-RPC 2.0 (/api/a2a/route) with circuit-breaker fallback.")

    add_styled_heading(doc, "4.4 Dynamic Exception Handling Agent (CrewAI)", level=2)
    add_body_p(doc, "Implemented in src/agents/crew_exception_agent.py. Resolves mid-transit disruption deadlocks. Triggered by event-driven delay alerts. Evaluates candidate standby drivers within proximity, queries Google ADK over A2A for emergency bypass corridors, and reassigns consignments in <0.05s, saving an average of 18.5 minutes per disrupted route.")

    add_styled_heading(doc, "4.5 Policy & Compliance Retrieval Agent (Local ChromaDB Vector RAG)", level=2)
    add_body_p(doc, "Implemented in src/agents/crew_retrieval_agent.py. Resolves enterprise data sovereignty and municipal zoning violations. Ingests municipal bylaws and internal driver shift policies locally in ChromaDB, preventing corporate records from leaking to public cloud LLMs while executing semantic vector searches in under 15ms.")

    add_styled_heading(doc, "5. Architectural Rationale: Programmatic Observability vs. Redundant LLM Agents", level=1)
    add_body_p(doc, "A critical senior engineering design decision made in Phase 2 was the complete rejection of an LLM-based 'Auditor/Monitoring Agent' in favor of high-frequency programmatic callback hooks and OpenTelemetry-compatible distributed trace spans:")
    add_bullet_p(doc, "Measuring execution timestamps, counting tokens, tracking HTTP status codes, and generating execution heatmaps requires 100% deterministic arithmetic. Wrapping an LLM around monitoring consumes redundant API tokens, introduces non-deterministic latency (400–1200ms per check), and risks hallucinated audit logs.", "1. Determinism vs. Hallucination Risk:")
    add_bullet_p(doc, "Our architecture handles observability natively via MASCallbackHandler (src/observability/callbacks.py) and MASTracer (src/observability/tracing.py), persisting every lifecycle hook to console, structured JSONL logs (logs/run_events.jsonl), and WebSockets in under 0.001s with zero token cost.", "2. Lightweight Telemetry Overhead:")

    add_styled_heading(doc, "6. Minimum Evaluation Criteria Mapping", level=1)
    add_body_p(doc, "The table below establishes the comprehensive mapping between university evaluation criteria, the operational problem statement, and the Phase 2 implementation:")
    crit_map_headers = ["#", "Prescribed Baseline Criterion", "Problem Addressed", "Phase 2 Implementation Status"]
    crit_map_data = [
        ["1", "Blackboard Shared State", "Shared context loss, race conditions, token bloat", "100% VERIFIED ✅ (BlackboardState, RLock, provenance log)"],
        ["2", "MCP Tool Integration (>= 2)", "Tight database coupling, brittle ad-hoc tools", "100% VERIFIED ✅ (5 FastMCP tools operational)"],
        ["3", "Pydantic Structured Output", "Free-text LLM hallucination, parser breakage", "100% VERIFIED ✅ (Pydantic v2 schemas: Report, Decision, Route)"],
        ["4", "Agentic Design Patterns", "Monolithic bottlenecks, inflexible execution", "100% VERIFIED ✅ (Hierarchical MAS vs. Sequential benchmarked)"],
        ["5", "Callbacks & Latency Heatmaps", "Silent failures, opaque execution latency", "100% VERIFIED ✅ (MASCallbackHandler, 2D density heatmap)"],
        ["6", "A2A Protocol Communication", "Framework silo isolation, proprietary lock-in", "100% VERIFIED ✅ (A2ABridge, JSON-RPC 2.0 over HTTP)"],
        ["7", "CrewAI + Google ADK Dual", "Single-framework vendor dependency", "100% VERIFIED ✅ (CrewAI ReAct + Google ADK AgentCards)"],
        ["8", "Security & Multi-Tier Guardrails", "Prompt injections, driver fatigue violations", "100% VERIFIED ✅ (InputGuard in 0.0004s + statutory 9.0h limit)"],
        ["9", "AI Observability & Tracing", "Multi-host distributed span correlation", "Phase 3 Novelty 🚀 (OpenTelemetry Collector + Jaeger APM)"],
        ["10", "Cloud Factorial Matrix & Pareto", "Cloud-scale multi-objective trade-off frontiers", "Phase 3 Novelty 🚀 (100+ factorial cloud runs)"],
        ["11", "Cloud Platform Deployment", "Remote production hosting & SSL termination", "Phase 3 Novelty 🚀 (Docker Compose on AWS EC2 / GCP)"]
    ]
    tbl_crit_map = doc.add_table(rows=1, cols=4)
    format_styled_table(doc, tbl_crit_map, [Inches(0.4), Inches(2.0), Inches(2.4), Inches(2.0)], crit_map_headers, crit_map_data)

    doc.save(out_path)
    print(f"[DONE] Created Problem Charter: {out_path}")

# ==============================================================================
# 2. BUILD REVISED PROJECT PLAN DOCX
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
        "Project Title: Autonomous Multi-Agent Delivery Fleet Coordination and Dispatch System | Group: 8\nAuthors: Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)\nFaculty Mentors: Dr. Soharab Hossain Shaikh, Mr. Pranshu Tiwari | Evaluation Phase: Phase 2 (~73% Milestone: 8 Core Modules Completed)"
    )
    
    add_styled_heading(doc, "1. Executive Context & Phase 1 to Phase 2 Architectural Evolution", level=1)
    add_body_p(doc, "Following the Phase 1 evaluation and the formal distribution of the 11 Minimum Baseline Criteria, Group 8 executed a systematic engineering gap analysis, restructuring the prototype into a production-grade multi-agent architecture:")
    add_bullet_p(doc, "Upgraded from a monolithic framework to a dual-framework architecture. Google ADK powers the Route Optimization Agent; CrewAI powers the Orchestrator, Dispatch, Retrieval, and Exception Agents.", "Dual-Framework Heterogeneity (Criteria 6 & 7):")
    add_bullet_p(doc, "Replaced peer-only messaging with a centralized, thread-safe BlackboardState carrying complete provenance auditing, while retaining A2A messaging for empirical comparison.", "Centralized Blackboard Architecture (Criterion 1):")
    add_bullet_p(doc, "Replaced free-text prompt outputs with Pydantic v2 algebraic data models (DispatchDecision, RoutePlan, ExceptionReplan, FinalDeliveryReport) generating JSON and Markdown tables.", "Typed Structured Contracts (Criterion 3):")
    add_bullet_p(doc, "Consolidated external capabilities into a FastMCP server exposing 5 tools: Driver DB, Routing Engine, Delay Forecaster, ChromaDB Vector RAG, and Blackboard State Tool.", "Model Context Protocol Tooling (Criterion 2):")
    add_bullet_p(doc, "Implemented MASCallbackHandler streaming real-time lifecycle events to console, JSONL, and WebSockets, generating 2D density heatmaps across 72 factorial runs.", "Lifecycle Callbacks & Latency Heatmaps (Criterion 5):")
    add_bullet_p(doc, "Implemented InputGuard defending against prompt injection attacks (regex patterns from LAB-06) and masking abusive customer personas.", "Multi-Tier Security Guardrails (Criterion 8):")
    add_bullet_p(doc, "Eliminated LLM monitoring bloat in favor of native callback hooks and OpenTelemetry tracing.", "Deterministic Observability & Heatmaps (Criteria 5 & 9):")

    add_styled_heading(doc, "2. Minimum Criteria Ownership & Implementation Ledger", level=1)
    add_body_p(doc, "Below is the detailed criteria ownership and source code reference ledger covering all 11 evaluation criteria:")
    crit_headers = ["#", "Prescribed Baseline Criterion", "Implementation Architecture & Module", "Student Lead", "Phase 2 Status"]
    crit_data = [
        ["1", "Blackboard Architecture", "BlackboardState in src/schemas/blackboard.py (lines 35-55) managed by BlackboardManager (lines 51-65) with RLock synchronization, FastMCP tool, and read-driven downstream handoffs.", "Bhumika Yadav\nAadit Bassi", "100% Completed (Phase 2 Verified ✅)"],
        ["2", "MCP Tool Integration (>= 2)", "FastMCP server (src/mcp/server.py, lines 23-45) and MCPClient (src/mcp/client.py, lines 15-40) exposing 5 tools with formal client session calls and schema validation.", "Aadit Bassi", "100% Completed (Phase 2 Verified ✅)"],
        ["3", "Pydantic Structured Output", "Pydantic v2 schemas: FinalDeliveryReport (src/schemas/reports.py, lines 20-45) and DispatchDecision (src/schemas/decisions.py, lines 15-45) with JSON & Markdown export.", "Bhumika Yadav", "100% Completed (Phase 2 Verified ✅)"],
        ["4", "Agentic Design Patterns", "Supervised Hierarchical Manager MAS pattern with parallel context gathering via ThreadPoolExecutor (src/orchestration/hierarchical_orchestrator.py, lines 154-172) vs Sequential Pipeline.", "Bhumika Yadav", "100% Completed (Phase 2 Verified ✅)"],
        ["5", "Callbacks & Latency Heatmaps", "MASCallbackHandler (src/observability/callbacks.py) capturing on_agent_start/end/exception in real time. Generated 2D density heatmaps across 72 factorial benchmark runs.", "Sahil Mudgil", "100% Completed (Phase 2 Verified ✅)"],
        ["6", "A2A Protocol Communication", "A2ABridge in src/agents/a2a_bridge.py (lines 74-114) routing A2AMessage envelopes between CrewAI and Google ADK Route Agent with live network JSON-RPC endpoint.", "Aadit Bassi", "100% Completed (Phase 2 Verified ✅)"],
        ["7", "CrewAI + Google ADK Dual", "Google ADK powers Route Agent (src/agents/adk_route_agent.py, lines 32-45); CrewAI powers Dispatch (src/agents/crew_dispatch_agent.py, lines 40-55), Retrieval, and Exception Agents.", "Aadit Bassi\nBhumika Yadav", "100% Completed (Phase 2 Verified ✅)"],
        ["8", "Security & Guardrails", "InputGuard regex injection defense in 0.0004s + toxic masking (src/guardrails/input_guard.py, lines 20-45) and BusinessGuardrails 9.0h driving cap (src/guardrails/business_guardrails.py, lines 18-38).", "Akshat Nagori\nSahil Mudgil", "100% Completed (Phase 2 Verified ✅)"],
        ["9", "AI Observability & Tracing", "Local JSONL trace spans operational. Multi-host OpenTelemetry Collector export to Jaeger dashboard reserved for End-Term novelty.", "Sahil Mudgil", "Phase 3 Novelty (End-Term Scope 🚀)"],
        ["10", "Cloud Factorial Matrix & Pareto", "Baseline 72 factorial runs operational. Cloud-scale 100+ factorial evaluation matrix across 3 architectures with Pareto frontier optimization reserved for End-Term novelty.", "Sahil Mudgil\nAkshat Nagori", "Phase 3 Novelty (End-Term Scope 🚀)"],
        ["11", "Cloud Platform Deployment", "Local multi-stage Docker container configured. Live production deployment to AWS EC2 / GCP Compute Engine with Cloudflare edge worker reserved for End-Term novelty.", "Aadit Bassi", "Phase 3 Novelty (End-Term Scope 🚀)"]
    ]
    tbl_crit = doc.add_table(rows=1, cols=5)
    format_styled_table(doc, tbl_crit, [Inches(0.4), Inches(1.5), Inches(2.6), Inches(1.1), Inches(1.2)], crit_headers, crit_data)

    add_styled_heading(doc, "3. Phase-by-Phase Roadmap & Milestone Timeline", level=1)
    sched_headers = ["Phase Window", "Milestone / Objective", "Core Deliverables & Current Status"]
    sched_data = [
        ["Phase 1\n(Aug 15 - Oct 10)", "Foundations & Architectural Conception", "Topic definition, PEAS specification, synthetic dataset curation, preliminary literature review. [COMPLETED]"],
        ["Phase 2\n(Oct 11 - Oct 31)", "Core Multi-Agent Working Prototype (Target: 65-70%)", "8 Core Baseline Criteria completed & empirically verified (Blackboard, FastMCP, Pydantic, Hierarchical MAS, Callbacks & Heatmaps, A2A, Dual CrewAI+ADK, Multi-Tier Guardrails), 49 unit/integration tests passing (100% green), 72 factorial runs. [ACHIEVED: ~73% COMPLETE]"],
        ["Phase 3\n(Nov 01 - Nov 20)", "Advanced Optimization, Cloud VM & End-Term Research Novelty", "OpenTelemetry Collector export to Jaeger dashboard, 100+ cloud factorial benchmark matrix across 3 architectures, remote cloud VM deployment on AWS EC2/GCP, 30-page final dissertation report, peer viva rehearsals. [PLANNED FOR FINAL DEFENSE]"]
    ]
    tbl_sched = doc.add_table(rows=1, cols=3)
    format_styled_table(doc, tbl_sched, [Inches(1.5), Inches(2.5), Inches(2.8)], sched_headers, sched_data)

    add_styled_heading(doc, "4. Detailed Bi-Weekly Sprint Execution Schedule", level=1)
    add_body_p(doc, "To ensure structured execution across the semester, development was tracked through seven distinct bi-weekly sprint windows:")
    sprint_headers = ["Sprint Window", "Milestone & Technical Objectives", "Deliverables & Artifacts", "Sprint Status"]
    sprint_data = [
        ["Oct 11 – Oct 18", "Infrastructure & Schemas", "Pydantic v2 schemas (BlackboardState, A2AMessage, FinalDeliveryReport); FastMCP server; synthetic datasets (orders.csv, drivers.csv, traffic.csv, delivery_history.csv).", "DONE ✅"],
        ["Oct 19 – Oct 24", "Agent Development & A2A", "Implement Google ADK Route Agent; CrewAI Dispatch & Retrieval Agents; A2A communication bridge; Random Forest delay predictor training (R^2 = 0.901).", "DONE ✅"],
        ["Oct 25 – Oct 29", "Guardrails & Orchestration", "InputGuard (injection defense + abusive masking); BusinessGuardrails (9.0h rule); Hierarchical Manager and Sequential Orchestrators; Exception recovery loop.", "DONE ✅"],
        ["Oct 30 – Oct 31", "Eval-2 Benchmark & Artifacts", "Execute 72-run factorial benchmark matrix; generate publication-quality boxplots and heatmaps; execute pytest suite (49/49 passing); author Eval-2 documentation.", "DONE ✅"],
        ["Nov 01 – Nov 08", "Production Cloud Containerization", "Docker Compose orchestration; health check endpoints; live cloud VM deployment; latency profiling under cloud network conditions.", "PLANNED ⏳"],
        ["Nov 09 – Nov 15", "UI Dashboard & Full Report", "Interactive Streamlit operations dashboard; comprehensive Phase 3 project report (approx. 25–30 pages) matching university thesis template.", "PLANNED ⏳"],
        ["Nov 16 – Nov 20", "Final Defense & Viva Readiness", "Peer cross-examination; code walkthrough rehearsals ensuring every member can modify and defend any component under evaluation.", "PLANNED ⏳"]
    ]
    tbl_sprint = doc.add_table(rows=1, cols=4)
    format_styled_table(doc, tbl_sprint, [Inches(1.3), Inches(1.8), Inches(2.7), Inches(1.0)], sprint_headers, sprint_data)

    add_styled_heading(doc, "5. Team Responsibility & Criteria Ownership Matrix", level=1)
    resp_headers = ["Student Name & ID", "Engineering Role", "Primary Module Ownership & Deliverables", "Criteria"]
    resp_data = [
        ["Bhumika Yadav\n(230732)", "Architecture Lead", "Blackboard state architecture (src/schemas/blackboard.py) and Pydantic v2 output models (src/schemas/reports.py, decisions.py); Hierarchical Orchestrator; concurrency tests.", "1, 3, 4, 7"],
        ["Aadit Bassi\n(230728)", "Multi-Agent Systems & Routing Lead", "Google ADK Route Agent (src/agents/adk_route_agent.py); A2A Protocol Bridge (src/agents/a2a_bridge.py); FastMCP server and tools; Docker configuration.", "1, 2, 6, 7, 11"],
        ["Akshat Nagori\n(230682)", "Security, Retrieval & Testing Lead", "InputGuard security (src/guardrails/input_guard.py); ChromaDB Vector RAG (src/mcp/tools/chroma_rag.py); web dashboard (src/web/); 13 Selenium automated browser tests.", "8, 10"],
        ["Sahil Mudgil\n(230743)", "Machine Learning & Observability Lead", "Random Forest delay model (src/mcp/tools/delay_predictor.py); BusinessGuardrails 9.0h shift limit; MASCallbackHandler; 72-run factorial benchmark runner.", "5, 8, 9, 10"]
    ]
    tbl_resp = doc.add_table(rows=1, cols=4)
    format_styled_table(doc, tbl_resp, [Inches(1.4), Inches(1.6), Inches(3.0), Inches(0.8)], resp_headers, resp_data)

    add_styled_heading(doc, "6. Risk Assessment & Contingency Fallback Plan", level=1)
    risk_headers = ["Identified Operational Risk", "Likelihood", "Impact", "Mitigation & Contingency Strategy"]
    risk_data = [
        ["Cross-Framework A2A Link Disruption", "Low", "High", "Pinned exact package versions in requirements.txt. Built in-process A2ABridge with thread-safe RLock history recording and HTTP JSON-RPC fallback."],
        ["ChromaDB Vector Embedding Latency", "Low", "Medium", "Local ChromaDB persistence with pre-embedded policy chunks ensures retrieval latency under 20 ms without network dependency."],
        ["Cloud VM CPU Bottleneck for Local LLM", "Medium", "Medium", "Quantized small model or lightweight embeddings selected; retrieval calls execute in parallel gathering step, hiding inference latency."],
        ["API Quota Exhaustion during Benchmarking", "Low", "Low", "Self-contained local simulation mode exercises all callbacks, tools, guardrails, and telemetry without burning API quotas."]
    ]
    tbl_risk = doc.add_table(rows=1, cols=4)
    format_styled_table(doc, tbl_risk, [Inches(1.8), Inches(0.8), Inches(0.8), Inches(3.4)], risk_headers, risk_data)

    doc.save(out_path)
    print(f"[DONE] Created Project Plan: {out_path}")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    out_dir = Path(r"D:\AKSHAT\DOCS\BTech CSE\Sem 7\Agentic AI\DeliveryFleet-MAS\Eval 2 Documents")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    build_problem_charter(out_dir / "Updated_Problem_Statement.docx")
    build_project_plan(out_dir / "Updated_Project_Plan.docx")
    
    print("\n[SUCCESS] Updated_Problem_Statement.docx & Updated_Project_Plan.docx successfully generated!")
