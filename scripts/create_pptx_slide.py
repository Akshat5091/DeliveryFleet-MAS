"""Generates the official 1-Slide Presentation on Criteria Coverage for Eval-2.
Maps exactly 8 completed criteria (Eval-2 core prototype, ~73% completion) and 3 Phase 3 novelty criteria (End-Term scope).
File: DeliveryFleet-MAS/Eval 2 Documents/1_Slide_Coverage_Matrix_Group8.pptx
"""
import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUT_PPTX = Path(r"D:\AKSHAT\DOCS\BTech CSE\Sem 7\Agentic AI\DeliveryFleet-MAS\Eval 2 Documents\CSE-IV_Group-8_1_Slide_Coverage_Matrix_Group8.pptx")
OUT_MD = Path(r"D:\AKSHAT\DOCS\BTech CSE\Sem 7\Agentic AI\DeliveryFleet-MAS\Eval 2 Documents\Markdown Sources\EVAL2_1_SLIDE_COVERAGE_MATRIX.md")

COLOR_CRIMSON = RGBColor(153, 27, 27)    # #991B1B Academic Crimson
COLOR_BLACK = RGBColor(17, 24, 39)       # #111827 Pitch Black
COLOR_CHARCOAL = RGBColor(31, 41, 55)    # #1F2937 Dark Charcoal
COLOR_MUTED = RGBColor(75, 85, 99)       # #4B5563 Muted Gray
COLOR_GREEN = RGBColor(22, 101, 52)      # #166534 Forest Green
COLOR_BORDER = RGBColor(209, 213, 219)   # #D1D5DB Pencil Border
COLOR_CARD_BG = RGBColor(249, 250, 251)  # #F9FAFB Card Background

CRITERIA_DATA = [
    ("C01", "Blackboard Shared State", "VERIFIED", "100% VERIFIED", "Centralized BlackboardState in src/schemas/blackboard.py (lines 35-55) with RLock concurrency synchronization, FastMCP update tool, and read-driven downstream handoffs via bb_manager.get_field (lines 56-63). [WIP Report: Chapter 3.1 & Section 4.3]"),
    ("C02", "MCP Tool Integration (>= 2)", "VERIFIED", "100% VERIFIED", "FastMCP server (src/mcp/server.py, lines 23-45) and native MCPClient (src/mcp/client.py, lines 15-40) exposing 5 tools with formal client session calls and schema validation. Exceeds >= 2 requirement by 150%. [WIP Report: Chapter 3.2 & Section 4.4]"),
    ("C03", "Pydantic Structured Output", "VERIFIED", "100% VERIFIED", "Pydantic v2 schemas: FinalDeliveryReport (src/schemas/reports.py, lines 20-45) and DispatchDecision / RoutePlan / ExceptionReplan (src/schemas/decisions.py, lines 15-45) with validated JSON export and Markdown tables. [WIP Report: Chapter 3.3]"),
    ("C04", "Agentic Design Patterns", "VERIFIED", "100% VERIFIED", "Supervised Hierarchical Manager MAS pattern with parallel context gathering via ThreadPoolExecutor (src/orchestration/hierarchical_orchestrator.py, lines 154-172) benchmarked against Sequential Pipeline. [WIP Report: Chapter 3.4 & Section 4.2]"),
    ("C05", "Callbacks & Latency Heatmaps", "VERIFIED", "100% VERIFIED", "MASCallbackHandler in src/observability/callbacks.py capturing real-time lifecycle hooks (on_agent_start/end/exception). Generated 2D density heatmaps across 72 factorial runs. [WIP Report: Chapter 3.5 & Section 4.8]"),
    ("C06", "A2A Protocol Communication", "VERIFIED", "100% VERIFIED", "A2ABridge in src/agents/a2a_bridge.py (lines 74-114) routing A2AMessage envelopes with live network JSON-RPC endpoint (POST /api/a2a/route) and in-process fallback circuit breaker. [WIP Report: Chapter 3.6 & Section 4.1]"),
    ("C07", "Dual Framework (CrewAI + ADK)", "VERIFIED", "100% VERIFIED", "Google ADK natively powers Route Agent (src/agents/adk_route_agent.py, lines 32-45); CrewAI natively powers Dispatch Agent (src/agents/crew_dispatch_agent.py, lines 40-55), Retrieval, and Exception Agents. [WIP Report: Chapter 3.7 & Section 4.1]"),
    ("C08", "Security & Multi-Tier Guardrails", "VERIFIED", "100% VERIFIED", "InputGuard regex injection defense in 0.0004s + toxic term masking (src/guardrails/input_guard.py, lines 20-45) and BusinessGuardrails statutory 9.0h driving limit block (src/guardrails/business_guardrails.py, lines 18-38). [WIP Report: Chapter 3.8 & Section 4.7]"),
    ("C09", "AI Observability & Tracing", "NOVELTY", "END-TERM NOVELTY", "Local JSONL trace spans operational. Multi-host OpenTelemetry Collector export to Jaeger/Prometheus distributed tracing dashboard reserved for End-Term Defense novelty. [WIP Report: Chapter 9.1 & Section 4.8]"),
    ("C10", "Evaluation (Cloud Factorial Matrix)", "NOVELTY", "END-TERM NOVELTY", "Baseline 72 factorial runs complete locally. Full 100+ factorial cloud evaluation matrix across 3 architectures with Pareto cost-latency frontiers reserved for End-Term Defense novelty. [WIP Report: Chapter 9.2 & Section 5.0]"),
    ("C11", "Cloud Platform Deployment", "NOVELTY", "END-TERM NOVELTY", "Local multi-stage Docker container configured. Live production deployment to AWS EC2 / GCP Compute Engine with Cloudflare edge proxy reserved for End-Term Defense novelty. [WIP Report: Chapter 9.3 & Section 9.3]")
]

def create_coverage_slide():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # 1. Top Header Banner Box
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.25), Inches(12.533), Inches(0.95))
    banner.fill.solid()
    banner.fill.fore_color.rgb = COLOR_CARD_BG
    banner.line.color.rgb = COLOR_CRIMSON
    banner.line.width = Pt(1.5)

    tf = banner.text_frame
    tf.word_wrap = True
    tf.margin_top = Inches(0.06)
    tf.margin_bottom = Inches(0.06)
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)

    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.LEFT
    r0 = p0.add_run()
    r0.text = "Autonomous Multi-Agent Delivery Fleet System — Eval-2 Criteria Coverage Matrix"
    r0.font.name = "Calibri"
    r0.font.size = Pt(15.0)
    r0.font.bold = True
    r0.font.color.rgb = COLOR_BLACK

    p1 = tf.add_paragraph()
    p1.alignment = PP_ALIGN.LEFT
    r1 = p1.add_run()
    r1.text = "Course: CSE3101 Agentic AI | Group 8: Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)"
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.0)
    r1.font.color.rgb = COLOR_MUTED

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.LEFT
    r2 = p2.add_run()
    r2.text = "Milestone Target: 65–70% | Achieved: ~73% Complete  —  [ 8 Core Baseline Criteria 100% Verified   |  3 Advanced Research Criteria Reserved for End-Term Novelty  ]"
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.0)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_CRIMSON

    # 2. Dual KPI Status Badges
    # Left Badge: 8 Covered
    b_left = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(1.28), Inches(6.15), Inches(0.42))
    b_left.fill.solid()
    b_left.fill.fore_color.rgb = RGBColor(0xEC, 0xFD, 0xF5) # Emerald 50
    b_left.line.color.rgb = RGBColor(0x16, 0x65, 0x34) # Emerald 800
    b_left.line.width = Pt(1.2)
    tf_l = b_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_top = Inches(0.04)
    tf_l.margin_left = Inches(0.12)
    p_l = tf_l.paragraphs[0]
    p_l.alignment = PP_ALIGN.CENTER
    r_l = p_l.add_run()
    r_l.text = " 8 EVAL-2 VERIFIED CRITERIA (100% Complete — 49/49 Pytest & 13/13 Selenium Passing)"
    r_l.font.name = "Calibri"
    r_l.font.size = Pt(8.5)
    r_l.font.bold = True
    r_l.font.color.rgb = COLOR_GREEN

    # Right Badge: 3 Novelty
    b_right = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.783), Inches(1.28), Inches(6.15), Inches(0.42))
    b_right.fill.solid()
    b_right.fill.fore_color.rgb = COLOR_CARD_BG
    b_right.line.color.rgb = COLOR_CRIMSON
    b_right.line.width = Pt(1.2)
    tf_r = b_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_top = Inches(0.04)
    tf_r.margin_left = Inches(0.12)
    p_r = tf_r.paragraphs[0]
    p_r.alignment = PP_ALIGN.CENTER
    r_r = p_r.add_run()
    r_r.text = " 3 PHASE-3 RESEARCH NOVELTIES (Strategically Staged for End-Term Defense on Nov 20)"
    r_r.font.name = "Calibri"
    r_r.font.size = Pt(8.5)
    r_r.font.bold = True
    r_r.font.color.rgb = COLOR_CRIMSON

    # 3. Coverage Matrix Table (11 Criteria + Header)
    rows = 12
    cols = 4
    left = Inches(0.4)
    top = Inches(1.78)
    width = Inches(12.533)
    height = Inches(5.05)

    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    tbl = table_shape.table
    tbl.columns[0].width = Inches(1.0)
    tbl.columns[1].width = Inches(2.2)
    tbl.columns[2].width = Inches(1.8)
    tbl.columns[3].width = Inches(7.533)

    headers = ["# & Status", "Evaluation Criterion (Prescribed Baseline)", "Phase 2 Coverage Status", "Technical Implementation in Working Prototype & WIP Report Section Link"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0x0F, 0x17, 0x2A) # Deep Navy Header
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if i in (0, 2) else PP_ALIGN.LEFT
        r = p.add_run()
        r.text = h
        r.font.name = "Calibri"
        r.font.size = Pt(9.0)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (num, name, c_type, status_text, details) in enumerate(CRITERIA_DATA, start=1):
        is_verified = (c_type == "VERIFIED")
        
        # Row background tint
        if is_verified:
            row_bg = RGBColor(0xFA, 0xFD, 0xFA) if row_idx % 2 == 1 else RGBColor(0xF0, 0xFD, 0xF4)
            status_bg = RGBColor(0xD1, 0xFA, 0xE5) # Emerald 100
            status_fg = RGBColor(0x06, 0x5F, 0x46) # Emerald 800
            badge_icon = f"{num} []"
        else:
            row_bg = RGBColor(0xF8, 0xFA, 0xFC) if row_idx % 2 == 1 else RGBColor(0xF0, 0xF9, 0xFF)
            status_bg = RGBColor(0xDB, 0xEA, 0xFE) # Blue 100
            status_fg = RGBColor(0x1E, 0x40, 0xAF) # Blue 800
            badge_icon = f"{num} []"

        # Cell 0: ID & Badge
        c0 = tbl.cell(row_idx, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = row_bg
        c0.vertical_anchor = MSO_ANCHOR.MIDDLE
        p0 = c0.text_frame.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        r0 = p0.add_run()
        r0.text = badge_icon
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.0)
        r0.font.bold = True
        r0.font.color.rgb = status_fg

        # Cell 1: Criterion Name
        c1 = tbl.cell(row_idx, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = row_bg
        c1.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = c1.text_frame.paragraphs[0]
        p1.alignment = PP_ALIGN.LEFT
        r1 = p1.add_run()
        r1.text = name
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.0)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        # Cell 2: Status Tag
        c2 = tbl.cell(row_idx, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = status_bg
        c2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p2 = c2.text_frame.paragraphs[0]
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = status_text
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.0)
        r2.font.bold = True
        r2.font.color.rgb = status_fg

        # Cell 3: Details
        c3 = tbl.cell(row_idx, 3)
        c3.fill.solid()
        c3.fill.fore_color.rgb = row_bg
        c3.vertical_anchor = MSO_ANCHOR.MIDDLE
        p3 = c3.text_frame.paragraphs[0]
        p3.alignment = PP_ALIGN.LEFT
        r3 = p3.add_run()
        r3.text = details
        r3.font.name = "Calibri"
        r3.font.size = Pt(7.5)
        r3.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # 4. Bottom Footer Banner
    footer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(6.92), Inches(12.533), Inches(0.35))
    footer.fill.solid()
    footer.fill.fore_color.rgb = RGBColor(0xF1, 0xF5, 0xF9) # Slate 100
    footer.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
    footer.line.width = Pt(1.0)

    tf_foot = footer.text_frame
    tf_foot.word_wrap = True
    tf_foot.margin_top = Inches(0.04)
    p_foot = tf_foot.paragraphs[0]
    p_foot.alignment = PP_ALIGN.CENTER
    r_foot = p_foot.add_run()
    r_foot.text = "Empirical Validation: 49/49 Pytest Tests Passing (9 Suites) | 13/13 Selenium Browser UI Scenarios Passing | Repository: Akshat5091/DeliveryFleet-MAS (Group 8)"
    r_foot.font.name = "Calibri"
    r_foot.font.size = Pt(7.5)
    r_foot.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    prs.save(str(OUT_PPTX))
    print(f"[DONE] Created 1-Slide Presentation: {OUT_PPTX.name}")

def sync_markdown_coverage():
    lines = [
        "# Autonomous Multi-Agent Delivery Fleet Coordination & Dispatch System",
        "## Evaluation Phase 2: One-Slide Criteria Coverage Matrix",
        "**Course:** CSE3101: Agentic AI — B.Tech CSE Semester VII",
        "**Group Number:** 8",
        "**Team Members:** Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)",
        "**Milestone Achievement:** ~73% Complete (8 of 11 Criteria 100% Verified for Eval-2 | 3 Reserved for End-Term Novelty)",
        "",
        "---",
        "",
        "### Summary Indicators:",
        "* ** 8 EVAL-2 VERIFIED CRITERIA (100% Complete):** C01, C02, C03, C04, C05, C06, C07, C08 — Supported by 49/49 Pytest unit tests, 13/13 Selenium browser scenarios, and 72/72 factorial benchmark runs.",
        "* ** 3 PHASE-3 RESEARCH NOVELTIES:** C09, C10, C11 — Strategically reserved as advanced research scope for the final End-Term defense on November 20, 2026.",
        "",
        "---",
        "",
        "### Phase 2 Evaluation Criteria Coverage & Link to Work-in-Progress (WIP) Report",
        "",
        "| # & Status | Prescribed Baseline Criterion | Phase 2 Coverage Status | Technical Implementation in Working Prototype & WIP Report Section Link |",
        "| :---: | :--- | :---: | :--- |"
    ]
    for num, name, c_type, status_text, details in CRITERIA_DATA:
        badge = f"**{num} [{'' if c_type == 'VERIFIED' else ''}]**"
        formatted_details = details.replace("[WIP Report:", "**[WIP Report:").replace("]", "]**")
        lines.append(f"| {badge} | **{name}** | **{status_text}** | {formatted_details} |")
    lines.extend([
        "",
        "---",
        "",
        "*Note: The corresponding PowerPoint 16:9 widescreen presentation slides are available at `Eval 2 Documents/1_Slide_Coverage_Matrix_Group8.pptx` (clean coverage matrix deck) and `Eval 2 Documents/DeliveryFleet_MAS_Evaluation2_Master_Presentation.pptx` (Slides 20 & 22).*  ",
        "*Empirical Verification: 49/49 Pytest Tests Passing | 13/13 Selenium Browser UI Tests Passing | 72/72 Factorial Benchmark Runs Completed | GitHub: Akshat5091/DeliveryFleet-MAS (Group 8)*"
    ])
    OUT_MD.write_text("\n".join(lines).strip(), encoding="utf-8")
    print(f"[DONE] Created Markdown Coverage Matrix: {OUT_MD}")

if __name__ == "__main__":
    create_coverage_slide()
    sync_markdown_coverage()
