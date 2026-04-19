# eSim Copilot – Chatbot Enhancement Proposal

**Focus:** Hariom's approach (PR 434)  
**Branch:** Chatbot_Enhancements  
**Date:** March 2025

---

# Part 1: Document Summary

## 1.1 Four Source Documents

| Document | Author | Focus |
|----------|--------|-------|
| **Project Context.pdf** | Synthesis | Rationale, problems, comparison of 3 interns, proposed Federated Knowledge Sync |
| **5 hariom.pdf** | Hariom Thakur | Full technical report: RAG, vision, FACT-based netlist, PyQt5 integration, automated error capture |
| **18 radhika goyal.pdf** | Radhika Goyal | Rule-based fault identification, static schematic/netlist analysis, cross-validation |
| **1 Nicholas_Coutinho.pdf** | Nicholas Coutinho | Conversational memory, topic discontinuity, context retention |

## 1.2 Three Intern Approaches (from Project Context)

| Aspect | Radhika | Nicholas | **Hariom** |
|--------|---------|----------|-------------|
| **Intelligence** | Proactive static analysis, rule-based | Conversational memory, topic discontinuity | **FACT-based netlist, strict RAG grounding** |
| **UI Integration** | Standard chat | Standard chat | **Deep PyQt5: dock, toolbar, context menus, auto error capture** |
| **Multimodal** | Text + image | Text + image | **Text + image + voice (Vosk)** |
| **Tech stack** | Broad | Broad | **Specific: qwen2.5:3b, minicpm-v, nomic-embed-text, ChromaDB** |

**Project Context conclusion:** Hariom's approach is best for **practical deployment & user experience** due to deep integration, automated error capture, and voice STT.

---

# Part 2: Current Chatbot Functionality (Hariom's Implementation)

## 2.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Presentation Layer (PyQt5)                                              │
│  • Application.py: toolbar, openChatbot(), errorDetectedSignal           │
│  • Chatbot.py: dock widget, chat UI, input, image/voice buttons           │
│  • ProjectExplorer.py: context menu "Analyze this Netlist"                │
│  • DockArea.py: createchatbotdock()                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Processing Layer (chatbot_core.py)                                       │
│  • classify_question_type() → routing                                     │
│  • handle_esim_question(), handle_image_query(), handle_netlist_analysis()│
│  • handle_follow_up(), handle_simple_question()                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Data Layer                                                               │
│  • knowledge_base.py: ChromaDB, search_knowledge()                       │
│  • image_handler.py: PaddleOCR + MiniCPM-V                                │
│  • Chatbot.py: FACT-based netlist detection (_detect_floating_nodes, etc) │
│  • error_solutions.py: pattern → fixes mapping                           │
│  • ollama_runner.py: run_ollama(), run_ollama_vision(), get_embedding()   │
│  • stt_handler.py: Vosk offline STT                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2.2 Current Features (Implemented)

| Feature | Status | Location |
|---------|--------|----------|
| **Intelligent Router** | ✅ | `chatbot_core.py` – classify_question_type() |
| **RAG (ChromaDB)** | ✅ | `knowledge_base.py` – search_knowledge() |
| **FACT-based netlist** | ✅ | `Chatbot.py` – _detect_floating_nodes, _detect_missing_models, etc. |
| **Vision (PaddleOCR + MiniCPM-V)** | ✅ | `image_handler.py` – analyze_and_extract() |
| **Voice (Vosk)** | ✅ (optional) | `stt_handler.py` |
| **Project Explorer context menu** | ✅ | `ProjectExplorer.py` – "Analyze this Netlist" |
| **Automated error capture** | ✅ | `Application.py` – errorDetectedSignal → send_error_to_chatbot |
| **Dockable chat** | ✅ | `Chatbot.py`, `DockArea.py` |
| **Error pattern matching** | ✅ | `error_solutions.py` – ERROR_SOLUTIONS dict |

## 2.3 Current Gaps / Limitations (from Hariom's report)

1. **Model capability constraints:** qwen2.5:3b struggles with complex multi-step reasoning; minicpm-v misinterprets complex topologies; 2048-token context limit.
2. **Performance on low-end hardware:** 8GB RAM minimum; vision can take 10+ seconds on older CPUs.
3. **Scope limitations:** No training mode; fixed knowledge base; cannot dynamically add new docs.
4. **PaddleOCR:** Often fails on first run (no `paddle` module) – vision falls back to partial OCR.
5. **Netlist contract:** Missing `manuals/esim_netlist_analysis_output_contract.txt` in some setups.

---

# Part 3: Proposed Enhancements (Hariom’s Approach)

## 3.1 Near-Term (Next 6 Months) – from Hariom's report

### 3.1.1 One-Click Netlist Fix

**Current:** Copilot suggests fixes; user must manually edit in Spice Editor.

**Proposal:** Add "Apply fix" button that auto-inserts suggested fixes into `.cir.out`:

- Add missing `.model` statements
- Add `.options gmin=1e-12 reltol=0.01` for singular matrix
- Add 1G resistors for floating nodes (as comments with copy-paste snippet)

**Implementation:** Extend `Chatbot.py` – parse FACT output, generate patch, offer "Insert into netlist" action.

---

### 3.1.2 Real-Time Suggestions in KiCad

**Current:** User must open Copilot and ask.

**Proposal:** Optional "live hints" during schematic capture – e.g. when floating pin detected, show small tooltip: "R1 pin 2 is unconnected."

**Implementation:** Requires KiCad callback or periodic checks; may need eSim/KiCad integration points.

---

### 3.1.3 Batch Processing for Multiple Images/Netlists

**Current:** One image or netlist at a time.

**Proposal:** Allow selecting multiple `.cir.out` files or pasting multiple images; run analysis in batch; report summary.

**Implementation:** Extend `Chatbot.py` – `analyze_specific_netlist()` accepts list; `handle_image_query()` can process multiple paths.

---

### 3.1.4 RAG Relevance Threshold

**Current:** `knowledge_base.py` returns top 4 chunks; no explicit cosine similarity filter.

**Proposal:** Add relevance threshold (e.g. cosine similarity > 0.3) – Hariom's report mentions this; filter out low-similarity chunks to reduce hallucination.

**Implementation:** ChromaDB query returns `distances`; filter by threshold before context assembly.

---

### 3.1.5 Stricter FACT-Based Prompting

**Current:** Netlist analysis uses FACT blocks; contract file may be missing.

**Proposal:** Ensure contract is always available; bundle `esim_netlist_analysis_output_contract.txt` in repo; add fallback inline prompt if file missing.

**Implementation:** Copy contract to `src/manuals/` or `src/frontEnd/manuals/`; ensure `Chatbot.py` loads from correct path.

---

### 3.1.6 Model Selection (Optional)

**Current:** Hardcoded qwen2.5:3b, minicpm-v.

**Proposal:** Allow user to choose model in settings (e.g. llama3, deepseek-coder for code-heavy tasks).

**Implementation:** Add `ollama_model` config; pass to `run_ollama()`.

---

## 3.2 Medium-Term (6–18 Months)

### 3.2.1 Circuit Optimization Suggestions

**Proposal:** After simulation succeeds, analyze output and suggest improvements (e.g. "Add capacitor for stability").

**Implementation:** Parse `.raw` or simulation output; integrate with plotting tools; add optional "optimization" analysis mode.

---

### 3.2.2 Predictive Error Detection During Schematic Capture

**Proposal:** (Radhika's strength) – cross-validate schematic vs netlist before simulation; detect mismatches early.

**Implementation:** Hook into eSim's netlist generation; run static analysis on generated netlist before user runs simulation.

---

### 3.2.3 Enhanced Conversation Memory (Nicholas's strength)

**Proposal:** Improve topic discontinuity detection; add reference resolution for "this", "that", "it".

**Implementation:** Refine `_is_follow_up_question()` and `is_semantic_topic_switch()`; use embedding similarity for pronoun resolution.

---

### 3.2.4 Federated Knowledge Sync (Project Context proposal)

**Proposal:** When user fixes an error after Copilot failed, prompt: "What did you change?" – store locally; optionally sync anonymously to FOSSEE server; server clusters fixes; push updates to ChromaDB.

**Implementation:** Large; requires server, encryption, consent UI. Defer to long-term.

---

## 3.3 Long-Term (18+ Months)

- **Autonomous design assistance:** Circuit synthesis from specs.

- **Research platform:** Dataset from anonymized interactions; benchmarking suite.

- **Ecosystem expansion:** Port to OpenModelica, Scilab; plugin architecture.

---

# Part 4: Prioritized Implementation Roadmap

| Priority | Enhancement | Effort | Impact |
|----------|-------------|--------|--------|
| 1 | RAG relevance threshold | Low | High (reduces hallucination) |
| 2 | Netlist contract bundling | Low | Medium (fixes missing contract) |
| 3 | One-click netlist fix | Medium | High (UX) |
| 4 | Batch netlist analysis | Low | Medium |
| 5 | Model selection in settings | Low | Medium |
| 6 | Enhanced conversation memory | Medium | Medium |
| 7 | Batch image processing | Low | Low |
| 8 | Real-time KiCad hints | High | Medium |

---

# Part 5: Quick Wins (Immediate)

1. **Add relevance threshold to `search_knowledge()`** – filter by distance/similarity.
2. **Bundle netlist contract** – ensure `esim_netlist_analysis_output_contract.txt` is in `src/manuals/` or `src/frontEnd/manuals/` and loaded correctly.
3. **Improve error message clarity** – when PaddleOCR fails, show: "Vision analysis unavailable. Text and netlist analysis still work."
4. **Add "Copy to clipboard" for netlist fixes** – so user can paste without manual retyping.

---

# Part 6: File Reference

| File | Purpose |
|------|---------|
| `src/chatbot/chatbot_core.py` | Router, handlers, classification |
| `src/chatbot/knowledge_base.py` | ChromaDB, search_knowledge |
| `src/chatbot/ollama_runner.py` | Ollama API, embeddings |
| `src/chatbot/image_handler.py` | PaddleOCR, MiniCPM-V |
| `src/chatbot/stt_handler.py` | Vosk STT |
| `src/chatbot/error_solutions.py` | Error pattern → fixes |
| `src/frontEnd/Chatbot.py` | UI, netlist FACT detection, analyze_specific_netlist |
| `src/frontEnd/Application.py` | errorDetectedSignal, openChatbot |
| `src/frontEnd/ProjectExplorer.py` | Context menu |
