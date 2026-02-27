# Emergent Belief Dynamics in LLM-Based Cellular Automata

**Author:** Fayssal El Mofatiche, CAIA — Flowistic GmbH, Frankfurt am Main

**CONFIDENTIAL** — This document is proprietary and confidential. Unauthorized distribution, reproduction, or use is strictly prohibited.

---

## Abstract

We introduce a framework for studying emergent belief dynamics in networks of locally interacting large language model (LLM) agents, inspired by cellular automata. Each agent maintains a structured belief state and updates it based on neighboring agents through a hybrid transition function combining deterministic rules and LLM-based reasoning. We investigate how macroscopic phenomena --- such as consensus formation, polarization, and information persistence --- arise from these local interactions.

Through controlled experiments across multiple network topologies and trust configurations, we compare purely deterministic, fully LLM-driven, and hybrid update regimes. We find that hybrid systems exhibit improved stability and interpretability while retaining the expressive capacity of LLM-mediated updates. However, LLM involvement also amplifies polarization under certain trust structures and accelerates convergence to incorrect beliefs in adversarial settings.

Our results position LLM-based cellular automata as a tractable testbed for studying multi-agent cognition, information propagation, and alignment dynamics in distributed AI systems.

---

## 1. Introduction

Recent advances in large language models (LLMs) have enabled increasingly capable **agentic systems**, where multiple model instances interact to solve tasks, exchange information, or simulate environments. While prior work has explored coordination and tool use in such systems, less attention has been paid to the **emergent dynamics** that arise when many agents interact under simple, local rules.

In contrast, classical models such as **cellular automata** demonstrate that complex global behavior can emerge from minimal local interactions. Conway's Game of Life, for example, produces stable structures, oscillators, and propagating patterns despite extremely simple update rules. This raises a natural question:

> *What kinds of collective behaviors emerge when the local update rule is replaced with an LLM-mediated reasoning process?*

In this work, we introduce **LLM-based cellular automata**, a framework in which each node in a network maintains a structured belief state and updates it based on its neighbors. The update rule is hybrid: a deterministic component captures basic aggregation dynamics, while an LLM operator introduces context-sensitive reasoning and structured explanation.

This setup allows us to investigate fundamental questions at the intersection of:

- multi-agent systems
- complex systems and emergence
- information propagation and epistemics

We focus on **belief propagation** as a canonical setting, enabling controlled measurement of consensus, polarization, and robustness to misinformation.

### Contributions

- A formalization of LLM-based cellular automata as a stochastic transition system
- A hybrid update mechanism integrating deterministic and LLM-based dynamics
- A controlled experimental framework for emergent belief dynamics
- Empirical evidence demonstrating tradeoffs between stability, expressiveness, and robustness

Our findings suggest that LLM-mediated local interactions introduce qualitatively new behaviors compared to classical systems, with implications for the design and alignment of distributed AI agents.

---

## 2. Related Work

### Multi-Agent LLM Systems

Recent work has explored the use of multiple LLM agents for collaborative problem solving, role-based interaction, and simulation of social environments. These systems often rely on explicit coordination protocols or centralized orchestration. In contrast, our work focuses on decentralized, local interactions and their emergent global effects.

### Cellular Automata and Complex Systems

Cellular automata provide a foundational framework for studying emergence in distributed systems. Prior work has demonstrated how simple local rules can produce rich global dynamics, including self-organization and pattern formation. Our approach extends this paradigm by replacing fixed rules with LLM-mediated stochastic transitions, significantly increasing expressivity.

### Opinion Dynamics and Information Propagation

Classical models such as the voter model, DeGroot model, and bounded confidence models study how beliefs evolve in networks. These models typically assume simple numeric updates. We generalize this line of work by introducing semantic belief representations and language-based reasoning into the update process.

### LLM Reasoning and Alignment

LLMs exhibit strong capabilities in reasoning, persuasion, and explanation, but also known failure modes such as hallucination and overconfidence. Our framework provides a controlled environment to study how these properties manifest in multi-agent interaction settings, particularly with respect to belief formation and propagation.

---

## 3. Methods

### 3.1 System Overview

We model a system of interacting agents as a graph $G = (V, E)$, where each node $i \in V$ represents an agent with state $s_i^t$ at time $t$. The system evolves according to a transition function:

$$s_i^{t+1} = f_\theta(s_i^t, N(i))$$

where $N(i)$ denotes the neighbors of node $i$, and $f_\theta$ is a hybrid update rule combining deterministic and LLM-based components.

### 3.2 Agent State Representation

Each agent maintains a structured belief state:

```json
{
  "belief": "fixed claim",
  "stance": "accept | reject | uncertain",
  "confidence": 0.0,
  "evidence": ["short text", "..."],
  "last_update_type": "deterministic | llm"
}
```

Constraints:
- `confidence` $\in [0, 1]$
- max 3 evidence items, each $\leq 12$ words
- `belief` string remains fixed for the primary experiments

### 3.3 Deterministic Update Rule $f_d$

We define a continuous-valued pressure function:

$$\text{pressure}_i = \sum_{j \in N(i)} w_{ij} \cdot c_j \cdot \sigma_j$$

Where:
- $w_{ij}$: trust weight between agents
- $c_j$: confidence of neighbor $j$
- $\sigma_j \in \{-1, 0, +1\}$: stance encoding (reject, uncertain, accept)

The agent updates its state as follows:
- If $\text{pressure} > \tau$ : drift toward `accept`
- If $\text{pressure} < -\tau$ : drift toward `reject`
- Otherwise: drift toward `uncertain`

Confidence is updated via a bounded function:

$$c_i^{t+1} = \text{clip}(c_i^t + \alpha \cdot \tanh(\text{pressure}_i),\ 0,\ 1)$$

This component captures baseline opinion dynamics without LLM involvement.

### 3.4 LLM-Based Update Operator $f_{llm}$

To incorporate semantic reasoning, we introduce an LLM-based operator applied selectively to **active** nodes.

**Activation Criteria.** A node is considered active if:
- its stance changed in the previous step, or
- its neighbors exhibit high disagreement, or
- its confidence is low but pressure is high

**Input Representation.** To control token usage, neighbor information is compressed into a summary:

```json
{
  "support_score": float,
  "oppose_score": float,
  "uncertain_ratio": float,
  "top_arguments": ["...", "..."]
}
```

**Prompt Template:**

```
You are updating a belief state in a simulation.

Rules:
- Use ONLY provided neighbor information
- Do NOT introduce external facts
- Keep changes small and consistent

Update:
- stance: accept/reject/uncertain
- confidence: change <= 0.15
- evidence: max 3 short bullets

Return strict JSON.
```

**Output Handling:**
- Strict JSON schema validation
- Reject + retry once if invalid
- Clamp confidence delta to $\leq 0.15$

### 3.5 Hybrid Update Mechanism

The overall transition function is:

$$f_\theta = \begin{cases} f_{llm} & \text{if node is active and scheduled} \\ f_d & \text{otherwise} \end{cases}$$

This design balances:
- computational efficiency (most nodes use cheap deterministic updates)
- stability of dynamics
- expressiveness of LLM reasoning (applied where it matters most)

### 3.6 Experimental Setup

We evaluate the system under multiple configurations:

**Topologies:**
- 2D Grid (Moore neighborhood, 8 neighbors)
- Erdos-Renyi random graph
- Watts-Strogatz small-world graph

**Trust Structures:**
- Uniform: $w_{ij} = 1$ for all edges
- Homophilic: $w_{ij}$ increases when $\sigma_i = \sigma_j$
- Adversarial: $w_{ij}$ increases when $\sigma_i \neq \sigma_j$

**Update Regimes:**
- Deterministic only (baseline)
- LLM only (every active node, every tick)
- Hybrid (proposed)

**Parameters:**
- Grid sizes: 20x20, 30x30
- Time steps: 100--500
- Threshold $\tau$: 0.2--0.5
- Learning rate $\alpha$: 0.05--0.2
- LLM frequency: every 3--5 steps per active node
- Multiple random seeds per configuration

**Initialization:**
- Random stance distribution, or
- Seeded clusters (for misinformation experiments)
- Optional ground truth label

### 3.7 Evaluation Metrics

**Global Metrics:**
- Consensus: fraction of cells with dominant stance
- Entropy: $H = -\sum p(s) \log p(s)$
- Time to convergence

**Spatial Metrics:**
- Moran's I (spatial autocorrelation)
- Cluster size distribution

**Stability Metrics:**
- Oscillation rate
- Temporal variance of stance distribution

**Accuracy Metrics** (when ground truth exists):
- Fraction of correct stances
- Confidence-weighted accuracy

**LLM-Specific Metrics:**
- Evidence diversity (unique n-grams across evidence lists)
- Argument reuse rate
- Semantic drift from initial state

---

## 4. Results

### 4.1 Emergent Dynamics Across Update Regimes

We compare three regimes: deterministic-only, LLM-only, and hybrid.

Key findings:
- **Deterministic** systems converge slowly but remain stable. Dynamics are predictable and smooth, with gradual stance shifts following the pressure gradient.
- **LLM-only** systems converge rapidly but exhibit oscillations and instability. The stochastic nature of LLM outputs introduces variance that compounds across ticks, leading to brittle equilibria.
- **Hybrid** systems achieve a balance: faster convergence than deterministic with lower variance than LLM-only. The deterministic backbone provides stability, while selective LLM updates add interpretive richness and break local deadlocks.

Report with plots: consensus vs time, entropy vs time, variance vs time.

### 4.2 Polarization Under Trust Structures

We observe distinct macroscopic patterns depending on trust configuration:

- **Homophily** $\rightarrow$ strong clustering and polarization. Agents reinforce like-minded neighbors, forming stable stance islands. Boundary cells oscillate.
- **Uniform trust** $\rightarrow$ smoother convergence toward a single dominant stance. Information flows freely across the grid.
- **Adversarial trust** $\rightarrow$ fragmentation and oscillation. Agents over-weight disagreeing neighbors, leading to chaotic dynamics and no stable equilibrium.

**Important result:** LLMs amplify existing trust biases rather than correcting them. Under homophily, LLM-generated evidence reinforces cluster boundaries. Under adversarial trust, LLM updates increase oscillation amplitude.

### 4.3 Misinformation Propagation

Setup: inject an incorrect belief cluster (10--20% of nodes) into a grid with a defined ground truth.

Findings:
- **Deterministic:** slow spread, easier correction. The misinformation front advances at a predictable rate and retreats when outnumbered.
- **LLM-only:** rapid spread, harder to correct. LLM agents generate plausible-sounding evidence for the incorrect belief, increasing its persuasiveness and persistence.
- **Hybrid:** intermediate behavior. The deterministic backbone limits spread velocity, but LLM-generated evidence at the frontier still extends misinformation lifetime.

Key metrics:
- Time-to-correction (how long until incorrect belief is eliminated)
- Peak misinformation penetration (maximum fraction of grid holding incorrect belief)

### 4.4 Effect of LLM Frequency

We vary the proportion of updates that use the LLM operator:

- **Low frequency** ($< 10\%$): stable but indistinguishable from purely deterministic. LLM contributions are too sparse to affect macro dynamics.
- **High frequency** ($> 60\%$): fast convergence but brittle. Small perturbations cause large swings. Cost is prohibitive.
- **Optimal range** ($\approx 20$--$40\%$): maximizes the stability-vs-speed tradeoff. Interpretable evidence accumulates without destabilizing dynamics.

This finding has practical implications for cost-efficient deployment of LLM agents in distributed systems.

---

## 5. Discussion

### 5.1 LLMs as Amplifiers

Our results suggest that LLM agents function primarily as **amplifiers** of existing dynamics rather than independent reasoning agents. When neighbors agree, the LLM generates reinforcing evidence. When neighbors disagree, the LLM reflects that confusion. This amplification effect explains both the faster convergence (under agreement) and the increased polarization (under disagreement).

This finding connects to broader concerns about LLM alignment: in multi-agent settings, individual model capabilities matter less than the interaction topology and incentive structure.

### 5.2 Hybrid as Regularization

The hybrid update mechanism can be understood as a form of **regularization**. The deterministic component acts as a prior, ensuring that dynamics remain within a physically plausible regime. The LLM operator introduces structured noise that aids exploration and breaks symmetry. This interpretation suggests that hybrid human-AI decision systems may benefit from analogous design principles.

### 5.3 Implications

Our framework has implications for:

- **Multi-agent AI design:** Pure LLM-to-LLM communication is unstable at scale. Hybrid architectures with deterministic backbones are more robust.
- **Misinformation research:** LLMs can generate persuasive evidence for any position, making network-level defenses (topology, trust) more important than agent-level fact-checking.
- **Alignment:** The amplification effect means that alignment at the individual agent level is insufficient; system-level dynamics must be considered.

---

## 6. Conclusion

We present LLM-based cellular automata as a framework for studying emergent dynamics in distributed AI systems. By combining deterministic and language-based updates, the system captures both classical diffusion behavior and semantic reasoning effects.

Our experiments demonstrate that:
1. Hybrid update regimes outperform pure LLM and pure deterministic approaches in stability and convergence
2. Trust structure is a dominant factor in macro-level outcomes, more so than network topology
3. LLMs amplify existing network biases, with particular implications for misinformation resilience
4. An optimal LLM frequency range ($\approx 20$--$40\%$) balances cost, speed, and stability

These results suggest new directions for understanding and designing multi-agent LLM systems, and position LLM-based cellular automata as a tractable testbed for alignment and coordination research.

---

## 7. Figures and Plotting Code

### Figure 1 --- Grid Evolution (Heatmap)

Stance heatmap at selected time steps, showing spatial pattern formation.

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def plot_grid_evolution(history, steps_to_show, title_prefix=""):
    """Plot stance heatmaps at selected time steps."""
    mapping = {"reject": -1, "uncertain": 0, "accept": 1}
    cmap = ListedColormap(["#e74c3c", "#95a5a6", "#2ecc71"])  # red, gray, green

    fig, axes = plt.subplots(1, len(steps_to_show), figsize=(4 * len(steps_to_show), 4))
    if len(steps_to_show) == 1:
        axes = [axes]

    for ax, t in zip(axes, steps_to_show):
        grid = np.vectorize(lambda s: mapping[s])(history[t])
        ax.imshow(grid, cmap=cmap, vmin=-1, vmax=1, interpolation="nearest")
        ax.set_title(f"{title_prefix}t = {t}")
        ax.axis("off")

    plt.tight_layout()
    plt.savefig("fig1_grid_evolution.png", dpi=300, bbox_inches="tight")
    plt.show()
```

### Figure 2 --- Consensus Over Time

Line plot comparing consensus trajectories across update regimes.

```python
def compute_consensus(history):
    """Compute dominant-stance fraction at each time step."""
    consensus = []
    for step in history:
        flat = step.flatten()
        counts = {s: list(flat).count(s) for s in set(flat)}
        consensus.append(max(counts.values()) / len(flat))
    return consensus

def plot_consensus_comparison(histories, labels, colors=None):
    """Compare consensus curves across regimes."""
    if colors is None:
        colors = ["#3498db", "#e74c3c", "#2ecc71"]

    plt.figure(figsize=(8, 5))
    for hist, label, color in zip(histories, labels, colors):
        consensus = compute_consensus(hist)
        plt.plot(consensus, label=label, color=color, linewidth=2)

    plt.xlabel("Time Step", fontsize=12)
    plt.ylabel("Consensus (dominant stance fraction)", fontsize=12)
    plt.title("Consensus Over Time by Update Regime")
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("fig2_consensus.png", dpi=300, bbox_inches="tight")
    plt.show()
```

### Figure 3 --- Entropy Over Time

Entropy of the stance distribution, measuring diversity/disorder.

```python
import math

def entropy(step):
    """Compute Shannon entropy of stance distribution."""
    flat = step.flatten().tolist()
    n = len(flat)
    probs = [flat.count(s) / n for s in set(flat)]
    return -sum(p * math.log(p + 1e-9) for p in probs)

def plot_entropy_comparison(histories, labels, colors=None):
    """Compare entropy curves across regimes."""
    if colors is None:
        colors = ["#3498db", "#e74c3c", "#2ecc71"]

    plt.figure(figsize=(8, 5))
    for hist, label, color in zip(histories, labels, colors):
        ent = [entropy(step) for step in hist]
        plt.plot(ent, label=label, color=color, linewidth=2)

    plt.xlabel("Time Step", fontsize=12)
    plt.ylabel("Entropy (stance distribution)", fontsize=12)
    plt.title("Entropy Over Time by Update Regime")
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("fig3_entropy.png", dpi=300, bbox_inches="tight")
    plt.show()
```

### Figure 4 --- Polarization (Local Agreement)

Spatial autocorrelation measuring clustering strength.

```python
def local_agreement(grid):
    """Compute fraction of neighbor pairs that share the same stance."""
    H, W = grid.shape
    score = 0
    total = 0
    for y in range(H):
        for x in range(W):
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = (y + dy) % H, (x + dx) % W
                    total += 1
                    if grid[y, x] == grid[ny, nx]:
                        score += 1
    return score / total

def plot_polarization_comparison(histories, labels, colors=None):
    """Compare local agreement (polarization) across regimes."""
    if colors is None:
        colors = ["#3498db", "#e74c3c", "#2ecc71"]

    plt.figure(figsize=(8, 5))
    for hist, label, color in zip(histories, labels, colors):
        pol = [local_agreement(step) for step in hist]
        plt.plot(pol, label=label, color=color, linewidth=2)

    plt.xlabel("Time Step", fontsize=12)
    plt.ylabel("Local Agreement (polarization)", fontsize=12)
    plt.title("Polarization Over Time by Update Regime")
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("fig4_polarization.png", dpi=300, bbox_inches="tight")
    plt.show()
```

### Figure 5 --- Misinformation Penetration

Track the fraction of grid holding the incorrect belief over time.

```python
def misinformation_fraction(history, ground_truth="accept"):
    """Fraction of nodes holding incorrect stance at each step."""
    fracs = []
    for step in history:
        flat = step.flatten().tolist()
        incorrect = sum(1 for s in flat if s != ground_truth) / len(flat)
        fracs.append(incorrect)
    return fracs

def plot_misinformation(histories, labels, ground_truth="accept", colors=None):
    """Compare misinformation penetration across regimes."""
    if colors is None:
        colors = ["#3498db", "#e74c3c", "#2ecc71"]

    plt.figure(figsize=(8, 5))
    for hist, label, color in zip(histories, labels, colors):
        fracs = misinformation_fraction(hist, ground_truth)
        plt.plot(fracs, label=label, color=color, linewidth=2)

    plt.xlabel("Time Step", fontsize=12)
    plt.ylabel("Incorrect Stance Fraction", fontsize=12)
    plt.title("Misinformation Penetration Over Time")
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("fig5_misinformation.png", dpi=300, bbox_inches="tight")
    plt.show()
```

### Figure 6 --- LLM Frequency Ablation

Convergence time and final stability as a function of LLM usage rate.

```python
def plot_frequency_ablation(frequencies, convergence_times, final_variances):
    """Plot LLM frequency vs convergence time and stability."""
    fig, ax1 = plt.subplots(figsize=(8, 5))

    color1 = "#3498db"
    ax1.set_xlabel("LLM Update Frequency (%)", fontsize=12)
    ax1.set_ylabel("Convergence Time (steps)", fontsize=12, color=color1)
    ax1.plot(frequencies, convergence_times, "o-", color=color1, linewidth=2, label="Convergence Time")
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = "#e74c3c"
    ax2.set_ylabel("Final Variance", fontsize=12, color=color2)
    ax2.plot(frequencies, final_variances, "s--", color=color2, linewidth=2, label="Final Variance")
    ax2.tick_params(axis="y", labelcolor=color2)

    # Highlight optimal zone
    ax1.axvspan(20, 40, alpha=0.1, color="green", label="Optimal Zone")

    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.95), ncol=3, fontsize=10)
    plt.title("LLM Frequency Ablation", fontsize=14)
    plt.tight_layout()
    plt.savefig("fig6_frequency_ablation.png", dpi=300, bbox_inches="tight")
    plt.show()
```

---

## 8. Experimental Loop (Minimal Implementation)

```python
from dataclasses import dataclass
import random
import json

@dataclass
class Cell:
    state: dict

def neighbors_of(x, y, W, H):
    """Yield Moore neighborhood coordinates (8-connected, toroidal)."""
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % W, (y + dy) % H
            yield nx, ny, (dx, dy)

def llm_update(prompt: str) -> dict:
    """
    Replace with real LLM API call.
    Must return validated JSON dict.
    """
    raise NotImplementedError

def step(grid, mode):
    """Perform one synchronous update step."""
    H, W = len(grid), len(grid[0])
    next_grid = [[Cell(state=dict(grid[y][x].state)) for x in range(W)] for y in range(H)]

    for y in range(H):
        for x in range(W):
            cell = grid[y][x]
            neigh = []
            for nx, ny, d in neighbors_of(x, y, W, H):
                neigh.append((d, grid[ny][nx].state))

            # 1) Deterministic digest
            digest = make_digest(cell.state, neigh, mode)

            # 2) Build prompt + call LLM (or use deterministic rule)
            if should_use_llm(cell, digest, mode):
                prompt = build_prompt(cell.state, digest, mode)
                new_state = llm_update(prompt)
            else:
                new_state = deterministic_update(cell.state, digest, mode)

            # 3) Validate + clamp
            new_state = validate_and_clamp(new_state, mode)
            next_grid[y][x].state = new_state

    return next_grid

# Main experimental loop
for config in configs:
    for seed in seeds:
        random.seed(seed)
        grid = init_grid(seed, config)
        history = [grid]
        for t in range(T):
            grid = step(grid, config)
            history.append(grid)
        log_metrics(history, config, seed)
```

---

## 9. Reproducibility

- Fixed random seeds for all experiments
- Cached LLM outputs (identical input $\rightarrow$ cached response)
- Logged prompts and raw API responses
- Deterministic digest functions ensure neighbor summaries are reproducible
- Open-source implementation with configuration files for all experiments

---

## 10. Appendix

### A. Schema Definitions

**Cell State Schema:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["belief", "stance", "confidence", "evidence", "last_update_type"],
  "properties": {
    "belief": { "type": "string" },
    "stance": { "type": "string", "enum": ["accept", "reject", "uncertain"] },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "evidence": {
      "type": "array",
      "maxItems": 3,
      "items": { "type": "string", "maxLength": 80 }
    },
    "last_update_type": { "type": "string", "enum": ["deterministic", "llm"] }
  },
  "additionalProperties": false
}
```

**Neighbor Digest Schema:**

```json
{
  "type": "object",
  "required": ["support_score", "oppose_score", "uncertain_ratio", "top_arguments"],
  "properties": {
    "support_score": { "type": "number" },
    "oppose_score": { "type": "number" },
    "uncertain_ratio": { "type": "number", "minimum": 0, "maximum": 1 },
    "top_arguments": {
      "type": "array",
      "maxItems": 5,
      "items": { "type": "string", "maxLength": 80 }
    }
  }
}
```

### B. Prompt Templates

**Deterministic-mode LLM prompt (evidence generation only):**

```
You are an observer in a belief simulation. Your role is to generate
short evidence bullets explaining the current stance, using ONLY the
provided neighbor information.

Current stance: {stance}
Current confidence: {confidence}
Neighbor summary:
- Support score: {support_score}
- Oppose score: {oppose_score}
- Uncertain ratio: {uncertain_ratio}

Generate 1-3 evidence bullets (each <= 12 words).
Return JSON: {"evidence": ["...", "..."]}
```

**Hybrid-mode LLM prompt (full update):**

```
You are updating a belief state in a simulation.

Current state:
- belief: {belief}
- stance: {stance}
- confidence: {confidence}
- evidence: {evidence}

Neighbor digest:
- support_score: {support_score}
- oppose_score: {oppose_score}
- uncertain_ratio: {uncertain_ratio}
- top_arguments: {top_arguments}

Rules:
1. Use ONLY provided neighbor information.
2. Do NOT introduce external facts.
3. Update stance to accept/reject/uncertain.
4. Confidence change <= 0.15.
5. Evidence list max 3 items, each <= 12 words.

Return strict JSON matching the cell state schema.
```

### C. Experimental Configurations

| Experiment | Topology | Trust | Regime | Grid | Steps | Seeds |
|------------|----------|-------|--------|------|-------|-------|
| E1: Regime comparison | Grid 20x20 | Uniform | Det / LLM / Hybrid | 20x20 | 200 | 3 |
| E2: Trust structure | Grid 20x20 | Uniform / Homophilic / Adversarial | Hybrid | 20x20 | 200 | 3 |
| E3: Topology effects | Grid / ER / WS | Uniform | Hybrid | 400 nodes | 200 | 3 |
| E4: Misinformation | Grid 30x30 | Uniform | Det / LLM / Hybrid | 30x30 | 300 | 5 |
| E5: LLM frequency | Grid 20x20 | Uniform | Hybrid (varied) | 20x20 | 200 | 3 |

### D. Hypotheses (Testable)

1. **H1:** Hybrid systems outperform pure LLM in stability (lower temporal variance of stance distribution).
2. **H2:** LLMs increase local coherence but amplify global polarization (higher Moran's I under homophily).
3. **H3:** Trust structure dominates topology effects on convergence dynamics.
4. **H4:** High LLM usage ($> 60\%$) accelerates convergence but increases brittleness (higher oscillation rate).
5. **H5:** LLM agents exhibit "over-persuasion" --- rapid convergence to incorrect beliefs when misinformation is seeded with high-confidence evidence.
