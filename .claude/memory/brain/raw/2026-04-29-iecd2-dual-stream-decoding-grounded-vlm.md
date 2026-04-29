---
title: IECD2: Kontrastní dual-stream dekódování pro vizuálně zakotvené VLM
url: http://arxiv.org/abs/2604.25809v1
date: 2026-04-29
concepts: ["Vision-Language Models", "kontrastní dekódování", "dual-stream architektura", "vizuální grounding", "redukce halucinací", "KL divergence", "VQA"]
entities: ["Yashwant Pravinrao Bangde", "Debaditya Roy", "POPE", "MME", "VQAv2", "AMBER", "MS-COCO", "LLaVA-Bench"]
source: brain-ingest-local
---

# IECD2: Kontrastní dual-stream dekódování pro vizuálně zakotvené VLM

**URL**: http://arxiv.org/abs/2604.25809v1

## Key Idea

Nová dekódovací metoda pro Vision-Language modely, která paralelně udržuje dva proudy tokenů – jeden řízený instrukcí (expresivní) a druhý vizuálním důkazem (zakotvený) – a adaptivně je fúzuje pomocí KL divergence, čímž redukuje halucinace při zachování informativnosti odpovědí.

## Claims

- Instruction prompting zhoršuje problém halucinací u VLM tím, že zesiluje jazykové priory zejména při nejistém vizuálním signálu
- IECD2 metoda dosahuje konzistentního zlepšení v task accuracy a reasoning performance oproti state-of-the-art dekódovacím přístupům
- Symetrická KL-based kontrast-based brána dokáže potlačit tokeny preferované jazykovými priory, ale nepodpořené vizuálním důkazem

## Relevance for STOPA

Pro STOPA orchestraci multimodálních AI agentů je klíčová schopnost VLM generovat odpovědi skutečně zakotvené ve vizuálních datech – IECD2 ukazuje architektonický vzor pro balancování expresivity a faktické správnosti, což je kritické pro spolehlivou agent orchestraci.
