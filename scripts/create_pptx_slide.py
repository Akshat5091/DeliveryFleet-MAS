"""Generates the official 1-Slide Presentation on Criteria Coverage for Eval-2.
Maps all 11 criteria to implementation modules and exact WIP Report chapter headings.
File: DeliveryFleet-MAS/Eval 2 Documents/1_Slide_Coverage_Matrix_Group8.pptx
"""
import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUT_PPTX = Path(r"D:\AKSHAT\DOCS\BTech CSE\Sem 7\Agentic AI\DeliveryFleet-MAS\Eval 2 Documents\1_Slide_Coverage_Matrix_Group8.pptx")
OUT_MD = Path(r"D:\AKSHAT\DOCS\BTech CSE\Sem 7\Agentic AI\DeliveryFleet-MAS\Eval 2 Documents\EVAL2_1_SLIDE_COVERAGE_MATRIX.md")

CRITERIA_DATA = [
    ("1", "Blackboard Shared State", "COVERED (100%)", "Centralized BlackboardState in src/schemas/blackboard.py with RLock synchronization, FastMCP update tool, and read-driven downstream handoffs (bb_manager.get_field). [WIP Report: Chapter 3.1 & Section 4.3]"),
    ("2", "MCP Tool Integration (>= 2)", "COVERED (100%)", "FastMCP server (src/mcp/server.py) and native MCPClient (src/mcp/client.py) exposing 5 tools with formal client session calls and schema validation. Exceeds >= 2 requirement. [WIP Report: Chapter 3.2 & Section 4.4]"),
    ("3", "Pydantic Structured Output", "COVERED (100%)", "Pydantic v2 schemas: DispatchDecision, RoutePlan, ExceptionReplan, FinalDeliveryReport with validated JSON export and GitHub-flavored Markdown tables. [WIP Report: Chapter 3.3]"),
    ("4", "Agentic Design Patterns", "COVERED (100%)", "Tri-architecture evaluation: Supervised Hierarchical, standalone Parallel (4-way fan-out with barrier), and Sequential Pipeline benchmarked across 72 runs. [WIP Report: Chapter 3.4 & Section 4.2]"),
    ("5", "Callbacks & Agent Heatmaps", "COVERED (100%)", "MASCallbackHandler capturing empirical start, end, tokens, errors, and latency. 3 empirical heatmaps: within-agent metrics, 72-run density, and rubric heatmap (zero synthetic jitter). [WIP Report: Chapter 3.5 & Section 5.0]"),
    ("6", "A2A Protocol Communication", "COVERED (100%)", "A2ABridge in src/agents/a2a_bridge.py routing A2AMessage envelopes with live network JSON-RPC endpoint (POST /api/a2a/route) and in-process fallback circuit breaker. [WIP Report: Chapter 3.6 & Section 4.1]"),
    ("7", "Dual Framework (CrewAI + ADK)", "COVERED (100%)", "Google ADK natively powers Route Agent; CrewAI natively powers Orchestrators, Dispatch, Retrieval, and Exception Agents using formal Task and Crew execution graphs. [WIP Report: Chapter 3.7 & Section 4.1]"),
    ("8", "Security & Multi-Tier Guardrails", "COVERED (100%)", "InputGuard (regex injection defense from LAB-06 in 0.000s + toxic term masking), ToolValidator runtime checks, BusinessGuardrails (statutory 9.0h driving limit block). [WIP Report: Chapter 3.8, Section 4.7 & Section 6.0]"),
    ("9", "AI Observability & Tracing", "COVERED (100%)", "OpenTelemetry SDK (TracerProvider, SimpleSpanProcessor, InMemorySpanExporter) and persistent run_events.jsonl audit log. Microsecond precision without token bloat. [WIP Report: Chapter 3.9 & Section 4.8]"),
    ("10", "Evaluation (40+ Runs & Boxplots)", "COVERED (100%)", "72 systematic factorial benchmark runs across 3 architectures, 2 reasoning styles, 4 personas, 3 orders. Generated latency/cost boxplots + academic rubric (Y in R^4). [WIP Report: Chapter 3.10 & Section 5.0]"),
    ("11", "Cloud Platform Deployment", "READY (80%)", "Production multi-stage Dockerfile and docker-compose.yml orchestrating MAS core, FastMCP server, ChromaDB storage volume, and OpenTelemetry collector. [WIP Report: Chapter 3.11 & Section 9.0]")
]

def create_coverage_slide():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # 1. Top Banner Box
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.35), Inches(12.533), Inches(0.95))
    banner.fill.solid()
    banner.fill.fore_color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    banner.line.color.rgb = RGBColor(0x2E, 0x75, 0xB6)
    banner.line.width = Pt(1.5)

    tf = banner.text_frame
    tf.word_wrap = True
    tf.margin_top = Inches(0.08)
    tf.margin_bottom = Inches(0.08)
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)

    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.LEFT
    r0 = p0.add_run()
    r0.text = "Autonomous Multi-Agent Delivery Fleet System — Eval-2 Criteria Coverage Matrix"
    r0.font.name = "Calibri"
    r0.font.size = Pt(15.5)
    r0.font.bold = True
    r0.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    p1 = tf.add_paragraph()
    p1.alignment = PP_ALIGN.LEFT
    r1 = p1.add_run()
    r1.text = "Course: CSE3101 Agentic AI | Group 8: Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743) | Milestone: ~82% Complete (10/11 at 100%, 1 at 80%) | 49/49 Pytest Tests Passing | 72 Benchmark Runs"
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = RGBColor(0xD9, 0xE1, 0xF2)

    # 2. Coverage Matrix Table (11 Criteria + Header)
    rows = 12
    cols = 4
    left = Inches(0.4)
    top = Inches(1.42)
    width = Inches(12.533)
    height = Inches(5.7)

    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    tbl = table_shape.table
    tbl.columns[0].width = Inches(0.5)
    tbl.columns[1].width = Inches(2.2)
    tbl.columns[2].width = Inches(1.4)
    tbl.columns[3].width = Inches(8.433)

    headers = ["#", "Evaluation Criterion (Prescribed Baseline)", "Phase 2 Status", "Technical Implementation in Working Prototype & WIP Report Section Link"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if i < 3 else PP_ALIGN.LEFT
        r = p.add_run()
        r.text = h
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (num, name, status, details) in enumerate(CRITERIA_DATA, start=1):
        bg_rgb = RGBColor(0xF2, 0xF4, 0xF8) if row_idx % 2 == 1 else RGBColor(0xFF, 0xFF, 0xFF)

        c0 = tbl.cell(row_idx, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = bg_rgb
        p0 = c0.text_frame.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        r0 = p0.add_run()
        r0.text = num
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.bold = True

        c1 = tbl.cell(row_idx, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = bg_rgb
        p1 = c1.text_frame.paragraphs[0]
        p1.alignment = PP_ALIGN.LEFT
        r1 = p1.add_run()
        r1.text = name
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)
        r1.font.bold = True

        c2 = tbl.cell(row_idx, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = bg_rgb
        p2 = c2.text_frame.paragraphs[0]
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = status
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.0)
        r2.font.bold = True
        if "100%" in status:
            r2.font.color.rgb = RGBColor(0x0E, 0x8A, 0x16)
        else:
            r2.font.color.rgb = RGBColor(0xD9, 0x77, 0x06)

        c3 = tbl.cell(row_idx, 3)
        c3.fill.solid()
        c3.fill.fore_color.rgb = bg_rgb
        p3 = c3.text_frame.paragraphs[0]
        p3.alignment = PP_ALIGN.LEFT
        r3 = p3.add_run()
        r3.text = details
        r3.font.name = "Calibri"
        r3.font.size = Pt(8.0)
        r3.font.color.rgb = RGBColor(0x26, 0x26, 0x26)

    prs.save(str(OUT_PPTX))
    print(f"[DONE] Created 1-Slide Presentation: {OUT_PPTX}")

def sync_markdown_coverage():
    lines = [
        "# Autonomous Multi-Agent Delivery Fleet Coordination & Dispatch System",
        "## Evaluation Phase 2: One-Slide Criteria Coverage Matrix",
        "**Course:** CSE3101: Agentic AI — B.Tech CSE Semester VII",
        "**Group Number:** 8",
        "**Team Members:** Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)",
        "**Milestone Achievement:** ~82% Complete (10 of 11 Criteria at 100%, Criterion 11 at 80%) | 49/49 Pytest Tests Passing | 72 Benchmark Runs",
        "",
        "---",
        "",
        "### Phase 2 Evaluation Criteria Coverage & Link to Work-in-Progress (WIP) Report",
        "",
        "| # | Prescribed Baseline Criterion | Phase 2 Status | Technical Implementation in Working Prototype & WIP Report Section Link |",
        "| :---: | :--- | :---: | :--- |"
    ]
    for num, name, status, details in CRITERIA_DATA:
        formatted_details = details.replace("[WIP Report:", "**[WIP Report:").replace("]", "]**")
        # Ensure code blocks inside details
        formatted_details = formatted_details.replace("src/", "`src/").replace(".py", ".py`").replace("`src/mcp/server.py`", "`src/mcp/server.py`")
        lines.append(f"| **{num}** | **{name}** | **{status}** | {formatted_details} |")
    lines.extend([
        "",
        "---",
        "",
        "*Note: The corresponding PowerPoint 16:9 widescreen presentation slide is available at `Eval 2 Documents/1_Slide_Coverage_Matrix_Group8.pptx`.*"
    ])
    OUT_MD.write_text("\n".join(lines).strip(), encoding="utf-8")
    print(f"[DONE] Created Markdown Coverage Matrix: {OUT_MD}")

if __name__ == "__main__":
    create_coverage_slide()
    sync_markdown_coverage()
