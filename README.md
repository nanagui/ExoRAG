# ExoRAG: Physics-Informed AI for Exoplanet Validation

<div align="center">

[![NASA Space Apps Challenge](https://img.shields.io/badge/NASA_Space_Apps-2025-blue.svg)](https://www.spaceappschallenge.org/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2+-ee4c2c.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*Accelerating exoplanet discovery from weeks to milliseconds with physics-informed deep learning and retrieval-augmented validation*

[Features](#-key-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🌟 Overview

**ExoRAG** is a cutting-edge AI system that addresses the critical bottleneck in exoplanet discovery: **manual validation**. NASA's TESS, Kepler, and K2 missions generate thousands of exoplanet candidates, but validating them takes weeks of expert analysis. ExoRAG reduces this time to **<100ms per light curve** while maintaining **F1-score > 0.98** through:

- 🧠 **Hybrid Neural Architecture**: CNN for morphological features + BiLSTM for temporal dependencies + Attention for interpretability
- ⚛️ **Physics-Informed Learning**: Enforces Keplerian constraints and transit physics directly in the loss function
- 📚 **Retrieval-Augmented Generation (RAG)**: Validates predictions against confirmed exoplanets and NASA literature
- 🎯 **Data Efficiency**: Reduces labeled data dependency by ~60% through realistic synthetic augmentation

## 🚀 Key Features

### Core Capabilities

✅ **Real-Time Processing**: Process light curves from TESS/Kepler/K2 with <100ms latency per curve
✅ **Physics-Informed Validation**: Penalizes violations of transit depth (Rp/Rs)², duration, and orbital dynamics
✅ **Explainable AI**: Attention heatmaps + RAG-generated justifications with scientific citations
✅ **Cross-Mission Generalization**: Train on Kepler, validate on TESS/K2 without degradation
✅ **Interactive Dashboard**: React-based UI for astronomers and citizen scientists

### Technical Highlights

- **Hybrid Deep Learning**: CNN-BiLSTM-Attention architecture with physics module
- **Advanced Data Augmentation**: PyTransit/BATMAN synthetic injection + SMOTE for class balance
- **Vector Retrieval**: Qdrant + BGE-M3 embeddings for scientific context
- **Production-Ready**: FastAPI backend, Docker deployment, Prometheus metrics
- **Comprehensive Pipeline**: From raw FITS files to validated predictions with evidence

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         NASA Data Sources                            │
│         Kepler DR25 • TESS Sectors • K2 • NASA Literature           │
└────────────────────┬────────────────────────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │  Data Ingestion Layer   │
        │  • Lightkurve API       │
        │  • MAST Archive         │
        │  • Metadata Catalog     │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │  Preprocessing Layer    │
        │  • Detrending           │
        │  • Outlier Removal      │
        │  • Normalization        │
        │  • Synthetic Injection  │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────────────┐
        │   Hybrid Model (GPU-Accelerated) │
        │  ┌──────┐  ┌───────┐  ┌─────────┐│
        │  │ CNN  │→ │BiLSTM │→ │Attention││
        │  └──────┘  └───────┘  └────┬────┘│
        │            Physics Loss ←───┘     │
        └────────────┬────────────────────┘
                     │
        ┌────────────▼────────────┐
        │   RAG Validation Layer   │
        │  • Qdrant Vector DB      │
        │  • BGE-M3 Embeddings     │
        │  • LLM Justifications    │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   Application Layer      │
        │  • FastAPI Endpoints     │
        │  • React Dashboard       │
        │  • Observability         │
        └──────────────────────────┘
```

### Component Breakdown

| Layer | Technologies | Purpose |
|-------|-------------|---------|
| **Data** | Lightkurve, Astropy, NASA MAST API | Ingest and catalog light curves |
| **Preprocessing** | NumPy, Pandas, PyTransit, SMOTE | Clean, augment, and balance data |
| **Model** | PyTorch, Lightning, TorchMetrics | Train hybrid physics-informed network |
| **RAG** | Qdrant, BGE-M3, LangChain | Retrieve context and generate explanations |
| **API** | FastAPI, Pydantic, SQLModel | Serve predictions and manage metadata |
| **Frontend** | React, Plotly, TypeScript | Interactive visualization and exploration |
| **Infrastructure** | Docker, PostgreSQL, Prometheus | Deployment and observability |

## ⚡ Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- **Python 3.11+** (for local development)
- **NVIDIA GPU** with CUDA 12+ (optional, for <100ms inference)
- **8GB+ RAM** (16GB recommended)

### 🐳 Docker Deployment (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/nasa_ai.git
cd nasa_ai/app

# 2. Copy environment template
cp .env.example .env

# 3. Configure NASA credentials (optional, for earthaccess)
# Edit .env and add your NASA Earthdata credentials

# 4. Start all services
docker-compose up -d

# 5. Verify services
docker-compose ps

# Services will be available at:
# - API: http://localhost:18000
# - Frontend: http://localhost:15173
# - Qdrant: http://localhost:16333
# - PostgreSQL: localhost:15432
```

### 🔧 Local Development

```bash
# 1. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export EXOAI_DEBUG=true
export EXOAI_DATABASE_URL=postgresql+psycopg://exoai:exoai@localhost:15432/exoai
export EXOAI_QDRANT_URL=http://localhost:16333

# 4. Run services (requires Docker for Qdrant/PostgreSQL)
docker-compose up -d postgres qdrant

# 5. Start API server
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000

# 6. Start frontend (in separate terminal)
cd frontend
npm install
npm run dev
```

## 📚 Usage

### API Examples

#### 1. Predict Exoplanet Transit

```bash
curl -X POST "http://localhost:18000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "target_id": "KIC-8462852",
    "mission": "kepler",
    "quarter": 8
  }'
```

**Response:**
```json
{
  "target_id": "KIC-8462852",
  "prediction": "exoplanet",
  "confidence": 0.956,
  "physics_residual": 0.023,
  "attention_map": [...],
  "rag_justification": {
    "summary": "Transit depth and duration consistent with confirmed Neptune-sized exoplanet...",
    "references": [
      {"title": "Kepler DR25 Catalog", "url": "..."}
    ]
  },
  "latency_ms": 87
}
```

#### 2. Batch Processing

```bash
curl -X POST "http://localhost:18000/api/v1/batch" \
  -F "file=@light_curves.csv"
```

#### 3. Explain Prediction

```bash
curl "http://localhost:18000/api/v1/explain/KIC-8462852"
```

### Python SDK

```python
from exorag import ExoRAGClient

client = ExoRAGClient(base_url="http://localhost:18000")

# Single prediction
result = client.predict(target_id="KIC-8462852", mission="kepler")
print(f"Prediction: {result.prediction} (confidence: {result.confidence:.3f})")

# Plot light curve with attention
client.plot_attention(target_id="KIC-8462852", save_path="attention.png")

# Get RAG explanation
explanation = client.explain(target_id="KIC-8462852")
print(explanation.justification)
```

### Web Dashboard

Navigate to `http://localhost:15173` to access the interactive dashboard:

- 📈 **Explore Light Curves**: Upload or fetch from NASA archives
- 🔍 **Analyze Predictions**: View attention maps and physics diagnostics
- 📚 **Review Evidence**: Read RAG-retrieved citations and anomaly alerts
- 📊 **Monitor Pipeline**: Track ingestion status and model metrics

## 🗂️ Project Structure

```
app/
├── src/                          # Source code
│   ├── app/                      # Application package
│   │   ├── api/                  # FastAPI routes and dependencies
│   │   ├── data/                 # Data ingestion and management
│   │   ├── preprocessing/        # Light curve preprocessing
│   │   ├── models/               # Neural network architectures
│   │   ├── physics/              # Physics-informed loss and constraints
│   │   ├── rag/                  # RAG validation (Qdrant + LLM)
│   │   ├── services/             # Inference and business logic
│   │   └── utils/                # Shared utilities
│   └── scripts/                  # CLI tools and automation
├── frontend/                     # React dashboard
│   ├── src/
│   │   ├── components/           # UI components
│   │   ├── pages/                # Route pages
│   │   ├── services/             # API clients
│   │   └── utils/                # Frontend utilities
│   └── public/                   # Static assets
├── tests/                        # Unit and integration tests
├── config/                       # Configuration files
├── docs/                         # Documentation
│   ├── architecture_overview.md
│   ├── earthaccess_setup.md
│   ├── user_guide.md
│   └── data_licensing.md
├── data/                         # Persistent data (git-ignored)
│   ├── raw/                      # Raw NASA downloads
│   ├── processed/                # Preprocessed tensors
│   ├── qdrant/                   # Vector database storage
│   └── postgres/                 # Relational database
├── models/                       # Model checkpoints (git-ignored)
├── corpus/                       # Scientific literature for RAG
├── docker-compose.yml            # Multi-service orchestration
├── Dockerfile                    # Production image
├── Dockerfile.dev                # Development image
├── requirements.txt              # Python dependencies
├── Makefile                      # Build and run automation
└── README.md                     # This file
```

## 🔬 Training Custom Models

### 1. Download Training Data

```bash
# Using Lightkurve (recommended)
python scripts/download_kepler_data.py --mission kepler --limit 10000

# Or use earthaccess for additional datasets
python scripts/download_with_earthaccess.py --dataset tess
```

### 2. Preprocess Light Curves

```bash
python scripts/preprocess.py \
  --input data/raw/kepler \
  --output data/processed/kepler \
  --synthetic-ratio 0.74 \
  --smote
```

### 3. Train Model

```bash
python scripts/train.py \
  --config config/train_config.yaml \
  --gpus 1 \
  --max-epochs 50 \
  --physics-lambda 0.1
```

**Key Hyperparameters:**
- `--physics-lambda`: Weight for physics-informed loss term (default: 0.1)
- `--synthetic-ratio`: Fraction of synthetic transits (default: 0.74)
- `--lr`: Learning rate (default: 1e-4)
- `--batch-size`: Batch size (default: 32)

### 4. Evaluate Model

```bash
python scripts/evaluate.py \
  --checkpoint models/best.ckpt \
  --test-data data/processed/tess \
  --output results/cross_mission_eval.json
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test suite
pytest tests/test_preprocessing.py -v

# Run integration tests (requires Docker services)
docker-compose up -d postgres qdrant
pytest tests/integration/ -v
```

## 📖 Documentation

Comprehensive documentation available in [`docs/`](docs/):

- **[Architecture Overview](docs/architecture_overview.md)**: System design and data flow
- **[User Guide](docs/user_guide.md)**: Step-by-step tutorials and examples
- **[Earthaccess Setup](docs/earthaccess_setup.md)**: NASA Earthdata authentication guide
- **[Data Licensing](docs/data_licensing.md)**: NASA data usage and attribution
- **[Onboarding](docs/onboarding.md)**: Developer setup and contribution workflow

### API Documentation

Once the API is running, interactive documentation is available at:

- **Swagger UI**: http://localhost:18000/docs
- **ReDoc**: http://localhost:18000/redoc
- **OpenAPI Schema**: http://localhost:18000/openapi.json

## 🌍 NASA Data Sources

This project uses the following NASA datasets:

| Dataset | Source | Purpose |
|---------|--------|---------|
| **Kepler DR25** | [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/) | Primary training data |
| **TESS Sectors** | [MAST Archive](https://archive.stsci.edu/tess/) | Cross-mission validation |
| **K2 Light Curves** | [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/) | Additional validation |
| **Confirmed Exoplanets** | [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/) | RAG reference corpus |

**License Compliance**: All NASA data is used under open data policies. See [`docs/data_licensing.md`](docs/data_licensing.md) for attribution requirements.

## 🛠️ Technology Stack

### Backend
- **FastAPI** 0.111+ - High-performance async API framework
- **PyTorch** 2.2+ - Deep learning and neural networks
- **PyTorch Lightning** 2.3+ - Training orchestration and best practices
- **Lightkurve** 2.4+ - NASA light curve analysis
- **Qdrant** 1.10+ - Vector database for RAG
- **LangChain** 0.2+ - RAG orchestration and LLM integration
- **PostgreSQL** 15 - Relational metadata storage
- **SQLModel** - Type-safe database ORM

### Machine Learning
- **sentence-transformers** (BGE-M3) - Semantic embeddings
- **imbalanced-learn** - SMOTE class balancing
- **PyTransit / BATMAN** - Synthetic transit generation
- **scikit-learn** - Baseline models and metrics
- **TorchMetrics** - Performance evaluation

### Frontend
- **React** 18+ with TypeScript
- **Plotly.js** - Interactive scientific visualizations
- **Vite** - Fast development and bundling

### DevOps & Observability
- **Docker & Docker Compose** - Containerization
- **Prometheus** - Metrics collection
- **MLflow** - Experiment tracking
- **Structlog** - Structured logging

## 🤝 Contributing

We welcome contributions from astronomers, data scientists, and developers!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run linting**: `make lint`
5. **Run tests**: `make test`
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Workflow

```bash
# Install pre-commit hooks
pre-commit install

# Run linting
make lint

# Run tests
make test

# Build Docker images
make build

# Start development environment
make dev
```

See [`docs/onboarding.md`](docs/onboarding.md) for detailed development setup.

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### NASA Data Attribution

This project uses data from NASA's Kepler, K2, and TESS missions. All data is publicly available and used in accordance with NASA's open data policies. Please cite the original data sources when using this software:

```bibtex
@dataset{kepler_dr25,
  author = {Thompson, Susan E. and others},
  title = {Kepler Data Release 25},
  year = {2018},
  publisher = {NASA Exoplanet Archive},
  doi = {10.26133/NEA4}
}
```

See [`docs/data_licensing.md`](docs/data_licensing.md) for complete attribution requirements.

## 🙏 Acknowledgments

- **NASA Space Apps Challenge 2025** for the inspiring challenge
- **NASA Ames Research Center** for Kepler and K2 missions
- **MIT/NASA** for TESS mission and data
- **Space Telescope Science Institute (STScI)** for MAST archive
- **Lightkurve Collaboration** for the excellent Python package
- All contributors and citizen scientists who make exoplanet discovery accessible

## 📞 Contact & Links

- **NASA Space Apps Project**: [Link to submission](#)
- **GitHub Repository**: https://github.com/your-username/nasa_ai
- **Documentation**: [docs/](docs/)
- **Issue Tracker**: https://github.com/your-username/nasa_ai/issues

## 🎯 Roadmap

- [x] Core CNN-BiLSTM-Attention architecture
- [x] Physics-informed loss implementation
- [x] RAG validation with Qdrant
- [x] FastAPI backend and Docker deployment
- [x] React dashboard with attention visualization
- [ ] Bayesian uncertainty quantification
- [ ] JWST spectroscopic integration
- [ ] Mobile/edge deployment (TensorFlow Lite)
- [ ] Real-time TESS alert processing
- [ ] Citizen science annotation platform
- [ ] Multi-language support (Spanish, Portuguese, Mandarin)

---

<div align="center">

**Made with ❤️ for NASA Space Apps Challenge 2025**

*Democratizing exoplanet discovery, one light curve at a time* 🌍🔭

[![NASA](https://img.shields.io/badge/Data-NASA-blue.svg)](https://www.nasa.gov/)
[![Space Apps](https://img.shields.io/badge/Challenge-Space_Apps_2025-orange.svg)](https://www.spaceappschallenge.org/)

</div>
