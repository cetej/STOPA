---
name: Tools & Stack Decisions
description: Evaluated tools and stack decisions — OCR, TTS, browser, frontend, RAG, optimizers, MCP security
type: reference
originSessionId: 16b10457-62ed-45b8-91c1-49616a4950d4
---
Evaluated tools and technology decisions.

| Area | Tool/Decision | Status |
|------|--------------|--------|
| OCR | Tesseract/Marker/Claude Vision per project; GLM-OCR skipped (no Czech) | Active |
| TTS | Voxtral (no Czech), Voicebox + VoxCPM2 (LoRA čeština candidate) | Blocked — no Czech yet |
| Browser automation | Camofox (anti-detection MCP, 7.5/10 ADOPT), Priority 0 in /browse | Active |
| Frontend | Pretext (CSS-free text layout, 120fps, no DOM reflow) | Reference |
| RAG | Enterprise checklist (8 items), colBERT vs embedding distinction | Active for ORAKULUM |
| Optimizers | Prodigy (LoRA), AdamW (default), Schedule-Free, SAM, Lion | Reference |
| MCP security | mcp-scan: tool poisoning detector (hidden docstring instructions) | Run on all configs |
| Video production | OpenMontage: 7D provider scoring, delivery promise — adopted (ADR 0014) | Active |
| Agent code | Claw Code: permission deny-lists, 6 MCP transports, QueryEngine | Reference |
| Anthropic key | In DANE/.env and NG-ROBOT — never ask user | Active |
