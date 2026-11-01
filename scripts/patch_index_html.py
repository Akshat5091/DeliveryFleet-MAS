from pathlib import Path

root = Path(__file__).resolve().parent.parent
p = root / "src" / "web" / "index.html"
text = p.read_text(encoding="utf-8")

# 1. Update captions in lines 1028-1029
text = text.replace("across the 48-run matrix", "across the 72-run matrix")
text = text.replace("across 48 benchmark runs", "across 72 benchmark runs")

# 2. Update Header Badge in Architecture tab
old_badge = '<span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-200 dark:border-emerald-500/30">100% Verified</span>'
new_badge = '<span class="text-xs font-bold text-sky-700 dark:text-sky-400 bg-sky-50 dark:bg-sky-500/10 px-2.5 py-1 rounded-full border border-sky-200 dark:border-sky-500/30">Phase 2: ~68% Milestone (7 Verified | 4 End-Term Novelties)</span>'
text = text.replace(old_badge, new_badge)

# 3. Update the 11 criteria block in Architecture tab
old_criteria_block = '''          <div class="space-y-3 text-xs">
            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C1: Diverse Personas &amp; Adaptive Prompting</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C2: RAG Pipeline with Document Chunking</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C3: FastMCP Tool Ecosystem (5 tools)</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C4: Multi-Tier Guardrails &amp; HMAC Security</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C5: Observability, Tracing &amp; Cost Metrics</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C6: Collaborative MAS Protocols (A2A Bridge)</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C7: Exception Handling &amp; Dynamic Recovery</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C8: Tri-Architecture Orchestrations (Hierarchical vs Parallel vs Sequential)</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C9: Comprehensive Academic Benchmarks</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C10: Individual Member Contributions &amp; Testing</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>C11: Edge Deployment &amp; Cloudflare Gateway</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">100%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>
          </div>'''

new_criteria_block = '''          <div class="space-y-3 text-xs">
            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>1. Blackboard Shared State (src/schemas/blackboard.py:35-55)</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">Covered (100% ✅)</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>2. FastMCP Tool Ecosystem (src/mcp/server.py:23-45 &amp; client.py)</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">Covered (100% ✅)</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>3. Pydantic v2 Structured Output (src/schemas/reports.py:20-45)</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">Covered (100% ✅)</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>4. Hierarchical vs Sequential MAS (src/orchestration/hierarchical_orchestrator.py:154-172)</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">Covered (100% ✅)</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>5. Callbacks &amp; 24h Telematics Heatmaps (src/observability/callbacks.py)</span>
                <span class="text-sky-600 dark:text-sky-400 font-bold">Phase 3 Novelty 🚀</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-sky-500 h-1.5 rounded-full" style="width: 40%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>6. Cross-Framework A2A Protocol Bridge (src/agents/a2a_bridge.py:74-114)</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">Covered (100% ✅)</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>7. Dual Framework Architecture (CrewAI + Google ADK)</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">Covered (100% ✅)</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>8. Multi-Tier Security Guardrails &amp; 9.0h Shift Cap (src/guardrails/input_guard.py:20-45)</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">Covered (100% ✅)</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>9. Enterprise OpenTelemetry Collector &amp; Jaeger Dashboard</span>
                <span class="text-sky-600 dark:text-sky-400 font-bold">Phase 3 Novelty 🚀</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-sky-500 h-1.5 rounded-full" style="width: 35%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>10. 72+ Run Factorial Suite &amp; Pareto Frontiers (src/evaluation/benchmark_runner.py)</span>
                <span class="text-sky-600 dark:text-sky-400 font-bold">Phase 3 Novelty 🚀</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-sky-500 h-1.5 rounded-full" style="width: 45%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-700 dark:text-slate-300 mb-1">
                <span>11. Cloud VM Deployment (AWS/GCP) &amp; Cloudflare Edge Worker Bridge</span>
                <span class="text-sky-600 dark:text-sky-400 font-bold">Phase 3 Novelty 🚀</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-[#151f33] h-1.5 rounded-full overflow-hidden">
                <div class="bg-sky-500 h-1.5 rounded-full" style="width: 30%"></div>
              </div>
            </div>
          </div>'''

text = text.replace(old_criteria_block, new_criteria_block)
p.write_text(text, encoding="utf-8")
print("[DONE] Successfully patched index.html with Hallmark criteria pacing!")
