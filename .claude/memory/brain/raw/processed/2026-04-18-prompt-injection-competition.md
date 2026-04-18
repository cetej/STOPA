---
date: 2026-04-18
source: https://arxiv.org/abs/2603.15714
type: paper
title: "How Vulnerable Are AI Agents to Indirect Prompt Injections? Insights from a Large-Scale Public Competition"
authors: Mateusz Dziemian, Maxwell Lin, Xiaohan Fu, Andy Zou, Lama Ahmad, et al.
tags: [security, prompt-injection, red-teaming, agent-safety, vulnerability]
---

## Summary

Large-scale red-teaming competition: 464 participants, 272,000 attack attempts, 13 frontier models, 41 scenarios, 8,648 successful attacks. Critical finding: harmful actions can succeed without visible traces in user-facing responses. Universal attack strategies transferable across model families in 21/41 behaviors. Capability-robustness correlation is weak: Claude Opus 4.5 = 0.5% attack success rate, Gemini 2.5 Pro = 8.5%.

## Key Concepts

- Indirect prompt injection: attacks via tool call results, not user input
- Attack concealment: harmful actions succeed without user-visible traces
- Universal attacks: transferable across model families (21/41 behaviors)
- Capability ≠ robustness: more capable models not necessarily safer
- 0.5% (Claude Opus 4.5) vs 8.5% (Gemini 2.5 Pro) attack success rate

## Claims

- 8,648 successful attacks out of 272,000 attempts
- 21/41 attack behaviors had universal cross-model strategies
- Harmful actions often leave no visible trace in user-facing output
- Weak correlation between model capability and injection robustness

## Entities

Authors: Mateusz Dziemian, Maxwell Lin, Xiaohan Fu, Andy Zou, Lama Ahmad, Kamalika Chaudhuri, Sahana Chennabasappa, Zico Kolter, Matt Fredrikson (+25 more)
Institutions: Meta, CMU
Models: Claude Opus 4.5 (0.5% ASR), Gemini 2.5 Pro (8.5% ASR)
