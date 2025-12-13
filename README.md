# Job Title Standardization Pipeline

**Version:** 1.0  
**Status:** Development / RFC Review

## Overview

This project implements an AI-powered pipeline to standardize job titles from LinkedIn member data into structured classifications: **Department**, **Function**, and **Seniority**. The pipeline is designed to process millions of records efficiently while maintaining cost-effectiveness through intelligent caching and hybrid classification approaches.

## Project Structure

```
standardization_pipeline/
├── README.md                 # This file - project overview
├── RFC.md                    # Request for Comments document
├── docs/                     # Documentation
│   ├── architecture.md      # System architecture and design
│   ├── taxonomy.md          # Standardization taxonomy definitions
│   ├── database_setup.md    # Database setup instructions
│   └── experiments/         # Experiment documentation
│       ├── README.md        # Experiments overview
│       ├── rule_classifier.md
│       ├── spacy_classifier.md
│       ├── classifier_comparison.md
│       └── llama_classifier.md
├── src/                      # Source code
│   ├── classifiers/         # Classification implementations
│   │   ├── __init__.py
│   │   ├── rule_classifier.py
│   │   ├── spacy_classifier.py
│   │   └── llama_classifier.py
│   ├── validator.py         # Taxonomy validation
│   └── utils/               # Utility functions
├── tests/                    # Test files
│   ├── test_rule_classifier.py
│   ├── test_spacy_classifier.py
│   ├── test_llama_classifier.py
│   └── test_validator.py
├── experiments/             # Experimental scripts and analysis
│   ├── compare_classifiers.py
│   └── classify_seniority.py
├── migrations/              # Database migrations
├── scripts/                 # Setup and utility scripts
│   ├── setup_database.sh
│   └── setup_hf_auth.py
└── data/                    # Data files (if needed)
```

## Quick Start

### 1. Database Setup

```bash
# Set up PostgreSQL database with LinkedIn member data
./scripts/setup_database.sh
```

See [docs/database_setup.md](docs/database_setup.md) for detailed instructions.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Tests

```bash
# Test rule-based classifier
python -m pytest tests/test_rule_classifier.py

# Test validator
python -m pytest tests/test_validator.py
```

### 4. Run Experiments

```bash
# Compare different classifier approaches
python experiments/compare_classifiers.py
```

## Project Goals

1. **Standardize job titles** - Transform unstructured titles into structured classifications
2. **Enable querying** - Support queries like "find all senior sales positions"
3. **Auto-triggered processing** - Automatically process new profiles and changes
4. **Cost-effective** - Target <$0.001 per title after caching
5. **Extensible** - Support future standardization pipelines

## Architecture

The pipeline follows a hybrid approach combining:
- **Rule-based classification** - Fast pattern matching (~40% coverage)
- **LLM classification** - GPT-4 for ambiguous titles
- **Caching** - Redis (hot) + PostgreSQL (warm) for cost optimization
- **Validation** - Ensures taxonomy compliance

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Experiments & Thinking Process

This project involved extensive experimentation with different classification approaches:

1. **Rule-based Classifier** - Fast, deterministic pattern matching
2. **spaCy Classifier** - NLP-based approach using linguistic features
3. **Llama Classifier** - Local LLM for classification
4. **Comparison Analysis** - Performance, accuracy, and cost trade-offs

See [EXPERIMENTS.md](EXPERIMENTS.md) for a comprehensive overview of the thinking process and experiments, or [docs/experiments/README.md](docs/experiments/README.md) for detailed experiment documentation.

## Taxonomy

The standardization taxonomy includes:

- **13 Departments**: C-Suite, Engineering & Technical, Sales, Marketing, etc.
- **100+ Functions**: Software Development, Data Science, Sales, etc.
- **11 Seniority Levels**: Owner, Founder, C-suite, VP, Head, Director, Manager, Senior, Entry, Intern

See [docs/taxonomy.md](docs/taxonomy.md) for the complete taxonomy.

## Key Components

### Classifiers

- **RuleClassifier** (`src/classifiers/rule_classifier.py`) - Pattern-based classification
- **SpacyClassifier** (`src/classifiers/spacy_classifier.py`) - NLP-based classification
- **LlamaClassifier** (`src/classifiers/llama_classifier.py`) - Local LLM classification

### Validator

- **Validator** (`src/validator.py`) - Ensures taxonomy compliance and data quality

### Database

- PostgreSQL database with standardized fields
- Cache table for cost optimization
- Migration scripts in `migrations/`

## Documentation

- **[RFC.md](RFC.md)** - Request for Comments document with full specification
- **[docs/architecture.md](docs/architecture.md)** - System architecture details
- **[docs/taxonomy.md](docs/taxonomy.md)** - Complete taxonomy definitions
- **[docs/experiments/](docs/experiments/)** - Experiment documentation and findings

## Development Status

### ✅ Completed

- [x] Rule-based classifier implementation
- [x] spaCy classifier implementation
- [x] Llama classifier implementation
- [x] Validator component
- [x] Database schema design
- [x] Experiment comparison and analysis
- [x] Test suite

### 🚧 In Progress

- [ ] LLM classifier integration (GPT-4)
- [ ] Caching layer implementation
- [ ] Queue system (Redis)
- [ ] Change detection system
- [ ] Query API

### 📋 Planned

- [ ] Auto-trigger pipeline
- [ ] Monitoring and metrics
- [ ] Production deployment
- [ ] Performance optimization

## Cost Estimates

- **Initial processing** (1M titles): ~$600-900
- **Monthly** (10K new titles): ~$100-200
- **Per title** (after caching): <$0.001

## Performance Targets

- **Cache hit rate**: 90%+
- **Processing throughput**: 1000+ titles/hour
- **Classification accuracy**: 90%+
- **Cost per title**: <$0.001

## Contributing

This project is currently in RFC review. For questions or feedback, please refer to the [RFC.md](RFC.md) document.

## License

[Add license information]

## Contact

[Add contact information]
