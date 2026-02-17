---
layout: base.njk
title: Eval-Driven Development
permalink: /
articleSchema: >
  {"@context":"https://schema.org","@type":"Article","headline":"Eval-Driven Development","description":"A manifesto for evaluation-driven AI development. Why every AI system needs deterministic, automated evaluation as a first-class engineering practice.","author":{"@type":"Person","@id":"https://greynewell.com/#identity","name":"Grey Newell","url":"https://greynewell.com"},"publisher":{"@type":"Person","@id":"https://greynewell.com/#identity","name":"Grey Newell","url":"https://greynewell.com"},"url":"https://evaldriven.org","datePublished":"2026-02-15","mainEntityOfPage":{"@type":"WebPage","@id":"https://evaldriven.org"},"keywords":["eval-driven development","AI evaluation","LLM evaluation","model evaluation","evaluation engineering","CI/CD for LLMs","deterministic testing","AI quality assurance"]}
faqSchema: >
  {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How is eval-driven development different from test-driven development?","acceptedAnswer":{"@type":"Answer","text":"TDD uses binary pass/fail criteria that work for deterministic code. AI systems are probabilistic\u2014outputs vary across runs, models, and prompts. Eval-driven development requires defining success thresholds before writing tests: what score is good enough? What regression is acceptable? That threshold-setting step is the part that experienced test-driven developers do intuitively but rarely formalize. EDD makes it explicit and mandatory."}},{"@type":"Question","name":"Isn't this just MLOps?","acceptedAnswer":{"@type":"Answer","text":"MLOps treats evaluation as a deployment and monitoring concern. Eval-driven development makes it a development practice that precedes writing code, not something bolted on after. The eval comes first\u2014before the prompt, before the pipeline, before the model selection. MLOps asks \"is it still working?\" EDD asks \"how do we know it works at all?\""}},{"@type":"Question","name":"You can't evaluate subjective AI outputs.","acceptedAnswer":{"@type":"Answer","text":"You can. Define rubrics, use LLM-as-judge, measure consistency across runs. \"Subjective\" usually means \"we haven't defined our criteria yet\"\u2014which is exactly the problem eval-driven development solves. If you can't articulate what good looks like, you can't build toward it."}},{"@type":"Question","name":"Evals are too slow and expensive to run in CI.","acceptedAnswer":{"@type":"Answer","text":"Tier them. Fast, cheap smoke evals on every commit. Comprehensive suites nightly. Same pattern as unit tests versus integration tests. The cost of not running evals is shipping regressions to users\u2014that's more expensive."}},{"@type":"Question","name":"My use case is just one API call. I don't need this.","acceptedAnswer":{"@type":"Answer","text":"That call will regress when the model updates, the prompt drifts, or the context changes. The simpler the integration, the easier the eval\u2014no excuse not to have one."}},{"@type":"Question","name":"How is this different from A/B testing?","acceptedAnswer":{"@type":"Answer","text":"A/B testing experiments on users post-deploy. Evals catch problems pre-deploy, deterministically, without shipping broken experiences to real people. A/B testing tells you which version users prefer. Evals tell you whether either version is good enough to ship."}}]}
---
# Eval-Driven Development

Our focus as technologists must shift from what we can build to what we can prove.

Software development is now agent-driven. AI writes the code. The engineer's job is no longer to produce working software — it is to define what "working" means, measure it, and hold the system to that definition.

We propose **Eval-Driven Development**: a discipline where every probabilistic system starts with a specification of correctness, and nothing ships without automated proof that it meets that spec.

## Definitions

An **eval** is a dataset, a grader, and a harness. The grader and harness are built before you write code. The dataset evolves from synthetic to production-representative. The commitment to measure is there from the start, even if the full specifics cannot be known at project inception.

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
