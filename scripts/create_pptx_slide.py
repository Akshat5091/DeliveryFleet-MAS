"""Generates the official 1-Slide Presentation on Criteria Coverage for Eval-2.
Exactly 1 slide: Clear, executive, high-level summary of What is Covered (8 criteria) vs. What is Not Covered (3 criteria).
File: DeliveryFleet-MAS/Eval 2 Documents/CSE-IV_Group-8_1_Slide_Coverage_Matrix_Group8.pptx
"""
import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

REPO_DIR = Path(__file__).resolve().parent.parent
OUT_PPTX = REPO_DIR / "Eval 2 Documents" / "CSE-IV_Group-8_1_Slide_Coverage_Matrix_Group8.pptx"
OUT_MD = REPO_DIR / "Eval 2 Documents" / "Markdown Sources" / "EVAL2_1_SLIDE_COVERAGE_MATRIX.md"

# Color Palette: Academic Minimalist (Zero Blue, Pitch Black, Crimson, Forest Green)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BLACK = RGBColor(17, 24, 39)          # #111827
COLOR_CRIMSON = RGBColor(153, 27, 27)       # #991B1B Academic Crimson
COLOR_CHARCOAL = RGBColor(31, 41, 55)       # #1F2937 Body text
COLOR_MUTED = RGBColor(75, 85, 99)          # #4B5563
COLOR_GREEN = RGBColor(22, 101, 52)         # #166534 Forest Green
COLOR_BORDER = RGBColor(209, 213, 219)      # #D1D5DB Pencil Border
COLOR_CARD_BG = RGBColor(249, 250, 251)     # #F9FAFB Card Fill
COLOR_GREEN_BG = RGBColor(240, 253, 244)    # #F0FDF4 Light Mint Fill
COLOR_CRIMSON_BG = RGBColor(254, 242, 242)  # #FEF2F2 Light Red Fill

def create_coverage_slide():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # -------------------------------------------------------------------------
    # 1. TOP HEADER BANNER (Width: 12.433 in)
    # -------------------------------------------------------------------------
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(0.25), Inches(12.433), Inches(0.98))
    banner.fill.solid()
    banner.fill.fore_color.rgb = COLOR_CARD_BG
    banner.line.color.rgb = COLOR_CRIMSON
    banner.line.width = Pt(1.5)

    tf_b = banner.text_frame
    tf_b.word_wrap = True
    tf_b.margin_top = Inches(0.06)
    tf_b.margin_bottom = Inches(0.04)
    tf_b.margin_left = Inches(0.18)
    tf_b.margin_right = Inches(0.18)

    p0 = tf_b.paragraphs[0]
    p0.alignment = PP_ALIGN.LEFT
    r0 = p0.add_run()
    r0.text = "Autonomous Multi-Agent Delivery Fleet System — Evaluation 2 Criteria Coverage Matrix"
    r0.font.name = "Calibri"
    r0.font.size = Pt(15.0)
    r0.font.bold = True
    r0.font.color.rgb = COLOR_BLACK

    p1 = tf_b.add_paragraph()
    p1.alignment = PP_ALIGN.LEFT
    r1 = p1.add_run()
    r1.text = "Course: CSE3101 Agentic AI | Group 8: Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)"
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.0)
    r1.font.color.rgb = COLOR_MUTED

    p2 = tf_b.add_paragraph()
    p2.alignment = PP_ALIGN.LEFT
    r2 = p2.add_run()
    r2.text = "Milestone Status: ~73% Complete (Target: 65–70%)  —  8 Core Criteria Verified & Operational  |  3 Advanced Criteria Staged for Phase 3"
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_CRIMSON

    # -------------------------------------------------------------------------
    # 2. LEFT CARD: WHAT IS COVERED (8 Criteria — 100% Operational)
    # -------------------------------------------------------------------------
    w_left = Inches(6.05)
    h_left = Inches(5.82)
    left_x = Inches(0.45)
    top_y = Inches(1.35)

    card_left = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, top_y, w_left, h_left)
    card_left.fill.solid()
    card_left.fill.fore_color.rgb = COLOR_WHITE
    card_left.line.color.rgb = COLOR_GREEN
    card_left.line.width = Pt(1.5)

    tf_l = card_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_top = Inches(0.10)
    tf_l.margin_bottom = Inches(0.10)
    tf_l.margin_left = Inches(0.16)
    tf_l.margin_right = Inches(0.16)

    # Header Paragraph
    p_lh = tf_l.paragraphs[0]
    p_lh.alignment = PP_ALIGN.LEFT
    p_lh.space_after = Pt(6)
    r_lh = p_lh.add_run()
    r_lh.text = "WHAT IS COVERED (8 Core Baseline Criteria — 100% Verified in Phase 2)"
    r_lh.font.name = "Calibri"
    r_lh.font.size = Pt(11.5)
    r_lh.font.bold = True
    r_lh.font.color.rgb = COLOR_GREEN

    covered_items = [
        ("Criterion 1: Centralized Blackboard Shared State", "Thread-safe BlackboardState under threading.RLock() with FastMCP update tool and full provenance logging."),
        ("Criterion 2: Model Context Protocol (FastMCP)", "5 operational domain tools: Driver DB, Routing Engine, ML Delay Predictor, ChromaDB Vector RAG, and State Tool."),
        ("Criterion 3: Pydantic v2 Structured Output Contracts", "Strict schema validation across all agent decisions (DispatchDecision, RoutePlan, ExceptionReplan, FinalDeliveryReport)."),
        ("Criterion 4: Agentic Design Patterns (Hierarchical MAS)", "Supervised Hierarchical MAS supervisor with concurrent context gathering via ThreadPoolExecutor (48.6% speedup)."),
        ("Criterion 5: Programmatic Callbacks & Latency Heatmaps", "Real-time lifecycle hooks (MASCallbackHandler) streaming telemetry to JSONL; 2D density heatmaps across 72 runs."),
        ("Criterion 6: Agent-to-Agent (A2A) Protocol Communication", "Standardized JSON-RPC 2.0 network messaging (/api/a2a/route) with circuit-breaker fallback between CrewAI and Google ADK."),
        ("Criterion 7: Dual-Framework Synergy (Google ADK + CrewAI)", "Google ADK powers spatial routing (AgentCards); CrewAI powers cognitive dispatch, retrieval, and contingency replanning."),
        ("Criterion 8: Multi-Tier Security & Statutory Guardrails", "Sub-millisecond regex injection defense in 0.0004s (InputGuard) and statutory 9.0h driver fatigue limit enforcement.")
    ]

    for title, desc in covered_items:
        p = tf_l.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(4)
        
        r_tag = p.add_run()
        r_tag.text = "[VERIFIED] "
        r_tag.font.name = "Calibri"
        r_tag.font.size = Pt(9.0)
        r_tag.font.bold = True
        r_tag.font.color.rgb = COLOR_GREEN

        r_title = p.add_run()
        r_title.text = title + ": "
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(9.5)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_BLACK

        r_desc = p.add_run()
        r_desc.text = desc
        r_desc.font.name = "Calibri"
        r_desc.font.size = Pt(9.0)
        r_desc.font.color.rgb = COLOR_CHARCOAL

    # -------------------------------------------------------------------------
    # 3. RIGHT TOP CARD: WHAT IS NOT COVERED YET (3 Criteria — Staged for Phase 3)
    # -------------------------------------------------------------------------
    w_right = Inches(6.15)
    h_rtop = Inches(4.35)
    right_x = Inches(6.73)

    card_right = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, top_y, w_right, h_rtop)
    card_right.fill.solid()
    card_right.fill.fore_color.rgb = COLOR_CARD_BG
    card_right.line.color.rgb = COLOR_CRIMSON
    card_right.line.width = Pt(1.5)

    tf_r = card_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_top = Inches(0.10)
    tf_r.margin_bottom = Inches(0.08)
    tf_r.margin_left = Inches(0.16)
    tf_r.margin_right = Inches(0.16)

    p_rh = tf_r.paragraphs[0]
    p_rh.alignment = PP_ALIGN.LEFT
    p_rh.space_after = Pt(6)
    r_rh = p_rh.add_run()
    r_rh.text = "WHAT IS NOT COVERED YET (3 Advanced Criteria — Staged for Phase 3 Final Defense)"
    r_rh.font.name = "Calibri"
    r_rh.font.size = Pt(11.0)
    r_rh.font.bold = True
    r_rh.font.color.rgb = COLOR_CRIMSON

    staged_items = [
        ("Criterion 9: Distributed AI Observability & Tracing",
         "Current Phase 2 Status: Local single-host JSONL event spans active.\nStaged Phase 3 Scope: Multi-host OpenTelemetry Collector daemon exporting to live hosted Jaeger and Prometheus distributed tracing dashboards."),
        ("Criterion 10: Cloud-Scale Factorial Matrix & Pareto Optimization",
         "Current Phase 2 Status: Baseline 72 factorial runs completed locally.\nStaged Phase 3 Scope: 100+ factorial cloud benchmark runs evaluating Pareto cost-latency trade-offs under simulated network latency."),
        ("Criterion 11: Production Cloud Platform Deployment",
         "Current Phase 2 Status: Local multi-stage Docker container configured.\nStaged Phase 3 Scope: Live cloud VM deployment (AWS EC2 / GCP Compute Engine) with Cloudflare edge worker reverse proxy.")
    ]

    for title, desc in staged_items:
        p = tf_r.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(5)

        r_tag = p.add_run()
        r_tag.text = "[STAGED] "
        r_tag.font.name = "Calibri"
        r_tag.font.size = Pt(9.0)
        r_tag.font.bold = True
        r_tag.font.color.rgb = COLOR_CRIMSON

        r_title = p.add_run()
        r_title.text = title + "\n"
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(9.5)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_BLACK

        r_desc = p.add_run()
        r_desc.text = desc
        r_desc.font.name = "Calibri"
        r_desc.font.size = Pt(8.5)
        r_desc.font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------------------
    # 4. RIGHT BOTTOM CARD: EMPIRICAL VERIFICATION SUMMARY
    # -------------------------------------------------------------------------
    h_rbot = Inches(1.35)
    top_rbot = Inches(5.82)

    card_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, top_rbot, w_right, h_rbot)
    card_bot.fill.solid()
    card_bot.fill.fore_color.rgb = COLOR_WHITE
    card_bot.line.color.rgb = COLOR_BORDER
    card_bot.line.width = Pt(1.0)

    tf_bot = card_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_top = Inches(0.08)
    tf_bot.margin_bottom = Inches(0.06)
    tf_bot.margin_left = Inches(0.14)
    tf_bot.margin_right = Inches(0.14)

    p_bh = tf_bot.paragraphs[0]
    p_bh.alignment = PP_ALIGN.LEFT
    p_bh.space_after = Pt(2)
    r_bh = p_bh.add_run()
    r_bh.text = "Empirical Validation & Milestone Evidence"
    r_bh.font.name = "Calibri"
    r_bh.font.size = Pt(10.0)
    r_bh.font.bold = True
    r_bh.font.color.rgb = COLOR_BLACK

    bullets = [
        "Milestone Completion: Achieved ~73% completion (surpassing prescribed 65–70% target).",
        "Automated Test Coverage: 49/49 Pytest unit tests passing (100% green across 9 test suites).",
        "Browser UI Validation: 13/13 Selenium automated browser scenarios passing."
    ]
    for b in bullets:
        p = tf_bot.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(1)
        r = p.add_run()
        r.text = "• " + b
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = COLOR_CHARCOAL

    prs.save(str(OUT_PPTX))
    print(f"[DONE] Created EXACT 1-Slide Presentation: {OUT_PPTX.name} (Slide count: {len(prs.slides)})")

def sync_markdown_coverage():
    lines = [
        "# Autonomous Multi-Agent Delivery Fleet Coordination & Dispatch System",
        "## Evaluation Phase 2: One-Slide Criteria Coverage Matrix",
        "**Course:** CSE3101: Agentic AI — B.Tech CSE Semester VII  ",
        "**Group Number:** 8  ",
        "**Team Members:** Bhumika Yadav (230732), Aadit Bassi (230728), Akshat Nagori (230682), Sahil Mudgil (230743)  ",
        "**Phase 2 Prescribed Milestone Target:** 65–70% | **Actual Achieved Completion:** ~73% (8 Core Modules 100% Operational & Verified | 3 Staged Research Novelties)  ",
        "",
        "---",
        "",
        "### WHAT IS COVERED (8 Core Baseline Criteria — 100% Operational & Verified)",
        "* **Criterion 1 (C01): Blackboard Shared State** — Centralized thread-safe `BlackboardState` under `threading.RLock()` with FastMCP update tool and full provenance logging.",
        "* **Criterion 2 (C02): Model Context Protocol (FastMCP)** — 5 operational domain tools: Driver DB, Routing Engine, ML Delay Predictor, ChromaDB Vector RAG, and State Tool.",
        "* **Criterion 3 (C03): Pydantic v2 Structured Output Contracts** — Strict schema validation across all agent decisions (`DispatchDecision`, `RoutePlan`, `ExceptionReplan`, `FinalDeliveryReport`).",
        "* **Criterion 4 (C04): Agentic Design Patterns (Hierarchical MAS)** — Supervised Hierarchical MAS supervisor with concurrent context gathering via `ThreadPoolExecutor` (48.6% speedup).",
        "* **Criterion 5 (C05): Programmatic Callbacks & Latency Heatmaps** — Real-time lifecycle hooks (`MASCallbackHandler`) streaming telemetry to JSONL; 2D density heatmaps across 72 runs.",
        "* **Criterion 6 (C06): Agent-to-Agent (A2A) Protocol Communication** — Standardized JSON-RPC 2.0 network messaging (`/api/a2a/route`) with circuit-breaker fallback between CrewAI and Google ADK.",
        "* **Criterion 7 (C07): Dual-Framework Synergy (Google ADK + CrewAI)** — Google ADK powers spatial routing (`AgentCards`); CrewAI powers cognitive dispatch, retrieval, and contingency replanning.",
        "* **Criterion 8 (C08): Multi-Tier Security & Statutory Guardrails** — Sub-millisecond regex injection defense in 0.0004s (`InputGuard`) and statutory 9.0h driver fatigue limit enforcement.",
        "",
        "---",
        "",
        "### WHAT IS NOT COVERED YET (3 Advanced Criteria — Staged for Phase 3 Defense)",
        "* **Criterion 9 (C09): Distributed AI Observability & Tracing** — Current Phase 2 Status: Local single-host JSONL event spans active. Staged Phase 3 Scope: Multi-host OpenTelemetry Collector daemon exporting to live hosted Jaeger and Prometheus distributed tracing dashboards.",
        "* **Criterion 10 (C10): Cloud Factorial Matrix & Pareto Optimization** — Current Phase 2 Status: Baseline 72 factorial runs completed locally. Staged Phase 3 Scope: 100+ factorial cloud benchmark runs evaluating Pareto cost-latency trade-offs under simulated network latency.",
        "* **Criterion 11 (C11): Production Cloud Platform Deployment** — Current Phase 2 Status: Local multi-stage Docker container configured. Staged Phase 3 Scope: Live cloud VM deployment (AWS EC2 / GCP Compute Engine) with Cloudflare edge worker reverse proxy.",
        "",
        "---",
        "",
        "### Phase 2 Empirical Verification Summary",
        "* **Milestone Completion:** ~73% (surpassing university target of 65–70%).",
        "* **Automated Test Coverage:** 49/49 Pytest unit tests passing (100% green across 9 test suites).",
        "* **Browser UI Validation:** 13/13 Selenium automated browser scenarios passing.",
        "* **Code Repository:** Akshat5091/DeliveryFleet-MAS (Group 8)"
    ]
    OUT_MD.write_text("\n".join(lines).strip(), encoding="utf-8")
    print(f"[DONE] Created Markdown Coverage Matrix: {OUT_MD.name}")

if __name__ == "__main__":
    create_coverage_slide()
    sync_markdown_coverage()
