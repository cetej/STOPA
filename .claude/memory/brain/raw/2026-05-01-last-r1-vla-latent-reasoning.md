---
title: LaST-R1: VLA model s latentním uvažováním pro robotickou manipulaci
url: http://arxiv.org/abs/2604.28192v1
date: 2026-05-01
concepts: ["Vision-Language-Action (VLA)", "latentní Chain-of-Thought (CoT)", "Latent-to-Action Policy Optimization (LAPO)", "online reinforcement learning", "robotická manipulace", "adaptivní uvažování", "fyzikální modelování"]
entities: ["Hao Chen", "Jiaming Liu", "Shanghang Zhang", "Pheng-Ann Heng", "LIBERO benchmark"]
source: brain-ingest-local
---

# LaST-R1: VLA model s latentním uvažováním pro robotickou manipulaci

**URL**: http://arxiv.org/abs/2604.28192v1

## Key Idea

LaST-R1 je framework pro Vision-Language-Action modely, který kombinuje latentní Chain-of-Thought uvažování o fyzikální dynamice s online reinforcement learningem (LAPO algoritmus), umožňující robotům adaptivně přizpůsobovat hloubku uvažování podle složitosti úlohy.

## Claims

- LaST-R1 dosahuje 99,8% průměrné úspěšnosti na LIBERO benchmarku s pouze jednou ukázkou supervised učení
- LAPO post-training přináší až 44% zlepšení oproti počáteční politice v reálném nasazení napříč čtyřmi komplexními úlohami
- Existující VLA přístupy optimalizují pouze akční prostor a obcházejí proces fyzikálního uvažování, což omezuje adaptabilitu
- Adaptivní latentní CoT mechanismus umožňuje politice dynamicky přizpůsobovat horizont uvažování podle složitosti prostředí

## Relevance for STOPA

Demonstruje pokročilý přístup k integraci uvažování do akcí AI agentů, kde adaptivní latentní uvažování může inspirovat orchestraci multi-agentních systémů s dynamickou alokací výpočetních zdrojů podle složitosti úloh.
