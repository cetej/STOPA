---
date: 2026-04-18
source: https://arxiv.org/abs/2603.13424
type: paper
title: "Agent Privilege Separation in OpenClaw: A Structural Defense Against Prompt Injection"
authors: Darren Cheng, Wen-Kwang Tsao
tags: [security, prompt-injection, privilege-separation, agent-safety, structured-output]
---

## Summary

Structural defense combining two-agent pipeline with privilege separation/tool partitioning plus JSON formatting that strips persuasive natural language before processing. On 649 attacks from Microsoft LLMail-Inject benchmark: 0% attack success rate. Agent isolation = ~323× improvement over baseline; JSON formatting alone = ~7× improvement. OS-style privilege separation applied to LLM agent design.

## Key Concepts

- Two-agent pipeline: privilege separation + tool partitioning
- JSON formatting strips persuasive NL before processing
- Agent isolation dominant factor (323× vs baseline)
- 0% attack success rate on 649 LLMail-Inject attacks
- OS-style privilege separation for LLM agents

## Claims

- Full pipeline: 0% attack success rate on 649 attacks
- Agent isolation: ~323× improvement over baseline
- JSON formatting alone: ~7× improvement
- Privilege separation > output formatting as defense mechanism

## Entities

Authors: Darren Cheng, Wen-Kwang Tsao
Platform: OpenClaw
Benchmark: Microsoft LLMail-Inject (Greshake et al., 2024), 649 attacks
