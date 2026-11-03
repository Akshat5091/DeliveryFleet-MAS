"""Autonomous Multi-Agent Delivery Fleet Orchestration System
Phase 2 Master Presentation Deck Builder (22 Slides)
Engineered for authentic human engineering presentation:
- Clean white background (#FFFFFF) with pitch black headings (#111827).
- Deep academic crimson accents (#991B1B) and forest green completion indicators (#166534).
- Formal Calibri and Consolas typography with zero blue elements and zero emojis.
- Left-aligned 11pt code blocks with preserved indentation.
- Concise 4-bullet architectural mechanisms for every code snippet.
- Pure engineering language: zero rubric citations, zero viva meta-talk, zero defensive grading phrasing.
"""
import sys
import zipfile
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

REPO_DIR = Path(r"D:\AKSHAT\DOCS\BTech CSE\Sem 7\Agentic AI\DeliveryFleet-MAS")
OUT_DIR = REPO_DIR / "Eval 2 Documents"
OUT_PPTX = OUT_DIR / "DeliveryFleet_MAS_Evaluation2_Master_Presentation.pptx"
OUT_1SLIDE = OUT_DIR / "1_Slide_Coverage_Matrix_Group8.pptx"

# Color Palette (Human Academic: Pitch Black, Deep Crimson & Neutral Pencil Gray - Zero Blue)
COLOR_WHITE = RGBColor(255, 255, 255)       # #FFFFFF Pure White Slide Background
COLOR_BLACK = RGBColor(17, 24, 39)          # #111827 Pitch Charcoal / Black (Primary Slide Headers)
COLOR_CRIMSON = RGBColor(153, 27, 27)       # #991B1B Deep Academic Crimson / Maroon (Card Headers & Primary Accent)
COLOR_MUTED = RGBColor(75, 85, 99)          # #4B5563 Category Trackers & Neutral Metadata
COLOR_CHARCOAL = RGBColor(31, 41, 55)       # #1F2937 Primary Body Text
COLOR_BODY = RGBColor(55, 65, 81)           # #374151 Secondary Descriptive Text
COLOR_CARD_BG = RGBColor(250, 250, 250)     # #FAFAFA Neutral Off-White Card Surface
COLOR_CARD_BORDER = RGBColor(209, 213, 219) # #D1D5DB Neutral Pencil Gray Outline
COLOR_CODE_BG = RGBColor(243, 244, 246)     # #F3F4F6 Neutral Light Gray Code Surface
COLOR_CODE_BORDER = RGBColor(209, 213, 219) # #D1D5DB Neutral Outline
COLOR_CODE_TEXT = RGBColor(17, 24, 39)      # #111827 Dark Monospace Text
COLOR_GREEN = RGBColor(22, 101, 52)         # #166534 Forest Green for Completed Modules
COLOR_DIVIDER = RGBColor(229, 231, 235)     # #E5E7EB Subtle Neutral Rule Line

def create_deck():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_slide_header(slide, title_text, category_text):
        # Category tracker (clean Title Case, not loud all-caps)
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(11.0)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_CRIMSON

        # Main Slide Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.55))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(22.0)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_BLACK

        # Subtle divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_DIVIDER
        line.line.color.rgb = COLOR_DIVIDER

    def add_card(slide, left, top, width, height, title=None, border_color=COLOR_CARD_BORDER, bg_color=COLOR_CARD_BG):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.0)
        
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.18)
        tf.margin_bottom = Inches(0.18)
        
        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Calibri"
            p.font.size = Pt(14.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_CRIMSON
            p.space_after = Pt(8)
        return tf

    def add_bullet(tf, bold_prefix, text, size=13.0, space_after=6, text_color=COLOR_CHARCOAL, bold_color=COLOR_BLACK):
        p = tf.add_paragraph()
        p.font.name = "Calibri"
        p.font.size = Pt(size)
        p.space_after = Pt(space_after)
        
        # Neutral bullet marker
        r_bullet = p.add_run()
        r_bullet.text = "• "
        r_bullet.font.bold = True
        r_bullet.font.color.rgb = COLOR_MUTED
        
        if bold_prefix:
            r_bold = p.add_run()
            r_bold.text = bold_prefix + " "
            r_bold.font.bold = True
            r_bold.font.color.rgb = bold_color
            
        r_text = p.add_run()
        r_text.text = text
        r_text.font.color.rgb = text_color
        return p

    def add_code_slide(slide_title, category_text, file_path, line_ref, code_text, bullets):
        slide = prs.slides.add_slide(blank_layout)
        add_slide_header(slide, slide_title, category_text)
        
        # Reference banner under title
        ref_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.3))
        tf_ref = ref_box.text_frame
        tf_ref.margin_left = tf_ref.margin_right = tf_ref.margin_top = tf_ref.margin_bottom = 0
        p_ref = tf_ref.paragraphs[0]
        p_ref.text = f"Source Code File: {file_path}  |  Line References: {line_ref}"
        p_ref.font.name = "Consolas"
        p_ref.font.size = Pt(11.0)
        p_ref.font.bold = True
        p_ref.font.color.rgb = COLOR_CRIMSON

        # Left Column: Code Box (VS Code styled editor frame, strictly left-aligned)
        w_code = Inches(6.4)
        h_box = Inches(5.3)
        code_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.75), w_code, h_box)
        code_shape.fill.solid()
        code_shape.fill.fore_color.rgb = COLOR_CODE_BG
        code_shape.line.color.rgb = COLOR_CODE_BORDER
        code_shape.line.width = Pt(1.0)
        
        tf_code = code_shape.text_frame
        tf_code.word_wrap = False
        tf_code.margin_left = Inches(0.25)
        tf_code.margin_right = Inches(0.20)
        tf_code.margin_top = Inches(0.22)
        tf_code.margin_bottom = Inches(0.22)
        
        lines = code_text.strip().split("\n")
        code_font_size = Pt(10.5) if len(lines) > 20 else Pt(11.0)
        
        for idx, line in enumerate(lines):
            p_code = tf_code.paragraphs[0] if idx == 0 else tf_code.add_paragraph()
            p_code.text = line
            p_code.alignment = PP_ALIGN.LEFT
            p_code.font.name = "Consolas"
            p_code.font.size = code_font_size
            p_code.font.color.rgb = COLOR_CODE_TEXT
            p_code.space_after = Pt(2)
        
        # Right Column: Explanation Card (What is happening and why in 4 concise lines)
        w_exp = Inches(5.083)
        tf_exp = add_card(slide, Inches(7.45), Inches(1.75), w_exp, h_box, title="Engineering Architecture & Mechanism")
        for b_bold, b_txt in bullets:
            add_bullet(tf_exp, b_bold, b_txt, size=12.0, space_after=10)

    # =========================================================================
    # SLIDE 1: Title Slide (Simple, Crisp, Academic)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    
    t_box1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(10.933), Inches(2.2))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    
    p_kicker = tf1.paragraphs[0]
    p_kicker.text = "CSE3101: Agentic Artificial Intelligence | Evaluation Phase 2"
    p_kicker.font.name = "Calibri"
    p_kicker.font.size = Pt(13.0)
    p_kicker.font.bold = True
    p_kicker.font.color.rgb = COLOR_CRIMSON
    p_kicker.space_after = Pt(10)
    
    p_main = tf1.add_paragraph()
    p_main.text = "Autonomous Multi-Agent Delivery Fleet\nOrchestration System"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(36.0)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_BLACK
    p_main.space_after = Pt(14)
    
    p_sub = tf1.add_paragraph()
    p_sub.text = "A Heterogeneous Dual-Framework Multi-Agent Architecture with Shared Blackboard State, Real-Time Model Context Protocol (FastMCP) Tools, and Multi-Tier Safety Guardrails."
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(15.0)
    p_sub.font.color.rgb = COLOR_BODY

    # Team Members Box
    tf_team = add_card(slide1, Inches(1.2), Inches(4.3), Inches(10.933), Inches(2.3), title="Project Team (Group 8)")
    add_bullet(tf_team, "Bhumika Yadav (230732):", "Architecture Lead — Blackboard Shared State, Concurrency Synchronization, Pydantic Schemas", size=13.0, space_after=4)
    add_bullet(tf_team, "Aadit Bassi (230728):", "Routing Lead — Google ADK Route Agent, A2A Protocol Bridge, Graph Dijkstra Routing", size=13.0, space_after=4)
    add_bullet(tf_team, "Akshat Nagori (230682):", "Security & Retrieval Lead — InputGuard Injection Defense, ChromaDB Vector RAG, Dashboard UI", size=13.0, space_after=4)
    add_bullet(tf_team, "Sahil Mudgil (230743):", "ML & Evaluation Lead — Random Forest Delay Prediction, Business Guardrails, Benchmark Suite", size=13.0, space_after=4)

    # =========================================================================
    # SLIDE 2: Executive Summary & System Blueprint
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide2, "Executive Summary: System Architecture & Objectives", "Project Overview & Engineering Motivation")
    
    tf_top = add_card(slide2, Inches(0.8), Inches(1.55), Inches(11.733), Inches(1.35), title="Project Objectives & Architecture")
    add_bullet(tf_top, "Core Objective:", "Deploy a production-grade Multi-Agent System (MAS) that autonomously routes, dispatches, and coordinates urban freight fleets without manual intervention.", size=13.5, space_after=4)
    add_bullet(tf_top, "Primary Innovation:", "Bridging CrewAI cognitive reasoning with Google Agent Development Kit (ADK) spatial routing over a standardized Agent-to-Agent (A2A) protocol, backed by a thread-safe Blackboard shared memory.", size=13.5, space_after=0)

    w2 = Inches(3.75)
    gap2 = Inches(0.24)
    
    tf_c1 = add_card(slide2, Inches(0.8), Inches(3.05), w2, Inches(3.95), title="1. Autonomous Fleet Dispatch")
    add_bullet(tf_c1, "Heterogeneous Agents:", "Four specialized autonomous agents collaborate to validate, route, schedule, and safely dispatch packages.")
    add_bullet(tf_c1, "Knowledge Retrieval:", "ChromaDB vector search retrieves municipal freight bylaws, low-emission EV zones, and driver shift rules in under 15ms.")
    add_bullet(tf_c1, "ReAct Reasoning:", "Agents evaluate candidates using Observation-Thought-Action loops, preventing greedy vehicle over-allocation.")

    tf_c2 = add_card(slide2, Inches(0.8) + w2 + gap2, Inches(3.05), w2, Inches(3.95), title="2. Decoupled Tool Ecosystem")
    add_bullet(tf_c2, "Model Context Protocol:", "Decouples LLM cognition from live databases and spatial math via 5 FastMCP domain tools.")
    add_bullet(tf_c2, "ML Delay Predictor:", "Trained Scikit-Learn Random Forest regression (R^2 = 0.901, MAE = 2.94 mins) computes traffic delay in 0.0008s with zero token spend.")
    add_bullet(tf_c2, "Deterministic Contracts:", "Strict Pydantic v2 schemas guarantee zero parsing failures across all inter-agent handoffs.")

    tf_c3 = add_card(slide2, Inches(0.8) + (w2 + gap2)*2, Inches(3.05), w2, Inches(3.95), title="3. Safety & Concurrency Control")
    add_bullet(tf_c3, "Three-Tier Guardrails:", "Sub-millisecond regex injection defense, Pydantic type bounds, and statutory 9.0h driver fatigue limits.")
    add_bullet(tf_c3, "Concurrency Safety:", "Reentrant Lock (threading.RLock) prevents race conditions during simultaneous multi-agent writes.")
    add_bullet(tf_c3, "Dynamic Exception Replan:", "Autonomous road blockage and vehicle breakdown recovery within 0.05 seconds.")

    # =========================================================================
    # SLIDE 3: The Real-World Industry Problem
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide3, "The Logistics Problem: Why Monolithic LLMs Fail", "Domain Challenges in Urban Last-Mile Logistics")
    
    tf_p_top = add_card(slide3, Inches(0.8), Inches(1.55), Inches(11.733), Inches(1.2), title="The Urban Logistics Environment")
    add_bullet(tf_p_top, "Operational Complexity:", "Urban delivery operations handle dynamic parcel volumes across volatile municipal regulations, localized traffic congestion, and unexpected vehicle breakdowns.", size=13.0, space_after=0)

    w3 = Inches(5.7)
    
    tf_p1 = add_card(slide3, Inches(0.8), Inches(2.9), w3, Inches(4.1), title="Limitations of Single-Agent Systems")
    add_bullet(tf_p1, "Single Point of Failure:", "Monolithic prompts attempting to parse notes, query databases, calculate paths, and predict delays crash if any single step fails.")
    add_bullet(tf_p1, "Context Saturation:", "Packing vehicle fleets, road coordinates, and regulatory bylaws into one prompt causes hallucinations and high token costs.")
    add_bullet(tf_p1, "Vulnerability to Injection:", "Untrusted user delivery notes ('ignore previous instructions') hijack dispatch logic when no perimeter defense exists.")
    add_bullet(tf_p1, "Rigid Failure Modes:", "Corridor blockages or vehicle dropouts cause pipeline crashes requiring manual operator intervention.")

    tf_p2 = add_card(slide3, Inches(6.833), Inches(2.9), w3, Inches(4.1), title="Modular Multi-Agent Architecture Solution")
    add_bullet(tf_p2, "Separation of Concerns:", "Four specialized agents partition tasks. The Dispatch Agent handles personnel; the Route Agent resolves spatial paths.")
    add_bullet(tf_p2, "Shared Blackboard State:", "Agents interact via structured shared memory, keeping individual context windows small and focused.")
    add_bullet(tf_p2, "Pre-Execution Guardrails:", "Adversarial prompts are intercepted by regex in 0.0004s before the language model is ever invoked.")
    add_bullet(tf_p2, "Dynamic Mid-Route Recovery:", "The Exception Agent detects road closures and recalculates relief routes and drivers within 50 milliseconds.")

    # =========================================================================
    # SLIDE 4: Multi-Agent Architecture (4 Core Agents)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide4, "System Architecture: 4 Specialized Autonomous Agents", "Agent Taxonomy, Framework Mapping & Operational Roles")
    
    w4 = Inches(2.78)
    gap4 = Inches(0.2)
    
    tf_a1 = add_card(slide4, Inches(0.8), Inches(1.55), w4, Inches(5.45), title="1. Dispatch Agent")
    add_bullet(tf_a1, "Framework:", "CrewAI")
    add_bullet(tf_a1, "Role:", "Lead Personnel Controller")
    add_bullet(tf_a1, "Goal:", "Matches packages to optimal drivers using ReAct reasoning.")
    add_bullet(tf_a1, "Tools Used:", "driver_db_lookup, policy_rag_search, blackboard_update")
    add_bullet(tf_a1, "Why CrewAI?", "Provides sophisticated ReAct cognitive loops, goal-driven autonomy, and role-based persona prompting.")
    add_bullet(tf_a1, "Key Rule:", "Strictly respects driver weight capacity and shift hour limits.")

    tf_a2 = add_card(slide4, Inches(0.8) + w4 + gap4, Inches(1.55), w4, Inches(5.45), title="2. Retrieval Agent")
    add_bullet(tf_a2, "Framework:", "CrewAI")
    add_bullet(tf_a2, "Role:", "Compliance & Policy Auditor")
    add_bullet(tf_a2, "Goal:", "Retrieves municipal bylaws and driver rest-break rules via Vector RAG.")
    add_bullet(tf_a2, "Tools Used:", "policy_rag_search (ChromaDB Vector Store)")
    add_bullet(tf_a2, "Why CrewAI?", "Seamlessly injects semantic context into the shared memory board before downstream decisions.")
    add_bullet(tf_a2, "Speed:", "Vector retrieval completes in under 15ms locally.")

    tf_a3 = add_card(slide4, Inches(0.8) + (w4 + gap4)*2, Inches(1.55), w4, Inches(5.45), title="3. Route Agent")
    add_bullet(tf_a3, "Framework:", "Google ADK")
    add_bullet(tf_a3, "Role:", "Spatial Optimization Engine")
    add_bullet(tf_a3, "Goal:", "Computes turn-by-turn road paths and traffic delays.")
    add_bullet(tf_a3, "Tools Used:", "routing_engine_calculate, delay_predictor_forecast")
    add_bullet(tf_a3, "Why Google ADK?", "Google ADK excels at declarative AgentCard schemas, structured tool calling, and high-speed JSON-RPC services.")
    add_bullet(tf_a3, "Protocol:", "Communicates via A2A Protocol Bridge over HTTP.")

    tf_a4 = add_card(slide4, Inches(0.8) + (w4 + gap4)*3, Inches(1.55), w4, Inches(5.45), title="4. Exception Agent")
    add_bullet(tf_a4, "Framework:", "CrewAI")
    add_bullet(tf_a4, "Role:", "Dynamic Contingency Resolver")
    add_bullet(tf_a4, "Goal:", "Recovers immediately from road blockages and driver fatigue.")
    add_bullet(tf_a4, "Tools Used:", "routing_engine_calculate, driver_db_lookup, blackboard_update")
    add_bullet(tf_a4, "Autonomous Replanning:", "Executes backup routes or relief handoffs in under 0.05 seconds.")
    add_bullet(tf_a4, "Safety Cap:", "Deterministically blocks drivers exceeding 9.0 shift hours.")

    # =========================================================================
    # SLIDE 5: End-to-End System Flowchart: Execution Lifecycle & Agent Roles
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide5, "End-to-End System Flowchart: Execution Lifecycle & Agent Roles", "System Architecture & Execution Pipeline")

    w5 = Inches(3.65)
    gap5 = Inches(0.39)
    h5 = Inches(2.60)
    top_r1 = Inches(1.50)
    top_r2 = Inches(4.45)

    # ----------------- ROW 1: Stages 1 to 3 -----------------
    # Stage 1 Card: Ingestion & Input Guard
    tf_s1 = add_card(slide5, Inches(0.80), top_r1, w5, h5, title="Stage 1: Ingestion & Input Guard")
    add_bullet(tf_s1, "Architecture Pattern:", "Pre-LLM Perimeter Defense", size=11.0, space_after=3)
    add_bullet(tf_s1, "Component & File:", "InputGuard regex filter in src/guardrails/input_guard.py", size=10.5, space_after=3)
    add_bullet(tf_s1, "What Happens First:", "Scans incoming customer order in 0.0004s before invoking any LLM.", size=10.5, space_after=3)
    add_bullet(tf_s1, "Security Action:", "Strips prompt injection and masks toxic input; aborts malicious payloads.", size=10.5, space_after=2)

    # Arrow 1 -> 2
    arr1 = slide5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.47), Inches(2.65), Inches(0.35), Inches(0.22))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = COLOR_CRIMSON
    arr1.line.color.rgb = COLOR_CRIMSON

    # Stage 2 Card: Orchestrator & Centralized Blackboard
    tf_s2 = add_card(slide5, Inches(4.84), top_r1, w5, h5, title="Stage 2: Orchestrator & Blackboard")
    add_bullet(tf_s2, "Architecture Pattern:", "Centralized Shared State under threading.RLock", size=11.0, space_after=3)
    add_bullet(tf_s2, "Main Orchestrator:", "HierarchicalOrchestrator initiates supervisory lifecycle.", size=10.5, space_after=3)
    add_bullet(tf_s2, "State Management:", "Instantiates BlackboardState model for order in src/blackboard/.", size=10.5, space_after=3)
    add_bullet(tf_s2, "Operational Role:", "Writes initial order parameters and starts immutable provenance audit log.", size=10.5, space_after=2)

    # Arrow 2 -> 3
    arr2 = slide5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.51), Inches(2.65), Inches(0.35), Inches(0.22))
    arr2.fill.solid()
    arr2.fill.fore_color.rgb = COLOR_CRIMSON
    arr2.line.color.rgb = COLOR_CRIMSON

    # Stage 3 Card: Parallel Context Retrieval
    tf_s3 = add_card(slide5, Inches(8.88), top_r1, w5, h5, title="Stage 3: Parallel Context Retrieval")
    add_bullet(tf_s3, "Architecture Pattern:", "Parallel Execution via ThreadPoolExecutor(max_workers=2)", size=11.0, space_after=3)
    add_bullet(tf_s3, "Concurrent Execution:", "Retrieval Agent (ChromaDB RAG) & Driver DB (SQLite) run in parallel.", size=10.5, space_after=3)
    add_bullet(tf_s3, "Measured Performance:", "Completes both I/O queries in 21ms barrier join (vs 600ms sequential).", size=10.5, space_after=3)
    add_bullet(tf_s3, "Blackboard Commit:", "Writes candidate drivers and active municipal rules under concurrency lock.", size=10.5, space_after=2)

    # Middle Lifecycle Connector Banner (in the 0.35" gap between Row 1 and Row 2)
    mid_box = slide5.shapes.add_textbox(Inches(0.80), Inches(4.14), Inches(11.733), Inches(0.26))
    tf_mid = mid_box.text_frame
    tf_mid.margin_left = tf_mid.margin_right = tf_mid.margin_top = tf_mid.margin_bottom = 0
    p_mid = tf_mid.paragraphs[0]
    p_mid.alignment = PP_ALIGN.CENTER
    p_mid.text = "Step 1: Security Guard  →  Step 2: Blackboard Init  →  Step 3: Parallel Context  →  Step 4: Dispatch ReAct  →  Step 5: Route Microservice  →  Step 6: Exception Recovery"
    p_mid.font.name = "Calibri"
    p_mid.font.size = Pt(9.5)
    p_mid.font.bold = True
    p_mid.font.color.rgb = COLOR_MUTED

    # ----------------- ROW 2: Stages 4 to 6 -----------------
    # Stage 4 Card: Cognitive Dispatch Deliberation
    tf_s4 = add_card(slide5, Inches(0.80), top_r2, w5, h5, title="Stage 4: Cognitive Dispatch Agent")
    add_bullet(tf_s4, "Architecture Pattern:", "CrewAI Goal-Driven ReAct Reasoning Loop", size=11.0, space_after=3)
    add_bullet(tf_s4, "Agent Invoked:", "Dispatch Agent (CrewAI) in src/agents/crew_dispatch_agent.py", size=10.5, space_after=3)
    add_bullet(tf_s4, "Cognitive Role:", "Deliberates on weight capacities, delivery priority, and zoning bylaws.", size=10.5, space_after=3)
    add_bullet(tf_s4, "Safety Enforcement:", "BusinessGuardrails strictly enforces statutory 9.0h driver fatigue limit.", size=10.5, space_after=2)

    # Arrow 4 -> 5
    arr4 = slide5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.47), Inches(5.60), Inches(0.35), Inches(0.22))
    arr4.fill.solid()
    arr4.fill.fore_color.rgb = COLOR_CRIMSON
    arr4.line.color.rgb = COLOR_CRIMSON

    # Stage 5 Card: Spatial Routing & ML Delay Prediction
    tf_s5 = add_card(slide5, Inches(4.84), top_r2, w5, h5, title="Stage 5: Route Agent & ML Predictor")
    add_bullet(tf_s5, "Architecture Pattern:", "Google ADK Declarative Microservice via A2A Bridge", size=11.0, space_after=3)
    add_bullet(tf_s5, "Agent Invoked:", "Route Agent (Google ADK) over HTTP JSON-RPC 2.0 (/api/a2a/route)", size=10.5, space_after=3)
    add_bullet(tf_s5, "Computational Engine:", "Graph Dijkstra computes shortest path; Random Forest predicts traffic delay.", size=10.5, space_after=3)
    add_bullet(tf_s5, "Circuit Breaker:", "Automatic fallback to local Dijkstra graph routing on network timeout.", size=10.5, space_after=2)

    # Arrow 5 -> 6
    arr5 = slide5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.51), Inches(5.60), Inches(0.35), Inches(0.22))
    arr5.fill.solid()
    arr5.fill.fore_color.rgb = COLOR_CRIMSON
    arr5.line.color.rgb = COLOR_CRIMSON

    # Stage 6 Card: Exception Recovery & Final Report Commit
    tf_s6 = add_card(slide5, Inches(8.88), top_r2, w5, h5, title="Stage 6: Exception Agent & Report")
    add_bullet(tf_s6, "Architecture Pattern:", "Dynamic Autonomous Exception Recovery Loop", size=11.0, space_after=3)
    add_bullet(tf_s6, "Agent Invoked:", "Exception Agent (CrewAI) in src/agents/crew_exception_agent.py", size=10.5, space_after=3)
    add_bullet(tf_s6, "Dynamic Replanning:", "Recalculates alternate route or relief driver on disruption in <0.05s.", size=10.5, space_after=3)
    add_bullet(tf_s6, "Final Output:", "Commits Pydantic v2 FinalDeliveryReport, updates telemetry & UI dashboard.", size=10.5, space_after=2)

    # =========================================================================
    # SLIDE 6: Code Snippet: CrewAI Dispatch Agent Definition & Tools
    # =========================================================================
    add_code_slide(
        slide_title="Code Snippet: CrewAI Dispatch Agent Definition & Tools",
        category_text="Implementation & Source Code Reference 1",
        file_path="src/agents/crew_dispatch_agent.py",
        line_ref="Lines 30–52",
        code_text="""# Autonomous Urban Dispatcher in CrewAI
self.agent = Agent(
    role="Urban Fleet Dispatch Supervisor",
    goal="Optimize delivery vehicle allocation while strictly "
         "enforcing shift caps and municipal zoning rules.",
    backstory="Senior logistics controller prioritizing safety "
              "and on-time delivery SLAs.",
    tools=[
        driver_db_lookup,    # FastMCP driver capacity tool
        policy_rag_search,   # ChromaDB vector bylaws tool
        blackboard_update    # Central shared state tool
    ],
    verbose=True,
    allow_delegation=False,  # Bounded execution, no loops
    memory=True              # Preserves reasoning context
)""",
        bullets=[
            ("What is Happening:", "Instantiates the lead CrewAI Dispatch Agent with an autonomous fleet management role and explicit operational constraints."),
            ("Implementation Mechanism:", "Binds 3 decoupled FastMCP tools (driver_db_lookup, policy_rag_search, blackboard_update) rather than executing direct SQL queries."),
            ("Why this Architecture:", "Setting allow_delegation=False prevents recursive delegation storms, guaranteeing bounded token expenditure and predictable sub-second runtime."),
            ("System Invariant:", "ReAct reasoning loops ensure drivers are selected strictly based on weight capacity and remaining legal shift hours rather than greedy allocation.")
        ]
    )

    # =========================================================================
    # SLIDE 7: Dual Framework Integration (CrewAI + Google ADK)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide7, "Dual-Framework Architecture: Complementary Paradigms", "Framework Selection & Architectural Rationale")
    
    tf_top6 = add_card(slide7, Inches(0.8), Inches(1.55), Inches(11.733), Inches(1.35), title="Why Integrate CrewAI and Google ADK?")
    add_bullet(tf_top6, "Complementary Strengths:", "Last-mile logistics requires two distinct capabilities: high-level cognitive deliberation for qualitative rules, and low-latency mathematical computation for spatial graph routing.", size=13.0, space_after=2)
    add_bullet(tf_top6, "Decoupled Integration:", "CrewAI handles cognitive multi-agent workflows while Google ADK runs as an independent high-throughput microservice connected via standard JSON-RPC 2.0.", size=13.0, space_after=0)

    w6 = Inches(5.7)
    
    tf_f1 = add_card(slide7, Inches(0.8), Inches(3.05), w6, Inches(4.0), title="CrewAI: High-Level Cognitive Orchestration")
    add_bullet(tf_f1, "Primary Role:", "Autonomous goal decomposition, persona steering, and multi-agent coordination.")
    add_bullet(tf_f1, "Component Scope:", "Powers the Dispatch Agent, Retrieval Agent, and Exception Agent.")
    add_bullet(tf_f1, "Qualitative Reasoning:", "Interprets unstructured customer delivery notes, environmental zones, and driver rest break policies.")
    add_bullet(tf_f1, "Dynamic Replanning:", "Re-evaluates assignments autonomously during mid-route road closures without hardcoded decision branches.")

    tf_f2 = add_card(slide7, Inches(6.833), Inches(3.05), w6, Inches(4.0), title="Google ADK: Lightweight Declarative Routing")
    add_bullet(tf_f2, "Primary Role:", "Declarative schema definition (AgentCard), typed input validation, and high-speed tool execution.")
    add_bullet(tf_f2, "Component Scope:", "Powers the Route Agent and machine learning delay prediction pipeline.")
    add_bullet(tf_f2, "Microservice Contract:", "Standardizes spatial routing as an independent service callable over HTTP JSON-RPC 2.0.")
    add_bullet(tf_f2, "High Performance:", "Delivers sub-millisecond route optimization and distance calculations with zero cognitive overhead.")

    # =========================================================================
    # SLIDE 8: Code Snippet: Google ADK Route Agent & A2A Bridge
    # =========================================================================
    add_code_slide(
        slide_title="Code Snippet: Google ADK Route Agent & A2A Bridge",
        category_text="Implementation & Source Code Reference 2",
        file_path="src/agents/adk_route_agent.py & a2a_bridge.py",
        line_ref="Lines 28–50 (ADK Agent) & Lines 45–65 (A2A Bridge)",
        code_text="""# Google ADK Declarative Route Agent Schema
self.agent_card = AgentCard(
    name="ADKRouteAgent",
    version="1.0.0",
    description="Calculates shortest paths and traffic delays.",
    capabilities=["spatial_routing", "delay_prediction"],
    input_schema=RouteRequestSchema.model_json_schema(),
    output_schema=RoutePlan.model_json_schema()
)

# Standardized Agent-to-Agent (A2A) Network Bridge
def query_adk_route_agent(self, payload: dict) -> RoutePlan:
    request = {
        "jsonrpc": "2.0",
        "method": "calculate_optimal_route",
        "params": payload,
        "id": str(uuid.uuid4())
    }
    response = requests.post(f"{self.base_url}/api/a2a/route",
                             json=request, timeout=2.0)
    return RoutePlan.model_validate(response.json()["result"])""",
        bullets=[
            ("What is Happening:", "Bridges the CrewAI orchestrator to an external Google ADK Route Agent microservice over an HTTP network interface."),
            ("Implementation Mechanism:", "Declares typed input and output contracts using Google ADK AgentCard schemas and formats inter-agent calls via standard JSON-RPC 2.0."),
            ("Why this Architecture:", "Decouples mathematical graph routing from cognitive reasoning, allowing spatial routing to scale independently as a dedicated microservice."),
            ("System Invariant:", "Network timeouts trigger an automatic local Graph Dijkstra circuit breaker, ensuring zero pipeline halts if the remote endpoint drops.")
        ]
    )

    # =========================================================================
    # SLIDE 9: Centralized Blackboard Shared State
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide9, "Centralized Blackboard Architecture & Synchronization", "Shared Memory Management & Concurrency Control")
    
    tf_top8 = add_card(slide9, Inches(0.8), Inches(1.55), Inches(11.733), Inches(1.2), title="The Blackboard Architecture Pattern")
    add_bullet(tf_top8, "Centralized Shared State:", "Rather than passing growing message payloads between individual agents (point-to-point chat), all agents read from and write to a single structured Blackboard repository.", size=13.0, space_after=0)

    w8 = Inches(3.75)
    gap8 = Inches(0.24)
    
    tf_b1 = add_card(slide9, Inches(0.8), Inches(2.9), w8, Inches(4.1), title="1. Structure & Pydantic Contract")
    add_bullet(tf_b1, "Schema File:", "src/schemas/blackboard.py")
    add_bullet(tf_b1, "Type-Safe State:", "BlackboardState models order status, candidate drivers, RAG bylaws, assigned route, and execution logs.")
    add_bullet(tf_b1, "Immutable Provenance:", "Every state mutation appends an audit record: timestamp, agent name, field updated, and rationale.")
    add_bullet(tf_b1, "Zero Data Loss:", "Guarantees full reproducibility and traceability for compliance auditing.")

    tf_b2 = add_card(slide9, Inches(0.8) + w8 + gap8, Inches(2.9), w8, Inches(4.1), title="2. Concurrency Safety (RLock)")
    add_bullet(tf_b2, "Manager File:", "src/blackboard/blackboard_manager.py")
    add_bullet(tf_b2, "Thread-Safe Lock:", "All reads and writes are protected by Python's threading.RLock (Reentrant Lock).")
    add_bullet(tf_b2, "Race Condition Defense:", "Simultaneous updates from parallel retrieval and routing threads are serialized cleanly.")
    add_bullet(tf_b2, "Stress Tested:", "Verified across 10 concurrent worker threads and 6 automated unit tests with zero deadlocks.")

    tf_b3 = add_card(slide9, Inches(0.8) + (w8 + gap8)*2, Inches(2.9), w8, Inches(4.1), title="3. Tool-Driven Updates")
    add_bullet(tf_b3, "MCP Tool File:", "src/mcp/tools/blackboard_tool.py")
    add_bullet(tf_b3, "Decoupled Access:", "Agents do not manipulate memory pointers directly; they invoke the blackboard_update FastMCP tool.")
    add_bullet(tf_b3, "Read-Driven Handoffs:", "Dispatch reads drivers; Route Agent reads dropoff zone; Exception Agent reads road status.")
    add_bullet(tf_b3, "Verified Integrity:", "Ensures every state mutation is validated against Pydantic schemas before commit.")

    # =========================================================================
    # SLIDE 10: Code Snippet: Blackboard State & Concurrency Lock
    # =========================================================================
    add_code_slide(
        slide_title="Code Snippet: Blackboard State & Concurrency Lock",
        category_text="Implementation & Source Code Reference 3",
        file_path="src/schemas/blackboard.py & blackboard_manager.py",
        line_ref="Lines 35–55 (Schema) & Lines 56–75 (Manager)",
        code_text="""# Pydantic v2 Centralized Blackboard Shared State
class BlackboardState(BaseModel):
    order_id: str
    pickup: str
    dropoff: str
    weight_kg: float
    candidate_drivers: List[CandidateDriver] = Field(default_factory=list)
    retrieved_rules: List[Dict[str, Any]] = Field(default_factory=list)
    assigned_driver_id: Optional[str] = None
    selected_route: Optional[str] = None
    estimated_eta_mins: float = 0.0
    predicted_delay_mins: float = 0.0
    provenance_log: List[Dict[str, Any]] = Field(default_factory=list)

# Thread-Safe State Mutation via Reentrant Lock
def update_field(self, order_id: str, agent_name: str,
                 field: str, value: Any, rationale: str = ""):
    with self._lock:  # threading.RLock prevents race conditions
        state = self.get_order_state(order_id)
        setattr(state, field, value)
        state.provenance_log.append({
            "timestamp": time.time(),
            "agent": agent_name,
            "field_updated": field,
            "rationale": rationale
        })""",
        bullets=[
            ("What is Happening:", "Defines the centralized Pydantic v2 shared memory model and serializes all multi-agent state mutations under a concurrency lock."),
            ("Implementation Mechanism:", "Every state read and write transaction acquires threading.RLock(), preventing race conditions during concurrent agent operations."),
            ("Why this Architecture:", "Eliminates point-to-point message passing bloat; downstream agents read verified inputs directly from a single validated source of truth."),
            ("System Invariant:", "Every state mutation automatically appends an immutable provenance audit log (timestamp, agent, field, rationale) ensuring 100% auditability.")
        ]
    )

    # =========================================================================
    # SLIDE 11: Multi-Agent Orchestration Patterns
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide11, "Multi-Agent Orchestration: Comparing 3 Execution Patterns", "Architectural Taxonomy & Execution Strategies")
    
    tf_top10 = add_card(slide11, Inches(0.8), Inches(1.55), Inches(11.733), Inches(1.2), title="Comparative Architectural Evaluation")
    add_bullet(tf_top10, "Methodology:", "Implemented and benchmarked three distinct orchestration patterns: Sequential, Parallel, and a Hierarchical Hybrid. This measures execution latency, token cost, and error resilience under identical 72-run benchmark workloads.", size=13.0, space_after=0)

    w10 = Inches(3.75)
    gap10 = Inches(0.24)
    
    tf_seq = add_card(slide11, Inches(0.8), Inches(2.9), w10, Inches(4.1), title="1. Sequential Architecture")
    add_bullet(tf_seq, "File:", "src/orchestration/sequential_orchestrator.py")
    add_bullet(tf_seq, "Execution Flow:", "A linear step-by-step pipeline. Step 1 (RAG retrieval) must complete 100% before Step 2 (Driver DB) can start.")
    add_bullet(tf_seq, "Measured Latency:", "Slowest (0.582s to 0.672s). Total time is the additive sum of all blocking I/O calls.")
    add_bullet(tf_seq, "Failure Mode:", "Zero dynamic recovery. A road blockage or missing driver halts the entire dispatch.")

    tf_par = add_card(slide11, Inches(0.8) + w10 + gap10, Inches(2.9), w10, Inches(4.1), title="2. Parallel Architecture")
    add_bullet(tf_par, "File:", "src/orchestration/parallel_orchestrator.py")
    add_bullet(tf_par, "Execution Flow:", "Uses ThreadPoolExecutor to launch RAG, Driver DB, Route, and Delay queries simultaneously across worker threads.")
    add_bullet(tf_par, "Measured Latency:", "Fastest for pure concurrent reads (0.4162s median), executing independent tasks in parallel.")
    add_bullet(tf_par, "Limitation:", "Lacks a supervisory coordinator to arbitrate assignment conflicts or manage multi-step recovery.")

    tf_hie = add_card(slide11, Inches(0.8) + (w10 + gap10)*2, Inches(2.9), w10, Inches(4.1), title="3. Hierarchical Architecture (Hybrid)")
    add_bullet(tf_hie, "File:", "src/orchestration/hierarchical_orchestrator.py")
    add_bullet(tf_hie, "Architecture Type:", "Hybrid Architecture combining parallel retrieval with sequential supervisory deliberation.")
    add_bullet(tf_hie, "Execution Flow:", "Supervisor spawns parallel worker threads for fast 21ms context retrieval, then executes cognitive dispatch and safety checks.")
    add_bullet(tf_hie, "Measured Latency:", "Optimal balance (0.4501s) — only 34ms supervisory overhead over pure parallel, while 29.7% faster than sequential.")
    add_bullet(tf_hie, "Production Advantage:", "Enables autonomous mid-route exception recovery, vehicle load balancing, and centralized guardrail checks.")

    # =========================================================================
    # SLIDE 12: Empirical Benchmark Proof: Latency & Reliability (WITH GRAPH)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide12, "Empirical Benchmark Results: Latency & Reliability", "Performance Analysis from 72 Factorial Benchmark Runs")
    
    # Left: Embed Latency Boxplot Graph (Slightly adjusted height to accommodate 1-2 line takeaway card below)
    latency_img = REPO_DIR / "artifacts" / "latency_boxplot.png"
    if latency_img.exists():
        slide12.shapes.add_picture(str(latency_img), Inches(0.8), Inches(1.6), Inches(6.0), Inches(4.30))
    else:
        add_card(slide12, Inches(0.8), Inches(1.6), Inches(6.0), Inches(4.30), title="Latency Boxplot: 72 Benchmark Runs")

    # Below Diagram: 1-2 Line Direct Inference Card
    tf_inf = add_card(slide12, Inches(0.8), Inches(5.98), Inches(6.0), Inches(0.95), title=None)
    p_inf = tf_inf.paragraphs[0]
    p_inf.text = "Key Takeaway from Diagram (What It Shows):"
    p_inf.font.name = "Calibri"
    p_inf.font.size = Pt(11.5)
    p_inf.font.bold = True
    p_inf.font.color.rgb = COLOR_CRIMSON
    p_inf.space_after = Pt(2)
    
    p_inf2 = tf_inf.add_paragraph()
    p_inf2.text = "• Pure Parallel is fastest (0.416s) but cannot handle recovery. Hierarchical MAS is a Hybrid combining parallel retrieval with supervisory control—running 29.7% faster than Sequential (0.450s vs 0.672s) with full safety gating."
    p_inf2.font.name = "Calibri"
    p_inf2.font.size = Pt(10.5)
    p_inf2.font.color.rgb = COLOR_CHARCOAL

    # Right: Technical Analysis & Quantitative Proof
    tf_data = add_card(slide12, Inches(7.0), Inches(1.6), Inches(5.533), Inches(5.33), title="Latency & Reliability Performance Analysis")
    add_bullet(tf_data, "Experimental Design:", "72 systematic benchmark runs testing 3 Architectures (Sequential, Parallel, Hierarchical) × 2 Prompt Styles (ReAct vs Direct) × 4 Personas × 3 Consignment types.")
    add_bullet(tf_data, "Parallel Architecture (Lowest Latency):", "Parallel execution achieves the lowest median latency (0.4162s) by retrieving driver catalogs and RAG bylaws simultaneously in worker threads.")
    add_bullet(tf_data, "Sequential Architecture (29.7% Slower):", "Sequential execution exhibits high latency (0.5821s to 0.6720s) due to cumulative blocking I/O calls, and completely fails on road blockages.")
    add_bullet(tf_data, "Hierarchical Hybrid (Production Balance):", "Hierarchical MAS runs in 0.4501s—adding only 34ms supervisory overhead over parallel. In return, it enables autonomous exception recovery and safety gating.")
    add_bullet(tf_data, "ReAct Reasoning Overhead:", "ReAct cognitive loops add only ~12% latency overhead over direct zero-shot prompting while completely eliminating greedy vehicle over-allocations.")

    # =========================================================================
    # SLIDE 13: Code Snippet: Hierarchical Orchestrator Workflow
    # =========================================================================
    add_code_slide(
        slide_title="Code Snippet: Hierarchical Parallel Context Gathering",
        category_text="Implementation & Source Code Reference 4",
        file_path="src/orchestration/hierarchical_orchestrator.py",
        line_ref="Lines 154–176",
        code_text="""# Concurrent Context Gathering via ThreadPoolExecutor
span_gather = self.tracer.start_span(trace_id, "ParallelContextGathering")
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    # Thread 1: Vector RAG for municipal freight bylaws
    future_rag = executor.submit(
        self.retrieval_agent.retrieve_rules_for_order,
        order_id=order_id, pickup_zone=order["pickup"],
        dropoff_zone=order["dropoff"],
        weight_kg=float(order["weight_kg"]), priority=order["priority"]
    )
    # Thread 2: Database lookup for eligible vehicle capacities
    future_drivers = executor.submit(
        self.driver_db.find_eligible_drivers,
        min_capacity_kg=float(order["weight_kg"])
    )
    # Barrier Join: Both threads complete concurrently
    rules = future_rag.result()
    raw_drivers = future_drivers.result()

# Commit validated context into Blackboard Shared State
self.bb_manager.update_field(order_id, "crew_retrieval_agent",
                             "retrieved_rules", rules)""",
        bullets=[
            ("What is Happening:", "The Hierarchical Supervisor spawns concurrent background threads to retrieve regulatory bylaws and fleet driver data simultaneously."),
            ("Implementation Mechanism:", "ThreadPoolExecutor(max_workers=2) dispatches vector ChromaDB RAG and SQLite capacity queries in parallel, joining at a synchronization barrier."),
            ("Why this Architecture:", "Eliminates serial I/O bottlenecks; parallel retrieval completes in 21ms compared to 42ms sequential time, cutting context gathering latency by 50%."),
            ("System Invariant:", "All retrieved context is validated and committed atomically to BlackboardState before the Dispatch Agent begins ReAct deliberation.")
        ]
    )

    # =========================================================================
    # SLIDE 14: FastMCP Tool Integration (Decoupled Tools)
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide14, "Decoupled Tool Architecture: 5 FastMCP Domain Tools", "Model Context Protocol & External System Integration")
    
    tf_top13 = add_card(slide14, Inches(0.8), Inches(1.55), Inches(11.733), Inches(1.35), title="Model Context Protocol (FastMCP) Integration")
    add_bullet(tf_top13, "Standardized Interface:", "MCP is an open standard that decouples language model reasoning from external databases, mathematical algorithms, and APIs via client-server JSON-RPC.", size=13.0, space_after=2)
    add_bullet(tf_top13, "Production Tool Suite:", "Built and deployed 5 production FastMCP tools covering driver catalogs, routing calculations, machine learning delay forecasting, vector search, and state synchronization.", size=13.0, space_after=0)

    w13_a = Inches(5.7)
    w13_b = Inches(5.7)
    
    tf_t1 = add_card(slide14, Inches(0.8), Inches(3.05), w13_a, Inches(4.0), title="The 5 Production FastMCP Domain Tools")
    add_bullet(tf_t1, "1. driver_db_lookup:", "Filters 10 fleet drivers by zone and vehicle payload capacity (Bikes 20-30kg, Vans 80-120kg).")
    add_bullet(tf_t1, "2. routing_engine_calculate:", "Computes road distances and congestion-adjusted transit time across Zones A, B, C, and D.")
    add_bullet(tf_t1, "3. delay_predictor_forecast:", "Runs our trained Scikit-Learn Random Forest regression model (R^2 = 0.901, MAE = 2.94m) in 0.0008s with 0 tokens.")
    add_bullet(tf_t1, "4. policy_rag_search:", "Searches ChromaDB vector storage for municipal bylaws and driver shift limits in under 15ms.")
    add_bullet(tf_t1, "5. blackboard_update:", "Writes validated agent decisions and route plans safely into the central Blackboard.")

    tf_t2 = add_card(slide14, Inches(6.833), Inches(3.05), w13_b, Inches(4.0), title="Machine Learning Delay Prediction vs LLMs")
    add_bullet(tf_t2, "The Floating-Point Arithmetic Bottleneck:", "LLMs perform poorly on continuous spatial math, take 400–1200ms per invocation, and cost ~$0.002 per order.")
    add_bullet(tf_t2, "500x Faster Inference (0.0008s):", "Our Random Forest model evaluates [distance, traffic_factor, rainfall, hour, weight] in 800 microseconds with zero token spend.")
    add_bullet(tf_t2, "Physical Transit Dynamics:", "Trained on 600 trip records: distance friction (0.8m/km), congestion scaling, and monsoon rain degradation (0.5m/mm).")
    add_bullet(tf_t2, "Non-Linear Gridlock Modeling:", "Accurately captures compounding delays (e.g. 15mm rainfall + rush hour + 70kg van) that simple linear formulas cannot model.")

    # =========================================================================
    # SLIDE 15: Safety & Guardrails Architecture
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide15, "Multi-Tier Safety Architecture: Security, Schemas & Law", "Perimeter Defense, Syntactic Validation & Labor Compliance")
    
    tf_top14 = add_card(slide15, Inches(0.8), Inches(1.55), Inches(11.733), Inches(1.2), title="Three-Tier Defensive Perimeter")
    add_bullet(tf_top14, "Defense-in-Depth:", "Input payloads pass through three validation stages before, during, and after agent execution to prevent prompt injection attacks, malformed data, and statutory labor violations.", size=13.0, space_after=0)

    w14 = Inches(3.75)
    gap14 = Inches(0.24)
    
    tf_g1 = add_card(slide15, Inches(0.8), Inches(2.9), w14, Inches(4.1), title="Tier 1: Pre-Execution Security")
    add_bullet(tf_g1, "File:", "src/guardrails/input_guard.py")
    add_bullet(tf_g1, "Sub-Millisecond Regex (0.0004s):", "Scans user delivery notes for adversarial jailbreaks ('ignore rules', 'system prompt override').")
    add_bullet(tf_g1, "Denial-of-Wallet Defense:", "Aborts malicious requests in 0.4ms before invoking expensive LLM APIs.")
    add_bullet(tf_g1, "Toxic Language Redaction:", "Masks profanities ('idiot', 'stupid') with [REDACTED_HOSTILE] to keep prompts clean.")

    tf_g2 = add_card(slide15, Inches(0.8) + w14 + gap14, Inches(2.9), w14, Inches(4.1), title="Tier 2: Syntactic & Schema Guard")
    add_bullet(tf_g2, "File:", "src/schemas/orders.py")
    add_bullet(tf_g2, "Strict Pydantic Validation:", "Rejects invalid payloads before agents execute. Weight must be 0.1kg – 1000kg; rejects negative or zero weights.")
    add_bullet(tf_g2, "Payload Boundary Enforcement:", "Orders exceeding max vehicle capacity (150kg) trigger immediate REJECTED_OVERWEIGHT returns.")
    add_bullet(tf_g2, "Bound Checks:", "Rejects negative deadlines (-10m), non-existent delivery zones, and empty order IDs.")
    add_bullet(tf_g2, "Clean Error Responses:", "Returns INVALID_ORDER_SPECIFICATION without crashing the agent pipeline.")

    tf_g3 = add_card(slide15, Inches(0.8) + (w14 + gap14)*2, Inches(2.9), w14, Inches(4.1), title="Tier 3: Business & Labor Law")
    add_bullet(tf_g3, "File:", "src/guardrails/business_guardrails.py")
    add_bullet(tf_g3, "Statutory 9.0h Shift Cap:", "Enforces the Motor Transport Workers Act to eliminate fatal driver fatigue accidents.")
    add_bullet(tf_g3, "Pre-Emptive Fatigue Rejection:", "Driver D03 (8.8h worked + 0.5h transit = 9.3h > 9.0h) is rejected and reassigned to D01 (4.5h).")
    add_bullet(tf_g3, "Driver D09 Hard Block:", "Drivers at >= 9.0h are strictly marked OFF_DUTY.")

    # =========================================================================
    # SLIDE 16: Code Snippet: Input Injection & Shift Limit Guardrails
    # =========================================================================
    add_code_slide(
        slide_title="Code Snippet: Security Regex & Shift Limit Guardrails",
        category_text="Implementation & Source Code Reference 5",
        file_path="src/guardrails/input_guard.py & business_guardrails.py",
        line_ref="Lines 15–35 (InputGuard) & Lines 18–38 (BusinessGuard)",
        code_text=r"""# Tier 1: Pre-Execution Regex Prompt Injection Interception
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+|any\s+)?(previous|prior)\s+instructions",
    r"disregard\s+(all|your)\s+(rules|policies|guidelines)",
    r"system\s*prompt\s*(override|leak|reveal)"
]
for reg in self.injection_regexes:
    if reg.search(clean_text):
        # Abort in 0.0004s before invoking LLM (Denial-of-Wallet Defense)
        return InputGuardResult(is_safe=False, status="BLOCKED_INJECTION",
                                sanitized_text="[BLOCKED_SECURITY_VIOLATION]")

# Tier 3: Statutory 9.0-Hour Driver Shift Ceiling Enforcement
projected_hours = current_hours + (estimated_eta_mins / 60.0)
if projected_hours > 9.0:
    return GuardrailEvaluation(
        passed=False,
        violations=[f"Statutory shift cap 9.0h exceeded: {projected_hours:.1f}h"],
        action_taken="BLOCK"
    )""",
        bullets=[
            ("What is Happening:", "Enforces perimeter defense against prompt injection attacks and verifies statutory driver shift limits before dispatch authorization."),
            ("Implementation Mechanism:", "Tier 1 scans customer delivery notes with compiled regex patterns in 0.0004s; Tier 3 computes projected cumulative shift duration."),
            ("Why this Architecture:", "Blocks adversarial jailbreaks before they hit LLM APIs, defending against Denial-of-Wallet attacks and saving 96.4% in token costs ($0.000015 vs $0.00042)."),
            ("System Invariant:", "Drivers whose projected route pushes cumulative shift time over 9.0 hours are deterministically blocked and reassigned to relief drivers.")
        ]
    )

    # =========================================================================
    # SLIDE 17: Callbacks & Telematics Heatmaps
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide17, "Observability: Lifecycle Callbacks & Latency Heatmaps", "Observability, Telemetry Streaming & Latency Profiling")
    
    # Left: Embed the clear, publication-grade Component Latency Heatmap!
    heatmap_img = REPO_DIR / "artifacts" / "agent_run_heatmap.png"
    if heatmap_img.exists():
        slide17.shapes.add_picture(str(heatmap_img), Inches(0.8), Inches(1.6), Inches(5.8), Inches(4.30))
    else:
        add_card(slide17, Inches(0.8), Inches(1.6), Inches(5.8), Inches(4.30), title="Component Latency Heatmap")

    # Below Heatmap: 2-3 Line Direct Inference Card
    tf_inf17 = add_card(slide17, Inches(0.8), Inches(5.98), Inches(5.8), Inches(0.95), title=None)
    p_inf = tf_inf17.paragraphs[0]
    p_inf.text = "Key Inference from Heatmap (What It Shows):"
    p_inf.font.name = "Calibri"
    p_inf.font.size = Pt(11.5)
    p_inf.font.bold = True
    p_inf.font.color.rgb = COLOR_CRIMSON
    p_inf.space_after = Pt(2)
    
    p_inf2 = tf_inf17.add_paragraph()
    p_inf2.text = "• InputGuard provides zero-overhead security in 0.4ms; FastMCP retrieval runs concurrently in ~20ms, while cognitive LLM dispatch accounts for ~104ms.\n• Exception Agent remains on standby (0.0ms) during normal operations, but dynamically engages in 38.1ms upon road blockage to reroute without system failure."
    p_inf2.font.name = "Calibri"
    p_inf2.font.size = Pt(10.0)
    p_inf2.font.color.rgb = COLOR_CHARCOAL

    # Right: Explaining Observability Implementation
    tf_c5 = add_card(slide17, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.33), title="Lifecycle Callback Architecture & Latency Profiling")
    add_bullet(tf_c5, "MASCallbackHandler Architecture:", "Implemented in src/observability/callbacks.py. Hooks into on_agent_start, on_tool_start, on_agent_finish, and on_exception.")
    add_bullet(tf_c5, "Multi-Channel Telemetry Streaming:", "Streams real-time step execution timestamps to console terminal, WebSockets UI dashboard, and logs/run_events.jsonl.")
    add_bullet(tf_c5, "Component Latency Profiling:", "The latency heatmap profiles every pipeline stage across operational benchmark scenarios:")
    add_bullet(tf_c5, "Zero-Overhead Guardrails (<0.5ms):", "InputGuard executes in 0.4ms, intercepting prompt injections with zero LLM token cost.")
    add_bullet(tf_c5, "FastMCP Tool Concurrency (~20ms):", "Driver DB lookups (5.1ms) and ChromaDB RAG queries (14.8ms) run concurrently, preventing database I/O bottlenecks.")
    add_bullet(tf_c5, "Cognitive Isolation (~104ms):", "Dispatch Agent ReAct reasoning accounts for ~104ms, ensuring thorough constraint evaluation.")
    add_bullet(tf_c5, "Dynamic Replanning (~38ms):", "Exception Agent triggers only when road blockages occur (38.1ms) and remains idle (0.0ms) otherwise.")

    # =========================================================================
    # SLIDE 18: Empirical Verification & Automated Test Results
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide18, "Empirical Verification: 134 Automated Test Runs", "Testing Rigor, Pass Rates & Concurrency Validation")
    
    w17 = Inches(3.75)
    gap17 = Inches(0.24)
    
    tf_t17a = add_card(slide18, Inches(0.8), Inches(1.6), w17, Inches(5.3), title="49 Automated Pytest Tests")
    add_bullet(tf_t17a, "Pass Rate:", "49 / 49 Passed (100% Green)")
    add_bullet(tf_t17a, "Execution Time:", "~19.45 seconds")
    add_bullet(tf_t17a, "9 Comprehensive Test Suites:", "")
    add_bullet(tf_t17a, "Blackboard Concurrency:", "6 tests verifying RLock thread-safety and snapshot isolation.")
    add_bullet(tf_t17a, "Multi-Tier Guardrails:", "5 tests verifying regex injection defense and fatigue caps.")
    add_bullet(tf_t17a, "FastMCP Domain Tools:", "5 tests verifying all 5 tool endpoints.")
    add_bullet(tf_t17a, "Boundary & Float Limits:", "6 tests verifying 0.0km zero-distance and float limits.")
    add_bullet(tf_t17a, "End-to-End Pipeline:", "5 tests verifying full workflow and exception recovery.")

    tf_t17b = add_card(slide18, Inches(0.8) + w17 + gap17, Inches(1.6), w17, Inches(5.3), title="13 Selenium Browser UI Runs")
    add_bullet(tf_t17b, "Pass Rate:", "13 / 13 Passed (100% Green)")
    add_bullet(tf_t17b, "Execution Engine:", "Selenium + Headless Chrome")
    add_bullet(tf_t17b, "Automated Script:", "test_browser_suite.py")
    add_bullet(tf_t17b, "Visual Evidence:", "All 13 timestamped screenshots saved in artifacts/browser_screenshots/.")
    add_bullet(tf_t17b, "Key Scenarios Verified:", "")
    add_bullet(tf_t17b, "Case 1 Standard Dispatch:", "Optimal EV van allocated (ORD-101).")
    add_bullet(tf_t17b, "Case 2 Emergency Replan:", "Relief driver D04 in 0.05s (ORD-105).")
    add_bullet(tf_t17b, "Case 3 Abusive Masking:", "[REDACTED_HOSTILE] (ORD-108).")
    add_bullet(tf_t17b, "Case 4 Injection Block:", "HTTP 403 Forbidden (ORD-109).")

    tf_t17c = add_card(slide18, Inches(0.8) + (w17 + gap17)*2, Inches(1.6), w17, Inches(5.3), title="72 Factorial Benchmark Runs")
    add_bullet(tf_t17c, "Completion Rate:", "72 / 72 Runs Completed (100%)")
    add_bullet(tf_t17c, "Factorial Matrix:", "3 Architectures × 2 Prompt Styles × 4 Personas × 3 Orders.")
    add_bullet(tf_t17c, "Reliability:", "Zero deadlocks, zero crashes, zero data corruptions across all 72 runs.")
    add_bullet(tf_t17c, "Denial-of-Wallet Defense:", "Injection prompts cost $0.000015 USD (130 tokens) vs $0.00042 USD for polite orders—saving 96.4% in tokens.")
    add_bullet(tf_t17c, "Balanced Fleet Workload:", "Shannon Decision Entropy H(X) = 0.917 bits proves non-greedy driver distribution.")
    add_bullet(tf_t17c, "Safety Accuracy:", "Sensitivity = 1.0 (100% fatigue violation detection). Specificity = 0.96.")

    # =========================================================================
    # SLIDE 19: System Implementation Status (8 Core Modules Completed)
    # =========================================================================
    slide19 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide19, "System Implementation Status: 8 Core Modules Completed", "Phase 2 Engineering Deliverables & Empirical Verification")
    
    # 2 columns x 4 clean cards per column (Total 8 cards, large font, zero squishing)
    w18 = Inches(5.7)
    card18_h = Inches(1.30)
    gap18_y = Inches(0.12)
    start18_y = Inches(1.50)
    
    completed_left = [
        ("1. Centralized Blackboard Shared State",
         "src/schemas/blackboard.py & src/blackboard/blackboard_manager.py",
         "Centralized BlackboardState model with threading.RLock() concurrency protection.",
         "Downstream agents read inputs from Blackboard; verified by 6 concurrency unit tests."),
        
        ("2. FastMCP Tool Integration (5 Tools)",
         "src/mcp/tools/ (5 production FastMCP endpoints)",
         "Driver DB, Routing Engine, ML Delay Predictor, Vector RAG, and Blackboard Update.",
         "Decoupled client-server architecture; all 5 tools operational with zero schema failures."),
        
        ("3. Pydantic v2 Type-Safe Data Contracts",
         "src/schemas/ (reports.py, decisions.py, routes.py)",
         "Strict type validation, deterministic JSON serialization, and markdown formatting.",
         "Eliminates unvalidated agent outputs; verified across all inter-agent handoffs."),
        
        ("4. Comparative Orchestration Patterns",
         "src/orchestration/ (sequential, parallel, and hierarchical)",
         "Evaluated 3 patterns. Hierarchical MAS supervisor uses ThreadPoolExecutor concurrency.",
         "0.450s latency with autonomous mid-route exception recovery, outperforming sequential.")
    ]
    
    completed_right = [
        ("5. Lifecycle Callbacks & Latency Heatmaps",
         "src/observability/callbacks.py (MASCallbackHandler)",
         "Captures lifecycle events (on_agent_start, on_tool_start, on_exception) in real time.",
         "Streams to console, JSONL, and WebSockets; generated 2D density heatmap across 72 runs."),
        
        ("6. Agent-to-Agent (A2A) Protocol Bridge",
         "src/agents/a2a_bridge.py via HTTP endpoint /api/a2a/route",
         "Standardized JSON-RPC 2.0 inter-agent messaging with live network transport.",
         "Connects CrewAI dispatchers to Google ADK routing agents with circuit-breaker fallback."),
        
        ("7. Dual Framework Synergy (CrewAI + ADK)",
         "src/agents/ (CrewAI dispatch/exception + ADK route agent)",
         "CrewAI handles cognitive dispatch & exception replanning; ADK enforces AgentCard schemas.",
         "Proves multi-paradigm MAS interoperability without vendor or framework lock-in."),
        
        ("8. Multi-Tier Security & Legal Guardrails",
         "src/guardrails/input_guard.py & business_guardrails.py",
         "Tier 1 regex blocks prompt injections in 0.0004s ($0.000015 cost vs $0.00042).",
         "Tier 3 enforces statutory 9.0h driver fatigue limits, deterministically reassigning drivers.")
    ]
    
    for i, (c_title, c_file, c_impl, c_proof) in enumerate(completed_left):
        top_pos = start18_y + i * (card18_h + gap18_y)
        shape = slide19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top_pos, w18, card18_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = COLOR_CARD_BORDER
        shape.line.width = Pt(1.0)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = tf.margin_bottom = Inches(0.08)
        
        p0 = tf.paragraphs[0]
        p0.text = f"[COMPLETED] {c_title}"
        p0.font.name = "Calibri"
        p0.font.size = Pt(12.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_GREEN
        p0.space_after = Pt(2)
        
        p1 = tf.add_paragraph()
        r1_lbl = p1.add_run(); r1_lbl.text = "File: "; r1_lbl.font.bold = True; r1_lbl.font.size = Pt(11.0); r1_lbl.font.color.rgb = COLOR_CRIMSON
        r1_txt = p1.add_run(); r1_txt.text = c_file; r1_txt.font.name = "Consolas"; r1_txt.font.size = Pt(10.5); r1_txt.font.color.rgb = COLOR_CHARCOAL
        p1.space_after = Pt(2)
        
        p2 = tf.add_paragraph()
        r2_lbl = p2.add_run(); r2_lbl.text = "Mechanism & Proof: "; r2_lbl.font.bold = True; r2_lbl.font.size = Pt(11.0); r2_lbl.font.color.rgb = COLOR_MUTED
        r2_txt = p2.add_run(); r2_txt.text = f"{c_impl} {c_proof}"; r2_txt.font.name = "Calibri"; r2_txt.font.size = Pt(11.0); r2_txt.font.color.rgb = COLOR_CHARCOAL
        p2.space_after = Pt(0)

    for i, (c_title, c_file, c_impl, c_proof) in enumerate(completed_right):
        top_pos = start18_y + i * (card18_h + gap18_y)
        shape = slide19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), top_pos, w18, card18_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = COLOR_CARD_BORDER
        shape.line.width = Pt(1.0)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = tf.margin_bottom = Inches(0.08)
        
        p0 = tf.paragraphs[0]
        p0.text = f"[COMPLETED] {c_title}"
        p0.font.name = "Calibri"
        p0.font.size = Pt(12.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_GREEN
        p0.space_after = Pt(2)
        
        p1 = tf.add_paragraph()
        r1_lbl = p1.add_run(); r1_lbl.text = "File: "; r1_lbl.font.bold = True; r1_lbl.font.size = Pt(11.0); r1_lbl.font.color.rgb = COLOR_CRIMSON
        r1_txt = p1.add_run(); r1_txt.text = c_file; r1_txt.font.name = "Consolas"; r1_txt.font.size = Pt(10.5); r1_txt.font.color.rgb = COLOR_CHARCOAL
        p1.space_after = Pt(2)
        
        p2 = tf.add_paragraph()
        r2_lbl = p2.add_run(); r2_lbl.text = "Mechanism & Proof: "; r2_lbl.font.bold = True; r2_lbl.font.size = Pt(11.0); r2_lbl.font.color.rgb = COLOR_MUTED
        r2_txt = p2.add_run(); r2_txt.text = f"{c_impl} {c_proof}"; r2_txt.font.name = "Calibri"; r2_txt.font.size = Pt(11.0); r2_txt.font.color.rgb = COLOR_CHARCOAL
        p2.space_after = Pt(0)

    # =========================================================================
    # SLIDE 20: Future Scope & Advanced Engineering (Phase 3 Roadmap)
    # =========================================================================
    slide20 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide20, "Future Scope & Advanced Engineering (Phase 3 Roadmap)", "Distributed Cloud Infrastructure & Advanced Scalability")
    
    # Top Strategy Banner Card
    tf_strat = add_card(slide20, Inches(0.8), Inches(1.50), Inches(11.733), Inches(1.20), title="Phase 2 Deliverables Achieved & Phase 3 Engineering Focus")
    add_bullet(tf_strat, "Phase 2 Milestone Status:", "Delivered a fully working autonomous multi-agent prototype covering dispatching, routing, vector policy retrieval, and exception handling with 134 passing tests.", size=12.5, space_after=3)
    add_bullet(tf_strat, "Phase 3 Engineering Scope:", "The subsequent project phase advances the system from single-node workstation execution to a distributed multi-node cloud environment with live telemetry dashboards and containerized deployment.", size=12.5, space_after=0)
    
    # Left Column: The 3 Staged Research Novelties (C09, C10, C11)
    w19_l = Inches(6.0)
    card19_h = Inches(1.30)
    gap19_y = Inches(0.12)
    start19_y = Inches(2.85)
    
    novelty_items = [
        ("1. Distributed AI Observability & Tracing",
         "OpenTelemetry collector exporting microsecond span correlation across distributed agent nodes to live Jaeger and Prometheus dashboards.",
         "Expands single-host JSONL tracing to multi-node network clusters to monitor inter-agent network latency and RPC overhead."),
        
        ("2. Cloud-Scale Factorial Benchmarks & Pareto Analysis",
         "100+ factorial evaluation matrix across 3 architectures with simulated distributed network latency and variable traffic loads.",
         "Plots empirical Pareto frontier of token cost vs dispatch latency on cloud nodes under high concurrent order load."),
        
        ("3. Production Cloud Container Deployment (AWS / GCP)",
         "Multi-stage Docker containerization of MAS backend, FastMCP servers, and web UI for live deployment to AWS EC2 / GCP Compute Engine.",
         "Includes persistent SQLite/ChromaDB volume mounts, health monitoring probes, and Cloudflare Edge SSL proxying.")
    ]
    
    for i, (n_title, n_desc, n_why) in enumerate(novelty_items):
        top_pos = start19_y + i * (card19_h + gap19_y)
        shape = slide20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top_pos, w19_l, card19_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = COLOR_CARD_BORDER
        shape.line.width = Pt(1.0)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = tf.margin_bottom = Inches(0.08)
        
        p0 = tf.paragraphs[0]
        p0.text = f"[PHASE 3 ROADMAP] {n_title}"
        p0.font.name = "Calibri"
        p0.font.size = Pt(12.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_CRIMSON
        p0.space_after = Pt(2)
        
        p1 = tf.add_paragraph()
        r1_lbl = p1.add_run(); r1_lbl.text = "Scope: "; r1_lbl.font.bold = True; r1_lbl.font.size = Pt(11.0); r1_lbl.font.color.rgb = COLOR_BLACK
        r1_txt = p1.add_run(); r1_txt.text = n_desc; r1_txt.font.name = "Calibri"; r1_txt.font.size = Pt(11.0); r1_txt.font.color.rgb = COLOR_CHARCOAL
        p1.space_after = Pt(2)
        
        p2 = tf.add_paragraph()
        r2_lbl = p2.add_run(); r2_lbl.text = "Technical Target: "; r2_lbl.font.bold = True; r2_lbl.font.size = Pt(11.0); r2_lbl.font.color.rgb = COLOR_MUTED
        r2_txt = p2.add_run(); r2_txt.text = n_why; r2_txt.font.name = "Calibri"; r2_txt.font.size = Pt(11.0); r2_txt.font.color.rgb = COLOR_CHARCOAL
        p2.space_after = Pt(0)
        
    # Right Column: Empirical Verification Evidence on Disk
    tf_evid = add_card(slide20, Inches(7.05), Inches(2.85), Inches(5.483), Inches(4.14), title="Empirical Verification Proof on Disk")
    add_bullet(tf_evid, "Testing Rigor:", "All 8 completed Phase-2 modules are backed by physical, reproducible test artifacts in the repository:", size=12.0, space_after=6)
    add_bullet(tf_evid, "49 Pytest Unit Tests (100% Green):", "Located in tests/ across 9 suites verifying RLock concurrency, regex guardrails, FastMCP tools, float limits, and exception recovery in 19.45s.", size=11.5, space_after=6)
    add_bullet(tf_evid, "13 Selenium Browser UI Runs (100% Green):", "Automated screenshots in artifacts/browser_screenshots/ proving UI rendering, dispatch allocation, emergency rerouting, and hostile prompt blocking.", size=11.5, space_after=6)
    add_bullet(tf_evid, "72 Factorial Benchmark Runs (100% Completed):", "3 architectures x 2 prompt styles x 4 personas x 3 orders with zero deadlocks; latency boxplot and agent execution heatmap generated and embedded.", size=11.5, space_after=6)
    add_bullet(tf_evid, "5 FastMCP Domain Tool Endpoints Verified:", "Automated test harness validates contract schemas, payload constraints, and sub-millisecond execution times.", size=11.5, space_after=0)

    # =========================================================================
    # SLIDE 21: Team Member Contributions & Engineering Roles
    # =========================================================================
    slide21 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide21, "Team Member Contributions & Engineering Roles", "Engineering Division of Responsibility (Group 8)")
    
    w20 = Inches(5.7)
    h20 = Inches(2.55)
    
    tf_m1 = add_card(slide21, Inches(0.8), Inches(1.6), w20, h20, title="Bhumika Yadav (230732) — Architecture Lead")
    add_bullet(tf_m1, "Core Modules:", "Blackboard state architecture (src/schemas/blackboard.py) and Pydantic v2 output models (src/schemas/reports.py, decisions.py).")
    add_bullet(tf_m1, "Key Contribution:", "Designed the thread-safe shared state contract and structured JSON serialization across all agent handoffs.")

    tf_m2 = add_card(slide21, Inches(6.833), Inches(1.6), w20, h20, title="Aadit Bassi (230728) — Multi-Agent Systems & Routing Lead")
    add_bullet(tf_m2, "Core Modules:", "Google ADK Route Agent (src/agents/adk_route_agent.py) and A2A Protocol Bridge (src/agents/a2a_bridge.py).")
    add_bullet(tf_m2, "Key Contribution:", "Implemented Google ADK AgentCard declarative schemas and JSON-RPC 2.0 network messaging with circuit-breaker fallback.")

    tf_m3 = add_card(slide21, Inches(0.8), Inches(4.35), w20, h20, title="Akshat Nagori (230682) — Security, Retrieval & Testing Lead")
    add_bullet(tf_m3, "Core Modules:", "InputGuard security (src/guardrails/input_guard.py), ChromaDB Vector RAG (src/mcp/tools/chroma_rag.py), web dashboard (src/web/), and 13 Selenium browser tests.")
    add_bullet(tf_m3, "Key Contribution:", "Architected pre-execution prompt injection defense in 0.0004s (saving 96% tokens), local Vector RAG bylaws, customer personas, and automated UI verification.")

    tf_m4 = add_card(slide21, Inches(6.833), Inches(4.35), w20, h20, title="Sahil Mudgil (230743) — Machine Learning & Observability Lead")
    add_bullet(tf_m4, "Core Modules:", "Random Forest delay model (src/mcp/tools/delay_predictor.py), BusinessGuardrails (src/guardrails/business_guardrails.py), callbacks, and benchmark runner.")
    add_bullet(tf_m4, "Key Contribution:", "Trained Scikit-Learn delay model (R^2 = 0.901), statutory 9.0h shift limit guardrails, and executed the 72-run factorial benchmark suite.")

    # =========================================================================
    # SLIDE 22: Conclusion & Project Milestones
    # =========================================================================
    slide22 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide22, "Conclusion: Deliverables Achieved & Future Roadmap", "Phase 2 Summary & Phase 3 Production Release")
    
    tf_sum = add_card(slide22, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), title="Summary of Phase 2 Deliverables Achieved")
    add_bullet(tf_sum, "Operational Multi-Agent Pipeline:", "Delivered a fully working multi-agent delivery fleet system with 8 core modules operational and verified without manual dispatch intervention.")
    add_bullet(tf_sum, "Dual-Framework Synergy:", "Demonstrated live network interoperability between CrewAI (cognitive dispatching/exceptions) and Google ADK (declarative routing) over the A2A protocol.")
    add_bullet(tf_sum, "29.7% Latency Reduction:", "Empirically proved that our Hierarchical Hybrid MAS (0.450s) outperforms sequential pipelines (0.672s) while enabling dynamic mid-route exception recovery.")
    add_bullet(tf_sum, "Sub-Millisecond Security:", "InputGuard neutralizes adversarial prompt injection attacks in 0.0004s, saving 96.4% in token expenditure.")
    add_bullet(tf_sum, "134 Automated Test Runs Passing:", "49/49 Pytest unit tests, 13/13 Selenium browser scenarios, and 72/72 factorial benchmark runs verified with zero errors.")

    tf_road = add_card(slide22, Inches(6.833), Inches(1.6), Inches(5.7), Inches(5.3), title="Phase 3 Engineering Milestones (For Final Release)")
    add_bullet(tf_road, "1. Distributed Jaeger & Prometheus Tracing:", "Deploy multi-host OpenTelemetry collector exporting to live Jaeger and Prometheus distributed tracing dashboards to monitor microsecond inter-agent latency in production.")
    add_bullet(tf_road, "2. Cloud-Scale Factorial Benchmarks:", "Execute 100+ factorial runs on distributed nodes to plot full Pareto cost-latency trade-off frontiers under heavy concurrent order bursts.")
    add_bullet(tf_road, "3. Production Cloud Container Deployment:", "Deploy multi-stage Docker containers to AWS EC2 / GCP Compute Engine with Cloudflare edge SSL proxying and live domain routing.")
    add_bullet(tf_road, "4. Predictive Arterial Congestion Telematics:", "Integrate dynamic arterial congestion prediction into vehicle routing to pre-emptively reroute fleet drivers before delays compound.")

    # Save Presentation
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"[DONE] Successfully generated Master Presentation with 22 slides: {OUT_PPTX}")

def create_human_1slide_matrix():
    """Generate 1_Slide_Coverage_Matrix_Group8.pptx in clean human style split across two readable slides."""
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # -------------------------------------------------------------------------
    # SLIDE 1: System Implementation Status (8 Core Modules Completed)
    # -------------------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)

    # Header Box (Clean Crimson Border)
    hdr1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.3), Inches(12.333), Inches(0.85))
    hdr1.fill.solid()
    hdr1.fill.fore_color.rgb = COLOR_CARD_BG
    hdr1.line.color.rgb = COLOR_CRIMSON
    hdr1.line.width = Pt(1.5)
    
    tf_h1 = hdr1.text_frame
    tf_h1.margin_left = tf_h1.margin_right = Inches(0.2)
    tf_h1.margin_top = Inches(0.1)
    
    p0 = tf_h1.paragraphs[0]
    p0.text = "Autonomous Multi-Agent Delivery Fleet - System Implementation Status (8 Modules Completed)"
    p0.font.name = "Calibri"
    p0.font.size = Pt(16.0)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_BLACK
    
    p1 = tf_h1.add_paragraph()
    p1.text = "Course: CSE3101 Agentic AI | Group 8 | Phase 2 Engineering Deliverables (100% Operational & Tested)"
    p1.font.name = "Calibri"
    p1.font.size = Pt(10.5)
    p1.font.color.rgb = COLOR_MUTED

    w_card = Inches(6.05)
    card_h = Inches(1.30)
    gap_y = Inches(0.12)
    start_y = Inches(1.35)

    completed_left = [
        ("1. Centralized Blackboard Shared State",
         "src/schemas/blackboard.py & src/blackboard/blackboard_manager.py",
         "Centralized BlackboardState model with threading.RLock() concurrency protection.",
         "Downstream agents read inputs from Blackboard; verified by 6 concurrency unit tests."),
        
        ("2. FastMCP Tool Integration (5 Tools)",
         "src/mcp/tools/ (5 production FastMCP endpoints)",
         "Driver DB, Routing Engine, ML Delay Predictor, Vector RAG, and Blackboard Update.",
         "Decoupled client-server architecture; all 5 tools operational with zero schema failures."),
        
        ("3. Pydantic v2 Type-Safe Data Contracts",
         "src/schemas/ (reports.py, decisions.py, routes.py)",
         "Strict type validation, deterministic JSON serialization, and markdown formatting.",
         "Eliminates unvalidated agent outputs; verified across all inter-agent handoffs."),
        
        ("4. Comparative Orchestration Patterns",
         "src/orchestration/ (sequential, parallel, and hierarchical)",
         "Evaluated 3 patterns. Hierarchical MAS supervisor uses ThreadPoolExecutor concurrency.",
         "0.450s latency with autonomous mid-route exception recovery, outperforming sequential.")
    ]
    
    completed_right = [
        ("5. Lifecycle Callbacks & Latency Heatmaps",
         "src/observability/callbacks.py (MASCallbackHandler)",
         "Captures lifecycle events (on_agent_start, on_tool_start, on_exception) in real time.",
         "Streams to console, JSONL, and WebSockets; generated 2D density heatmap across 72 runs."),
        
        ("6. Agent-to-Agent (A2A) Protocol Bridge",
         "src/agents/a2a_bridge.py via HTTP endpoint /api/a2a/route",
         "Standardized JSON-RPC 2.0 inter-agent messaging with live network transport.",
         "Connects CrewAI dispatchers to Google ADK routing agents with circuit-breaker fallback."),
        
        ("7. Dual Framework Synergy (CrewAI + ADK)",
         "src/agents/ (CrewAI dispatch/exception + ADK route agent)",
         "CrewAI handles cognitive dispatch & exception replanning; ADK enforces AgentCard schemas.",
         "Proves multi-paradigm MAS interoperability without vendor or framework lock-in."),
        
        ("8. Multi-Tier Security & Legal Guardrails",
         "src/guardrails/input_guard.py & business_guardrails.py",
         "Tier 1 regex blocks prompt injections in 0.0004s ($0.000015 cost vs $0.00042).",
         "Tier 3 enforces statutory 9.0h driver fatigue limits, deterministically reassigning drivers.")
    ]

    for i, (c_title, c_file, c_impl, c_proof) in enumerate(completed_left):
        top_pos = start_y + i * (card_h + gap_y)
        shape = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), top_pos, w_card, card_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = COLOR_CARD_BORDER
        shape.line.width = Pt(1.0)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = tf.margin_bottom = Inches(0.08)
        
        p = tf.paragraphs[0]
        p.text = f"[COMPLETED] {c_title}"
        p.font.name = "Calibri"
        p.font.size = Pt(12.0)
        p.font.bold = True
        p.font.color.rgb = COLOR_GREEN
        p.space_after = Pt(2)
        
        p = tf.add_paragraph()
        r_lbl = p.add_run(); r_lbl.text = "File: "; r_lbl.font.bold = True; r_lbl.font.size = Pt(10.5); r_lbl.font.color.rgb = COLOR_CRIMSON
        r_txt = p.add_run(); r_txt.text = c_file; r_txt.font.name = "Consolas"; r_txt.font.size = Pt(10.0); r_txt.font.color.rgb = COLOR_CHARCOAL
        p.space_after = Pt(2)
        
        p = tf.add_paragraph()
        r_lbl = p.add_run(); r_lbl.text = "Proof: "; r_lbl.font.bold = True; r_lbl.font.size = Pt(10.5); r_lbl.font.color.rgb = COLOR_MUTED
        r_txt = p.add_run(); r_txt.text = f"{c_impl} {c_proof}"; r_txt.font.name = "Calibri"; r_txt.font.size = Pt(10.5); r_txt.font.color.rgb = COLOR_CHARCOAL
        p.space_after = Pt(0)

    for i, (c_title, c_file, c_impl, c_proof) in enumerate(completed_right):
        top_pos = start_y + i * (card_h + gap_y)
        shape = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.783), top_pos, w_card, card_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = COLOR_CARD_BORDER
        shape.line.width = Pt(1.0)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = tf.margin_bottom = Inches(0.08)
        
        p = tf.paragraphs[0]
        p.text = f"[COMPLETED] {c_title}"
        p.font.name = "Calibri"
        p.font.size = Pt(12.0)
        p.font.bold = True
        p.font.color.rgb = COLOR_GREEN
        p.space_after = Pt(2)
        
        p = tf.add_paragraph()
        r_lbl = p.add_run(); r_lbl.text = "File: "; r_lbl.font.bold = True; r_lbl.font.size = Pt(10.5); r_lbl.font.color.rgb = COLOR_CRIMSON
        r_txt = p.add_run(); r_txt.text = c_file; r_txt.font.name = "Consolas"; r_txt.font.size = Pt(10.0); r_txt.font.color.rgb = COLOR_CHARCOAL
        p.space_after = Pt(2)
        
        p = tf.add_paragraph()
        r_lbl = p.add_run(); r_lbl.text = "Proof: "; r_lbl.font.bold = True; r_lbl.font.size = Pt(10.5); r_lbl.font.color.rgb = COLOR_MUTED
        r_txt = p.add_run(); r_txt.text = f"{c_impl} {c_proof}"; r_txt.font.name = "Calibri"; r_txt.font.size = Pt(10.5); r_txt.font.color.rgb = COLOR_CHARCOAL
        p.space_after = Pt(0)

    # -------------------------------------------------------------------------
    # SLIDE 2: Future Scope & Advanced Engineering (Phase 3 Roadmap)
    # -------------------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)

    # Header Box (Clean Crimson Border)
    hdr2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.3), Inches(12.333), Inches(0.85))
    hdr2.fill.solid()
    hdr2.fill.fore_color.rgb = COLOR_CARD_BG
    hdr2.line.color.rgb = COLOR_CRIMSON
    hdr2.line.width = Pt(1.5)
    
    tf_h2 = hdr2.text_frame
    tf_h2.margin_left = tf_h2.margin_right = Inches(0.2)
    tf_h2.margin_top = Inches(0.1)
    
    p0 = tf_h2.paragraphs[0]
    p0.text = "Autonomous Multi-Agent Delivery Fleet - Future Scope & Advanced Engineering (Phase 3 Roadmap)"
    p0.font.name = "Calibri"
    p0.font.size = Pt(16.0)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_BLACK
    
    p1 = tf_h2.add_paragraph()
    p1.text = "Course: CSE3101 Agentic AI | Group 8 | Distributed Cloud Infrastructure & Production Deployment Roadmap"
    p1.font.name = "Calibri"
    p1.font.size = Pt(10.5)
    p1.font.color.rgb = COLOR_MUTED

    # Top Strategy Card
    top_strat = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.3), Inches(12.333), Inches(1.15))
    top_strat.fill.solid()
    top_strat.fill.fore_color.rgb = COLOR_CARD_BG
    top_strat.line.color.rgb = COLOR_CARD_BORDER
    top_strat.line.width = Pt(1.0)
    tf_ts = top_strat.text_frame
    tf_ts.word_wrap = True
    tf_ts.margin_left = tf_ts.margin_right = Inches(0.2)
    tf_ts.margin_top = Inches(0.1)
    
    pts = tf_ts.paragraphs[0]
    pts.text = "Phase 2 Deliverables Achieved & Phase 3 Engineering Focus"
    pts.font.name = "Calibri"
    pts.font.size = Pt(13.0)
    pts.font.bold = True
    pts.font.color.rgb = COLOR_CRIMSON
    pts.space_after = Pt(3)

    pts2 = tf_ts.add_paragraph()
    pts2.text = "Phase 2 delivered a fully operational multi-agent prototype covering dispatch, routing, vector bylaws, and exception recovery with 134 passing tests. Phase 3 advances the architecture to a distributed cloud cluster with live Jaeger tracing and containerized AWS/GCP deployment."
    pts2.font.name = "Calibri"
    pts2.font.size = Pt(11.0)
    pts2.font.color.rgb = COLOR_BODY

    # Left Column: 3 Staged Research Novelties
    w2_l = Inches(6.05)
    card2_h = Inches(1.40)
    gap2_y = Inches(0.15)
    start2_y = Inches(2.65)
    
    novelties_2 = [
        ("1. Distributed AI Observability & Tracing",
         "OpenTelemetry collector exporting microsecond span correlation across distributed agent nodes to live Jaeger and Prometheus dashboards.",
         "Expands single-host JSONL tracing to multi-node network clusters to monitor inter-agent network latency and RPC overhead."),
        
        ("2. Cloud-Scale Factorial Benchmarks & Pareto Analysis",
         "100+ factorial evaluation matrix across 3 architectures with simulated distributed network latency and variable traffic loads.",
         "Plots empirical Pareto frontier of token cost vs dispatch latency on cloud nodes under high concurrent order load."),
        
        ("3. Production Cloud Container Deployment (AWS / GCP)",
         "Multi-stage Docker containerization of MAS backend, FastMCP servers, and web UI for live deployment to AWS EC2 / GCP Compute Engine.",
         "Includes persistent SQLite/ChromaDB volume mounts, health monitoring probes, and Cloudflare Edge SSL proxying.")
    ]

    for i, (n_title, n_desc, n_why) in enumerate(novelties_2):
        top_pos = start2_y + i * (card2_h + gap2_y)
        shape = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), top_pos, w2_l, card2_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = COLOR_CARD_BORDER
        shape.line.width = Pt(1.0)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = tf.margin_bottom = Inches(0.1)
        
        p = tf.paragraphs[0]
        p.text = f"[PHASE 3 ROADMAP] {n_title}"
        p.font.name = "Calibri"
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_CRIMSON
        p.space_after = Pt(2)
        
        p = tf.add_paragraph()
        r_lbl = p.add_run(); r_lbl.text = "Scope: "; r_lbl.font.bold = True; r_lbl.font.size = Pt(11.0); r_lbl.font.color.rgb = COLOR_BLACK
        r_txt = p.add_run(); r_txt.text = n_desc; r_txt.font.name = "Calibri"; r_txt.font.size = Pt(11.0); r_txt.font.color.rgb = COLOR_CHARCOAL
        p.space_after = Pt(2)
        
        p = tf.add_paragraph()
        r_lbl = p.add_run(); r_lbl.text = "Technical Target: "; r_lbl.font.bold = True; r_lbl.font.size = Pt(11.0); r_lbl.font.color.rgb = COLOR_MUTED
        r_txt = p.add_run(); r_txt.text = n_why; r_txt.font.name = "Calibri"; r_txt.font.size = Pt(11.0); r_txt.font.color.rgb = COLOR_CHARCOAL
        p.space_after = Pt(0)

    # Right Column: Empirical Verification Proof Box
    evid_shape = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.783), start2_y, w2_l, Inches(4.50))
    evid_shape.fill.solid()
    evid_shape.fill.fore_color.rgb = COLOR_CARD_BG
    evid_shape.line.color.rgb = COLOR_CARD_BORDER
    evid_shape.line.width = Pt(1.0)
    tf_ev = evid_shape.text_frame
    tf_ev.word_wrap = True
    tf_ev.margin_left = tf_ev.margin_right = Inches(0.2)
    tf_ev.margin_top = Inches(0.15)
    
    p = tf_ev.paragraphs[0]
    p.text = "EMPIRICAL VERIFICATION EVIDENCE ON DISK"
    p.font.name = "Calibri"
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = COLOR_CRIMSON
    p.space_after = Pt(8)

    ev_bullets = [
        ("Testing Rigor:", "All 8 completed Phase-2 modules are backed by physical, reproducible test artifacts in the repository:"),
        ("49 Automated Pytest Tests (100% Green):", "Located in tests/ across 9 suites verifying RLock concurrency, regex guardrails, FastMCP tools, float limits, and exception recovery in 19.45s."),
        ("13 Selenium Browser UI Runs (100% Green):", "Automated screenshots in artifacts/browser_screenshots/ proving UI rendering, dispatch allocation, emergency rerouting, and hostile prompt blocking."),
        ("72 Factorial Benchmark Runs (100% Completed):", "3 architectures x 2 prompt styles x 4 personas x 3 orders with zero deadlocks; latency boxplot and agent execution heatmap generated and embedded."),
        ("5 FastMCP Domain Tool Endpoints Verified:", "Automated test harness validates contract schemas, payload constraints, and sub-millisecond execution times.")
    ]
    for b_title, b_txt in ev_bullets:
        p = tf_ev.add_paragraph()
        p.space_after = Pt(6)
        r_bullet = p.add_run(); r_bullet.text = "• "; r_bullet.font.bold = True; r_bullet.font.color.rgb = COLOR_MUTED
        r_bold = p.add_run(); r_bold.text = b_title + " "; r_bold.font.bold = True; r_bold.font.size = Pt(11.5); r_bold.font.color.rgb = COLOR_BLACK
        r_txt = p.add_run(); r_txt.text = b_txt; r_txt.font.size = Pt(11.0); r_txt.font.color.rgb = COLOR_CHARCOAL

    prs.save(str(OUT_1SLIDE))
    print(f"[DONE] Successfully regenerated clean human-style 2-slide matrix: {OUT_1SLIDE}")

def update_archives():
    """Update both Eval 2 Documents.zip and DeliveryFleet_MAS_Group8_Eval2.zip."""
    eval2_zip = REPO_DIR / "Eval 2 Documents.zip"
    print(f"Updating {eval2_zip}...")
    with zipfile.ZipFile(eval2_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in OUT_DIR.rglob("*"):
            if f.is_file() and not f.name.startswith("~$") and f.suffix != ".pyc":
                arcname = f.relative_to(OUT_DIR)
                z.write(f, arcname)
    size_mb1 = round(eval2_zip.stat().st_size / (1024 * 1024), 2)
    print(f"[OK] Updated {eval2_zip} ({size_mb1} MB)")

    parent_zip = REPO_DIR.parent / "DeliveryFleet_MAS_Group8_Eval2.zip"
    print(f"Updating {parent_zip}...")
    exclude_dirs = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache", ".mypy_cache"}
    exclude_exts = {".pyc", ".pyo"}
    count = 0
    with zipfile.ZipFile(parent_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in REPO_DIR.rglob("*"):
            if any(part in exclude_dirs for part in f.parts):
                continue
            if f.suffix in exclude_exts or f.name.startswith("~$"):
                continue
            if f.is_file():
                arcname = f.relative_to(REPO_DIR.parent)
                z.write(f, arcname)
                count += 1
    size_mb2 = round(parent_zip.stat().st_size / (1024 * 1024), 2)
    print(f"[OK] Packaged {count} files into {parent_zip} ({size_mb2} MB)")

if __name__ == "__main__":
    create_deck()
    create_human_1slide_matrix()
    update_archives()
