# Simba

A fully self-hosted personal AI assistant — no OpenAI, no Claude, no external LLM API.
Open-source model (Llama/Mistral) served locally via Ollama/vLLM, with a hand-built
RAG pipeline, hand-built agent orchestration, and LoRA/PEFT fine-tuning on top.

## Status

Phase 1 — Self-hosted foundation. Not yet functional — scaffold only.

## Structure

- `app/` — production code (llm client, rag, orchestration, voice, memory, briefing)
- `finetune/` — LoRA/PEFT fine-tuning scripts
- `eval/` — automated eval harness (answer quality, tool-use accuracy, latency)
- `data/` — personal corpus for RAG (gitignored, never pushed)
- `scratch/` — weekend practice exercises, not production code
- `tests/` — unit + integration tests
- `docs/` — architecture diagram, latency budget

## Setup

See `docs/architecture.md` (TBD) for the full plan. First milestone: a self-hosted
model responding via Ollama, no external API calls anywhere in the stack.
