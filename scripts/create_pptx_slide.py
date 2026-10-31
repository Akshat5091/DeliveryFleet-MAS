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

def create_coverage_slide():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # 1. Top Banner Box
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.35), Inches(12.533), Inches(0.95))
    banner.fill.solid()
    banner.fill.fore_color.rgb = RGBColor(0x1F, 0x4E, 0x79) # Deep Academic Navy
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
    r1.text = "Course: CSE3101 Agentic AI | Group 8: Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743) | Milestone: ~78% Complete (10/11 at 100%, 1 at 80%)"
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
    tbl.columns[0].width = Inches(0.5)   # #
    tbl.columns[1].width = Inches(2.2)   # Minimum Evaluation Criterion
    tbl.columns[2].width = Inches(1.4)   # Phase 2 Status
    tbl.columns[3].width = Inches(8.433) # Implementation & WIP Report Link

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

    data = [
        ("1", "Blackboard Shared State", "COVERED (100%)", "Centralized BlackboardState in src/schemas/blackboard.py with RLock reentrant concurrency synchronization, FastMCP update tool, and immutable provenance trail. [WIP Report: Chapter 3.1 & Section 4.3]"),
        ("2", "MCP Tool Integration (>= 2)", "COVERED (100%)", "FastMCP server (src/mcp/server.py) exposing 5 tools: Driver DB, Routing Engine, Delay Forecaster (ML), ChromaDB RAG, and Blackboard Update. Exceeds >= 2 requirement. [WIP Report: Chapter 3.2 & Section 4.4]"),
        ("3", "Pydantic Structured Output", "COVERED (100%)", "Pydantic v2 schemas: DispatchDecision, RoutePlan, ExceptionReplan, FinalDeliveryReport with validated JSON export and GitHub-flavored Markdown tables. [WIP Report: Chapter 3.3]"),
        ("4", "Agentic Design Patterns", "COVERED (100%)", "Supervised Hierarchical Manager MAS pattern with parallel context gathering (ThreadPoolExecutor) benchmarked against Sequential Pipeline (0.518s vs 0.672s latency). [WIP Report: Chapter 3.4 & Section 4.2]"),
        ("5", "Callbacks & Agent Heatmaps", "COVERED (100%)", "MASCallbackHandler capturing start, end, tokens, and latency. Generated 3 publication-grade heatmaps: within-agent metrics, 48-run density, and rubric heatmap. [WIP Report: Chapter 3.5 & Section 5.0]"),
        ("6", "A2A Protocol Communication", "COVERED (100%)", "A2ABridge in src/agents/a2a_bridge.py routing A2AMessage envelopes between CrewAI and Google ADK Route Agent with sub-2ms overhead and zero binary coupling. [WIP Report: Chapter 3.6 & Section 4.1]"),
        ("7", "Dual Framework (CrewAI + ADK)", "COVERED (100%)", "Google ADK natively powers Route Optimization Agent; CrewAI natively powers Orchestrator, Dispatch, Retrieval, and Exception Agents. Zero other frameworks used. [WIP Report: Chapter 3.7 & Section 4.1]"),
        ("8", "Security & Multi-Tier Guardrails", "COVERED (100%)", "InputGuard (regex injection defense from LAB-06 in 0.000s + toxic term masking), ToolValidator, BusinessGuardrails (statutory 9.0h driving limit block). [WIP Report: Chapter 3.8, Section 4.7 & Section 6.0]"),
        ("9", "AI Observability & Tracing", "COVERED (100%)", "OpenTelemetry-compatible MASTracer generating distributed trace trees with sub-spans logged in run_events.jsonl. Microsecond precision without token bloat. [WIP Report: Chapter 3.9 & Section 4.8]"),
        ("10", "Evaluation (40+ Runs & Boxplots)", "COVERED (100%)", "48 systematic benchmark runs across 2 architectures, 2 reasoning styles, 4 personas, 3 orders. Generated latency/cost boxplots + academic rubric (Y in R^4). [WIP Report: Chapter 3.10 & Section 5.0]"),
        ("11", "Cloud Platform Deployment", "READY (80%)", "Production multi-stage Dockerfile and docker-compose.yml orchestrating MAS core, FastMCP server, ChromaDB storage volume, and OpenTelemetry collector. [WIP Report: Chapter 3.11 & Section 9.0]")
    ]

    for row_idx, (num, name, status, details) in enumerate(data, start=1):
        bg_rgb = RGBColor(0xF2, 0xF4, 0xF8) if row_idx % 2 == 1 else RGBColor(0xFF, 0xFF, 0xFF)

        # Col 0: #
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

        # Col 1: Criterion Name
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

        # Col 2: Status Badge
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
            r2.font.color.rgb = RGBColor(0x0E, 0x8A, 0x16) # Emerald Green
        else:
            r2.font.color.rgb = RGBColor(0xD9, 0x77, 0x06) # Amber

        # Col 3: Details & WIP Report Link
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
    md = """# Autonomous Multi-Agent Delivery Fleet Coordination & Dispatch System
## Evaluation Phase 2: One-Slide Criteria Coverage Matrix
**Course:** CSE3101: Agentic AI — B.Tech CSE Semester VII
**Group Number:** 9
**Team Members:** Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)
**Milestone Achievement:** ~78% Complete (10 of 11 Criteria at 100%, Criterion 11 at 80%)

---

### Phase 2 Evaluation Criteria Coverage & Link to Work-in-Progress (WIP) Report

| # | Prescribed Baseline Criterion | Phase 2 Status | Technical Implementation in Working Prototype & WIP Report Section Link |
| :---: | :--- | :---: | :--- |
| **1** | **Blackboard Shared State** | **COVERED (100%)** | Centralized `BlackboardState` in `src/schemas/blackboard.py` with `RLock` concurrency synchronization, FastMCP update tool, and immutable provenance trail. **[WIP Report: Chapter 3.1 & Section 4.3]** |
| **2** | **MCP Tool Integration (>= 2)** | **COVERED (100%)** | FastMCP server (`src/mcp/server.py`) exposing 5 tools: Driver DB, Routing Engine, Delay Forecaster (ML), ChromaDB RAG, and Blackboard Update. Exceeds >= 2 requirement. **[WIP Report: Chapter 3.2 & Section 4.4]** |
| **3** | **Pydantic Structured Output** | **COVERED (100%)** | Pydantic v2 schemas: `DispatchDecision`, `RoutePlan`, `ExceptionReplan`, `FinalDeliveryReport` with validated JSON export and Markdown tables. **[WIP Report: Chapter 3.3]** |
| **4** | **Agentic Design Patterns** | **COVERED (100%)** | Supervised Hierarchical Manager MAS pattern with parallel context gathering (`ThreadPoolExecutor`) benchmarked against Sequential Pipeline (0.518s vs 0.672s latency). **[WIP Report: Chapter 3.4 & Section 4.2]** |
| **5** | **Callbacks & Agent Heatmaps** | **COVERED (100%)** | `MASCallbackHandler` capturing start, end, tokens, and latency. Generated 3 publication-grade heatmaps: within-agent metrics, 48-run density, and rubric heatmap. **[WIP Report: Chapter 3.5 & Section 5.0]** |
| **6** | **A2A Protocol Communication** | **COVERED (100%)** | `A2ABridge` in `src/agents/a2a_bridge.py` routing `A2AMessage` envelopes between CrewAI and Google ADK Route Agent with sub-2ms overhead and zero binary coupling. **[WIP Report: Chapter 3.6 & Section 4.1]** |
| **7** | **Dual Framework (CrewAI + ADK)** | **COVERED (100%)** | Google ADK natively powers Route Optimization Agent; CrewAI natively powers Orchestrator, Dispatch, Retrieval, and Exception Agents. Zero other frameworks used. **[WIP Report: Chapter 3.7 & Section 4.1]** |
| **8** | **Security & Multi-Tier Guardrails** | **COVERED (100%)** | `InputGuard` (regex injection defense from LAB-06 in 0.000s + toxic term masking), `ToolValidator`, `BusinessGuardrails` (statutory 9.0h driving limit block). **[WIP Report: Chapter 3.8, Section 4.7 & Section 6.0]** |
| **9** | **AI Observability & Tracing** | **COVERED (100%)** | OpenTelemetry-compatible `MASTracer` generating distributed trace trees with sub-spans logged in `run_events.jsonl`. Microsecond precision without token bloat. **[WIP Report: Chapter 3.9 & Section 4.8]** |
| **10** | **Evaluation (40+ Runs & Boxplots)** | **COVERED (100%)** | 48 systematic benchmark runs across 2 architectures, 2 reasoning styles, 4 personas, 3 orders. Generated latency/cost boxplots + academic rubric ($Y \in \mathbb{R}^4$). **[WIP Report: Chapter 3.10 & Section 5.0]** |
| **11** | **Cloud Platform Deployment** | **READY (80%)** | Production multi-stage `Dockerfile` and `docker-compose.yml` orchestrating MAS core, FastMCP server, ChromaDB storage volume, and OpenTelemetry collector. **[WIP Report: Chapter 3.11 & Section 9.0]** |

---

*Note: The corresponding PowerPoint 16:9 widescreen presentation slide is available at `Eval 2 Documents/1_Slide_Coverage_Matrix_Group8.pptx`.*
"""
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(md.strip())
    print(f"[DONE] Created Markdown Coverage Matrix: {OUT_MD}")

if __name__ == "__main__":
    create_coverage_slide()
    sync_markdown_coverage()

