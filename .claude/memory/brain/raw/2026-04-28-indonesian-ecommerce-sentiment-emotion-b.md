---
title: Klasifikace sentimentu a emocí v indonéských e-shop recenzích
url: http://arxiv.org/abs/2604.24720v1
date: 2026-04-28
concepts: ["Multi-Task Learning", "BiLSTM", "Sentiment Analysis", "Emotion Classification", "AutoML", "Indonesian NLP", "TF-IDF", "Slang Normalization"]
entities: ["Hermawan Manurung", "Ibrahim Al-Kahfi", "Ahmad Rizqi", "Martin Clinton Tosima Manullang", "Institut Teknologi Sumatera", "PyCaret", "PyTorch", "Hugging Face Spaces"]
source: brain-ingest-local
---

# Klasifikace sentimentu a emocí v indonéských e-shop recenzích

**URL**: http://arxiv.org/abs/2604.24720v1

## Key Idea

Výzkum porovnává Multi-Task BiLSTM a AutoML přístupy pro klasifikaci sentimentu a emocí v 5 400 indonéských produktových recenzích z 29 e-commerce kategorií, s důrazem na preprocessing slangových výrazů a emoji.

## Claims

- Indonéské recenze míchají standardní slovník se slangem, regionálními výpůjčkami, numerickými zkratkami a emoji, což znemožňuje použití lexikálních sentimentových nástrojů
- Dataset PRDECT-ID obsahuje 5 400 produktových recenzí z 29 kategorií, každá označená binárním sentimentem (Pozitivní/Negativní) a pětitřídní emocí (Štěstí, Smutek, Strach, Láska, Hněv)
- Preprocessing modul aplikuje 14 sekvenčních kroků včetně 140položkového slovníku slangu sestaveného z marketplace korpusů

## Relevance for STOPA

Demonstrovat Multi-Task Learning architektury a preprocessing pipeline pro komplexní NLP úlohy s nestrukturovaným, slangem zatíženým textem – relevantní pro orchestraci heterogenních klasifikačních modelů v STOPA.
