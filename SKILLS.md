# Skills

What I've actually used, and where. My project repositories are private for now (one is a live Kaggle competition, one a commercial service), so the "where" column names the project, and I'm happy to walk through any of them.

How to read the levels:

- **Heavy use**: built with it repeatedly, across projects, with tests around it
- **Used**: built something real with it in at least one project
- **Familiar**: understand it and have touched it, but haven't relied on it

Projects referred to below:

- **CASMI 2026**: Kaggle competition, identifying molecules from tandem mass spectra
- **macaroonnetwork**: a live marketplace where AI agents pay for data, with payment settling only if the result passes a check
- **Polymathica**: computational physics lab: PDE and CFD solvers and experiments
- **Graphics Core**: Polymathica's scientific visualisation and evidence subsystem
- **PSIC**: a scientific reasoning and memory core

## Programming and data

| Skill | Level | Where |
|---|---|---|
| Python | Heavy use | every project |
| SQL (Postgres) | Used | macaroonnetwork: schema migrations (Alembic), queries for search, snapshots and change events |
| NumPy, SciPy | Heavy use | CASMI, Polymathica |
| pandas | Used | CASMI |
| Jupyter / Kaggle notebooks | Heavy use | CASMI (offline GPU notebooks, embedded modules) |
| CSV, JSON, Parquet | Heavy use | CASMI (2.5 million spectra, streamed by row group) |
| Data cleaning and validation | Heavy use | CASMI, macaroonnetwork |
| Exploratory data analysis | Used | CASMI |
| Large-scale data processing | Used | CASMI: indexes over 2.5M spectra in flat arrays to fit in memory |
| Pipelines / ETL | Used | macaroonnetwork (scrape, snapshot, diff, append-only history), CASMI |

## Machine learning and evaluation

| Skill | Level | Where |
|---|---|---|
| scikit-learn | Used | CASMI (gradient-boosted ranker, metrics) |
| PyTorch | Used | CASMI (spectrum-to-fingerprint transformer, forward spectrum model), Polymathica |
| Gradient boosting (HistGradientBoosting) | Used | CASMI: learned combiner, sealed as a failed experiment and reported as one |
| Model training and evaluation | Heavy use | CASMI |
| Train / validation / test design | Heavy use | CASMI: structure-disjoint splits, purpose-built holdouts |
| Ablations and baselines | Heavy use | CASMI: every change scored against a baseline re-run in the same script |
| Ranking, retrieval, similarity search | Heavy use | CASMI: candidate retrieval and ranking, spectral similarity |
| MRR@K, Recall@K, top-K | Heavy use | CASMI |
| Leakage and contamination detection | Heavy use | CASMI: checked a pretrained model's training data against our test sets before trusting it |
| Experiment design and pre-registration | Heavy use | CASMI: pass rules frozen before each run, one-shot evaluation scripts |
| Independent metric recomputation | Used | CASMI: found a 33-row disagreement between the published dataset size and the file, and confirmed it three ways |
| Cross-validation, hyperparameter search, feature selection | Familiar | |

## AI and LLM engineering

| Skill | Level | Where |
|---|---|---|
| Multi-agent workflows (Claude, Codex, Cline) | Heavy use | all projects: role-separated agents, written handovers, freeze-and-review |
| AI-assisted software development | Heavy use | all projects |
| Prompt engineering | Heavy use | all projects |
| Tool-using agents, MCP | Used | macaroonnetwork: an MCP server published on PyPI |
| RAG / GraphRAG | Used | PSIC (LightRAG over a research corpus) |
| Vector / semantic search | Used | macaroonnetwork (pgvector listing search) |
| Long-term agent memory | Used | PSIC (episodic, semantic and procedural memory) |
| AI governance, evidence-based workflows | Heavy use | all projects: constitutions with fixed rule IDs, validation gates, claim labelling |
| LLM evaluation | In progress | this repo |

## Scientific computing

| Skill | Level | Where |
|---|---|---|
| Physics-informed neural networks (PINNs) | Used | Polymathica, Graphics Core |
| Numerical simulation, PDEs, CFD, Navier-Stokes | Used | Polymathica |
| Heat and diffusion simulation | Used | Polymathica |
| JAX | Used | Graphics Core, Polymathica |
| NVIDIA PhysicsNeMo | Used | Graphics Core, Polymathica |
| GPU computing, CUDA-aware workflows, VRAM budgeting | Used | Polymathica, CASMI (Kaggle GPU sessions, CPU/GPU workload split) |
| Scientific validation (dimensional analysis, conservation, CFL checks) | Used | PSIC, Polymathica |
| Reproducibility and provenance | Heavy use | all projects: SHA-256 artifact checks, sealed versions |

## Cheminformatics and mass spectrometry

| Skill | Level | Where |
|---|---|---|
| RDKit, SMILES, InChI | Heavy use | CASMI |
| Molecular fingerprints and similarity | Heavy use | CASMI |
| LC-MS/MS and tandem mass spectra | Heavy use | CASMI |
| Spectral similarity (entropy, modified cosine) | Heavy use | CASMI |
| Candidate retrieval and ranking | Heavy use | CASMI |
| Structure-disjoint evaluation | Heavy use | CASMI |

## Software engineering and operations

| Skill | Level | Where |
|---|---|---|
| Git, GitHub, commit-level provenance | Heavy use | all projects |
| Automated testing (pytest) | Heavy use | all projects, about 680 test files in total |
| Property-based testing (Hypothesis) | Familiar | Graphics Core, macaroonnetwork stack |
| Spec-and-gate development (executable acceptance gates) | Heavy use | macaroonnetwork: 26 specs, each with a gate script |
| FastAPI, REST APIs, Pydantic | Used | macaroonnetwork, Polymathica, PSIC |
| Docker Compose, Caddy, VPS deployment, SSH | Used | macaroonnetwork (production), CASMI (deploy remote) |
| Celery, Redis | Used | macaroonnetwork |
| GitHub Actions / CI | Familiar | |
| Payments engineering (Lightning L402, x402 USDC, idempotency, integer money) | Used | macaroonnetwork: live on mainnet |
| Windows / PowerShell, Linux, WSL | Heavy use | all projects |
| Python packaging | Used | macaroonnetwork (PyPI release) |

## Visualisation and web

| Skill | Level | Where |
|---|---|---|
| Scientific visualisation | Heavy use | Graphics Core: deterministic renders, no figure without recorded data |
| Experiment dashboards, live monitoring | Used | Polymathica, CASMI |
| Server-Sent Events | Used | Polymathica |
| HTML, CSS, JavaScript | Used | Polymathica, Graphics Core |
| Next.js | Used | macaroonnetwork (public marketplace site) |
| Technical writing and documentation | Heavy use | all projects: handovers, freeze documents, write-ups |

## Background

Professional photography and visual communication. It's where the habit came from of not letting a picture say more than the data behind it.
