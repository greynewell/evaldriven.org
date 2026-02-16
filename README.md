# Eval-Driven Development

What we can build matters less than what we can prove.

AI writes code. The engineer defines "working," measures it, enforces it. **Eval-Driven Development**: every probabilistic system starts with a correctness spec. Nothing ships without automated proof it passes.

## Principles

### 1. Evaluation is the product

Build evals first. Code is generated. Evals are engineered.

### 2. Define correctness before you write a prompt

Can't express "correct" as a deterministic function? Not ready to build. Every task needs an eval. Every eval needs a threshold. Every threshold needs a justification.

### 3. Probabilistic systems require statistical proof

One passing test proves nothing about a stochastic system. Sample sizes, confidence intervals, regression baselines. Distributions, not anecdotes.

### 4. Evals run in CI

Evals that don't run on every change don't exist. Next to lint, type-check, build.

### 5. Evaluation drives architecture

Can't independently evaluate a component? Can't independently trust it. Design for measurability.

### 6. Cost is a metric

Token spend, latency, compute. Correct but unaffordable is a failed eval.

### 7. Human judgment doesn't scale

Every manual review is a missing eval. Extract judgment into a rubric, automate it, evaluate the evaluator.

### 8. Ship the eval, not the demo

Demos prove something works once. Evals prove it works under distribution shift.

### 9. Version your evals

Definitions, datasets, thresholds, results. Version control. Changelogs. Document why.

### 10. The eval gap is the opportunity

"Works on my machine" vs. "passes at p < 0.05." That gap is where defensible products get built.
