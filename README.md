# simulation-parc

**Multi-domain simulation platform built on [MiroFish](https://github.com/666ghj/MiroFish) swarm intelligence.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Vue 3](https://img.shields.io/badge/vue-3-4FC08D?style=flat-square&logo=vue.js&logoColor=white)](https://vuejs.org)
[![Flask](https://img.shields.io/badge/flask-backend-000?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![D3.js](https://img.shields.io/badge/d3.js-graphs-F9A03C?style=flat-square&logo=d3.js&logoColor=white)](https://d3js.org)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue?style=flat-square)](LICENSE)

---

Upload seed materials. Describe what you want to predict in natural language. Get back a detailed prediction report and an interactive digital world where thousands of agents with independent personalities, long-term memory, and behavioral logic evolve and surface emergent outcomes.

## What it does

| Domain | Description |
|--------|-------------|
| **Social Media** | Public opinion dynamics, viral spread, sentiment shifts |
| **Markets** | Financial signal propagation, price discovery, trading behavior |
| **Supply Chain** | Logistics bottleneck detection, demand cascade, inventory simulation |
| **Custom** | Bring your own domain -- novels, policy drafts, geopolitics, anything |

## Architecture

```
seed materials (news, reports, novels)
        |
        v
  +--------------+     +------------------+
  | Graph Builder | --> | Knowledge Graph   |
  | (GraphRAG)    |     | (Zep memory)      |
  +--------------+     +------------------+
        |
        v
  +--------------+     +------------------+
  | OASIS Engine  | --> | Agent Simulation  |
  | (multi-agent) |     | (personality,     |
  +--------------+     |  memory, behavior)|
        |               +------------------+
        v
  +--------------+
  | Report Agent  | --> prediction report + interactive world
  +--------------+
```

**Backend** -- Python 3.11+ / Flask. Domain modules (`social_media`, `market`, `supply_chain`, `custom`) with shared services for graph building, simulation management, ontology generation, and Zep-powered entity memory.

**Frontend** -- Vue 3 / Vite with D3.js graph visualization, domain selector, simulation controls, history database, and report viewer.

## Quick start

### Option A: Docker (fastest)

```bash
cp .env.example .env
# fill in LLM_API_KEY, ZEP_API_KEY

docker compose up -d
```

Frontend at `localhost:3000`, API at `localhost:5001`.

### Option B: Source

**Prerequisites:** Node.js 18+, Python 3.11--3.12, [uv](https://github.com/astral-sh/uv)

```bash
cp .env.example .env
# fill in your keys

npm run setup:all   # installs node + python deps
npm run dev          # starts frontend + backend concurrently
```

Or start them separately:

```bash
npm run backend     # Flask API on :5001
npm run frontend    # Vite dev server on :3000
```

### Environment variables

| Variable | Required | Notes |
|----------|----------|-------|
| `LLM_API_KEY` | Yes | Any OpenAI-compatible API key |
| `LLM_BASE_URL` | Yes | API endpoint URL |
| `LLM_MODEL_NAME` | Yes | Model identifier |
| `ZEP_API_KEY` | Yes | Free tier at [getzep.com](https://app.getzep.com/) is enough |
| `LLM_BOOST_*` | No | Optional accelerated model config |
| `ADMIN_USER` / `ADMIN_PASSWORD` | No | Dashboard auth (defaults: admin / changeme) |

## How a simulation runs

1. **Graph building** -- seed extraction, entity/relationship mapping, GraphRAG construction
2. **Environment setup** -- persona generation, agent configuration, memory injection
3. **Simulation** -- dual-platform parallel execution with dynamic temporal memory updates
4. **Report generation** -- ReportAgent synthesizes findings with deep interaction support
5. **Deep interaction** -- chat with any agent in the simulated world post-run

## Project structure

```
backend/
  app/
    api/            # REST endpoints (auth, simulation, graph, report, domains)
    domains/        # domain modules: social_media, market, supply_chain, custom
    models/         # project + task data models
    services/       # graph builder, simulation runner/manager, report agent,
                    #   ontology generator, Zep tools, text processor
frontend/
  src/
    api/            # client-side API layer
    components/     # DomainSelector, GraphPanel, HistoryDatabase, etc.
    composables/    # Vue composables
    views/          # page-level components
    store/          # state management
    router/         # SPA routing
```

## Attribution

Fork of [MiroFish](https://github.com/666ghj/MiroFish) by the 666ghj team, powered by the [OASIS](https://github.com/camel-ai/oasis) simulation engine from CAMEL-AI. Licensed under AGPL-3.0.
