# Eval-Driven Development

Our focus as technologists must shift from what we can build to what we can prove.

Software development is now agent-driven. AI writes the code. The engineer's job is no longer to produce working software — it is to define what "working" means, measure it, and hold the system to that definition.

We propose **Eval-Driven Development**: a discipline where every probabilistic system starts with a specification of correctness, and nothing ships without automated proof that it meets that spec.

## Principles

### 1. Evaluation is the product

The eval suite is not a phase that follows development. Build evals first. Code is generated. Evals are engineered.

### 2. Define correctness before you write a prompt

If you cannot express "correct" as a deterministic function, you are not ready to build. Every task needs an eval. Every eval needs a threshold. Every threshold needs a justification.

### 3. Probabilistic systems require statistical proof

A single passing test proves nothing about a stochastic system. You need sample sizes, confidence intervals, and regression baselines. Measure distributions, not anecdotes.

### 4. Evals must run in CI

If your evals do not run on every change, they do not exist. Evaluation belongs in the pipeline next to lint, type-check, and build — not in a notebook someone runs quarterly.

### 5. Evaluation drives architecture

The eval suite determines the system boundary. If a component cannot be independently evaluated, it cannot be independently trusted. Design for measurability like you design for testability.

### 6. Cost is a metric

Token spend, latency, and compute are evaluation dimensions. A system that is correct but unaffordable has failed its eval.

### 7. Human judgment does not scale — codify it

Every manual review is a missing eval. When a human judges output quality, extract that judgment into a rubric, automate the rubric, then evaluate the evaluator.

### 8. Ship the eval, not the demo

A demo proves something can work once. An eval proves it works reliably under distribution shift. Demos convince stakeholders. Evals convince engineers.

### 9. Version your evals like you version your code

Eval definitions, datasets, thresholds, and results live in version control. They have changelogs. When the eval changes, the reason is documented.

### 10. The eval gap is the opportunity

Most teams ship AI without rigorous evaluation. The gap between "it works on my machine" and "it passes eval at p < 0.05" is where defensible products get built.
