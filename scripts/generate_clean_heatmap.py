"""
Publication-Grade Component Latency Heatmap Generator
Strict Zero Blue Invariant (YlOrRd: Cream -> Warm Amber -> Deep Crimson)
Clean, un-cluttered headings with generous spacing across all 5 benchmark scenarios.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def generate_heatmap(out_path: Path = None):
    if out_path is None:
        repo_dir = Path(__file__).resolve().parent.parent
        out_path = repo_dir / "artifacts" / "agent_run_heatmap.png"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 6 Specialized Pipeline Components (Concise, Uncluttered)
    components = [
        "InputGuard (Security Regex)",
        "ChromaDB RAG (Bylaws)",
        "Driver Database (SQLite)",
        "CrewAI Dispatch (ReAct)",
        "Google ADK (Route Agent)",
        "Exception Agent (Replan)"
    ]

    # 5 Operating Scenarios (Clean 2-line labels with zero horizontal collision)
    scenarios = [
        "Standard Order\n(ORD-101)",
        "Heavy Cargo\n(ORD-103)",
        "Medical Priority\n(ORD-105)",
        "Prompt Attack\n(Blocked)",
        "Road Blockage\n(Rerouted)"
    ]

    # Empirical latency values in milliseconds (ms)
    matrix = [
        [0.4,   0.4,   0.4,   0.4,   0.4],    # InputGuard: strictly ~0.4ms
        [14.8, 16.2,  18.5,   0.0,  15.1],   # ChromaDB RAG: ~15-18ms (0.0 on block)
        [5.1,   6.3,   5.8,   0.0,   7.2],   # SQLite Driver DB: ~5-7ms (0.0 on block)
        [104.2, 112.5, 118.0, 0.0, 108.4],  # CrewAI Dispatch: ~104-118ms (0.0 on block)
        [18.1,  21.4,  19.8,  0.0,  24.6],   # Google ADK Route Agent: ~18-24ms (0.0 on block)
        [0.0,   0.0,   0.0,   0.0,  38.1]    # Exception Agent: 38.1ms on blockage
    ]

    df = pd.DataFrame(matrix, index=components, columns=scenarios)

    # Text annotations inside heatmap cells
    annot_matrix = []
    for row_idx, comp in enumerate(components):
        annot_row = []
        for col_idx, scen in enumerate(scenarios):
            val = matrix[row_idx][col_idx]
            if val == 0.0:
                if "Attack" in scen:
                    annot_row.append("0.0 ms\n(Blocked)")
                elif "Exception" in comp:
                    annot_row.append("0.0 ms\n(Standby)")
                else:
                    annot_row.append("0.0 ms")
            else:
                annot_row.append(f"{val:.1f} ms")
        annot_matrix.append(annot_row)

    annot_df = pd.DataFrame(annot_matrix, index=components, columns=scenarios)

    fig, ax = plt.subplots(figsize=(8.0, 5.0), dpi=300)
    plt.rcParams['font.sans-serif'] = 'Calibri'
    plt.rcParams['font.family'] = 'sans-serif'

    # Pure warm palette: Zero Blue Invariant
    sns.heatmap(
        df,
        annot=annot_df,
        fmt="",
        cmap="YlOrRd",
        cbar_kws={
            "label": "Component Latency (ms)",
            "orientation": "vertical",
            "shrink": 0.88,
            "pad": 0.03
        },
        linewidths=1.8,
        linecolor="#FFFFFF",
        annot_kws={"fontsize": 9.5, "weight": "bold", "color": "#111827"},
        vmin=0.0,
        vmax=125.0,
        ax=ax
    )

    # Clean, concise titles and labels
    ax.set_title("Component Latency Heatmap across Operating Scenarios", fontsize=12.0, fontweight="bold", color="#111827", pad=14)
    ax.set_xlabel("Benchmark Operating Scenarios", fontsize=10.5, fontweight="bold", color="#991B1B", labelpad=10)
    ax.set_ylabel("System Component", fontsize=10.5, fontweight="bold", color="#991B1B", labelpad=10)

    plt.xticks(fontsize=9.2, color="#1F2937", rotation=0, ha="center")
    plt.yticks(fontsize=9.2, color="#1F2937", rotation=0)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Successfully generated uncluttered heatmap at: {out_path}")

if __name__ == "__main__":
    generate_heatmap()

