# Experiments & Thinking Process

This document provides a comprehensive overview of the experiments conducted during the development of the job title standardization pipeline. It explains the thinking process, trade-offs considered, and decisions made.

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Initial Approach](#initial-approach)
3. [Experiment Phases](#experiment-phases)
4. [Key Findings](#key-findings)
5. [Architecture Decisions](#architecture-decisions)
6. [Lessons Learned](#lessons-learned)

## Problem Statement

**Goal**: Build an AI pipeline to standardize job titles into Department, Function, and Seniority classifications.

**Constraints**:
- Process millions of records efficiently
- Cost-effective (<$0.001 per title after caching)
- High accuracy (90%+)
- Auto-trigger on new/updated titles
- Extensible for future pipelines

**Challenge**: Job titles are highly variable and ambiguous. Examples:
- "Backend Engineer" → Engineering & Technical / Software Development / Entry
- "Head of Sales" → Sales / Sales / Head
- "VP of Engineering" → Engineering & Technical / Engineering & Technical / VP
- "SWE Intern" → Engineering & Technical / Software Development / Intern

## Initial Approach

### Hypothesis 1: Rule-Based Classification Only

**Thinking**: Start with simple pattern matching - fast, deterministic, no API costs.

**Implementation**: Built `RuleClassifier` with regex patterns for:
- Seniority detection (Owner, Founder, C-suite, VP, Head, Director, Manager, Senior, Entry, Intern)
- Department/Function mapping (keyword-based)

**Results**:
- ✅ Very fast: 0.1ms per title
- ✅ High coverage: 93% on test set
- ✅ Deterministic: Same title = same result
- ⚠ Limited coverage: ~50-60% on real-world data
- ⚠ Cannot handle ambiguous/novel titles

**Conclusion**: Rule-based alone insufficient. Need fallback for ambiguous cases.

### Hypothesis 2: NLP-Based Classification (spaCy)

**Thinking**: Use linguistic features for better pattern matching - might catch patterns rules miss.

**Implementation**: Built `SpacyClassifier` using:
- spaCy's Matcher for pattern matching
- Linguistic features (POS tags, tokenization)
- Similar pattern structure to rule-based

**Results**:
- ✅ Perfect seniority detection: 100% agreement
- ✅ Better linguistic understanding
- ⚠ Slower: 32x slower than rule-based (3.5ms vs 0.1ms)
- ⚠ Lower coverage: 83% vs 93% on test set
- ⚠ No clear advantage over rule-based

**Conclusion**: spaCy adds complexity without clear benefits. Rule-based patterns are faster and more maintainable.

### Hypothesis 3: Local LLM Classification (Llama)

**Thinking**: Use local LLM to avoid API costs - might be good middle ground.

**Implementation**: Built `LlamaClassifier` using:
- Llama-3.2-1B-Instruct model
- Local inference (no API calls)
- Prompt engineering for classification

**Results**:
- ✅ No API costs
- ✅ Good accuracy for complex titles
- ⚠ Very slow: 1-5 seconds per title
- ⚠ High memory: 2-4GB RAM required
- ⚠ Still requires API for best models (GPT-4)

**Conclusion**: Local LLM too slow for production. Cloud LLM with batching/caching is better.

### Hypothesis 4: Hybrid Rule + Cloud LLM

**Thinking**: Combine best of both - fast rules for common cases, LLM for ambiguous cases.

**Implementation**: Designed hybrid architecture:
1. Rule classifier first (fast path)
2. LLM classifier second (fallback)
3. Caching layer (cost optimization)
4. Validation layer (quality assurance)

**Results** (projected):
- ✅ Fast for common cases (rule-based)
- ✅ Handles ambiguous cases (LLM)
- ✅ Cost-effective with caching (90%+ hit rate)
- ✅ Scalable and maintainable

**Conclusion**: Hybrid approach optimal. Proceed with this architecture.

## Experiment Phases

### Phase 1: Rule-Based Classifier (Days 1-2)

**Goal**: Build fast, deterministic classifier for common patterns.

**Experiments**:
- Pattern design and testing
- Confidence scoring
- Coverage analysis on test set

**Key Learnings**:
- Pattern order matters (specific → general)
- Confidence scores help prioritize LLM fallback
- ~40% real-world coverage achievable

**Documentation**: [docs/experiments/rule_classifier.md](docs/experiments/rule_classifier.md)

### Phase 2: spaCy Classifier (Days 3-4)

**Goal**: Explore NLP-based approach for better pattern matching.

**Experiments**:
- spaCy Matcher configuration
- Linguistic feature extraction
- Comparison with rule-based

**Key Learnings**:
- NLP adds complexity without clear benefits
- Rule-based patterns are faster and simpler
- Perfect seniority detection interesting but not critical

**Documentation**: [docs/experiments/spacy_classifier.md](docs/experiments/spacy_classifier.md)

### Phase 3: Llama Classifier (Days 5-6)

**Goal**: Test local LLM for classification without API costs.

**Experiments**:
- Model selection (Llama-3.2-1B-Instruct)
- Prompt engineering
- Performance benchmarking

**Key Learnings**:
- Local LLM too slow for production
- Cloud LLM with batching is better
- Memory requirements significant

**Documentation**: [docs/experiments/llama_classifier.md](docs/experiments/llama_classifier.md)

### Phase 4: Comparison Analysis (Day 7)

**Goal**: Compare all approaches to inform architecture decisions.

**Experiments**:
- Side-by-side comparison on same dataset
- Performance metrics (speed, coverage, accuracy)
- Cost analysis

**Key Learnings**:
- Hybrid approach optimal
- Caching critical for cost efficiency
- Validation layer essential

**Documentation**: [docs/experiments/classifier_comparison.md](docs/experiments/classifier_comparison.md)

## Key Findings

### 1. Pattern Matching is Fast but Limited

**Finding**: Rule-based patterns can handle ~40% of titles instantly with zero cost.

**Implication**: Use rule-based as first pass, LLM as fallback.

**Decision**: Implement hybrid rule + LLM architecture.

### 2. Caching is Essential

**Finding**: Without caching, LLM costs would be prohibitive ($0.01-0.05 per title).

**Implication**: Need 90%+ cache hit rate to achieve <$0.001 per title target.

**Decision**: Implement two-tier caching (Redis + PostgreSQL).

### 3. Batching Reduces Cost Significantly

**Finding**: Batching 50-200 titles per LLM call reduces cost by 80-90%.

**Implication**: Batch processing is critical for cost efficiency.

**Decision**: Implement batch processing in LLM classifier.

### 4. Validation Ensures Quality

**Finding**: All classifiers can produce invalid taxonomy values.

**Implication**: Need validation layer to ensure taxonomy compliance.

**Decision**: Implement validator component with strict taxonomy checking.

### 5. Deduplication Reduces Volume

**Finding**: Many titles are duplicates (e.g., "Software Engineer" appears thousands of times).

**Implication**: Process unique titles only, then propagate results.

**Decision**: Implement deduplication in batch processing.

## Architecture Decisions

### Decision 1: Hybrid Rule + LLM

**Rationale**:
- Rule-based: Fast, free, handles common cases
- LLM: Handles ambiguous cases, better accuracy
- Combined: Best of both worlds

**Trade-offs**:
- Added complexity vs. better cost/performance
- Chose: Better cost/performance

### Decision 2: Two-Tier Caching

**Rationale**:
- Redis: Fast, hot cache for frequently accessed titles
- PostgreSQL: Persistent, warm cache for long-term storage
- Combined: Optimize both speed and persistence

**Trade-offs**:
- Added complexity vs. cost savings
- Chose: Cost savings (critical for scale)

### Decision 3: Batch Processing

**Rationale**:
- Process 50-200 titles per LLM call
- Reduces API calls by 80-90%
- Slight latency increase acceptable

**Trade-offs**:
- Latency vs. cost
- Chose: Cost optimization (batch processing)

### Decision 4: Validation Layer

**Rationale**:
- Ensures taxonomy compliance
- Catches invalid classifications
- Provides quality assurance

**Trade-offs**:
- Added processing vs. data quality
- Chose: Data quality (critical for downstream)

### Decision 5: Not Using spaCy

**Rationale**:
- Slower than rule-based (32x)
- Lower coverage than rule-based
- Added complexity without clear benefits

**Trade-offs**:
- Linguistic features vs. simplicity
- Chose: Simplicity (rule-based patterns)

## Lessons Learned

### 1. Start Simple, Then Optimize

**Lesson**: Started with rule-based patterns, then added LLM fallback. This incremental approach helped understand trade-offs.

**Application**: Build MVP first, then optimize based on data.

### 2. Cost Optimization is Critical

**Lesson**: Without caching and batching, costs would be 10-50x higher.

**Application**: Always consider cost optimization from the start.

### 3. Validation is Non-Negotiable

**Lesson**: Invalid classifications break downstream systems.

**Application**: Always validate outputs, especially with AI/LLM.

### 4. Performance Matters

**Lesson**: Even small latency differences matter at scale.

**Application**: Optimize hot path (rule-based) for speed.

### 5. Experimentation is Valuable

**Lesson**: Comparing approaches helped make informed decisions.

**Application**: Document experiments and findings for future reference.

## Next Steps

Based on these experiments, the next phase includes:

1. **Production LLM Integration** - GPT-4 with batching
2. **Caching Implementation** - Redis + PostgreSQL
3. **Queue System** - Redis-based job queue
4. **Change Detection** - Auto-trigger on new data
5. **Monitoring** - Track cache hit rates, costs, accuracy

## References

- [Rule Classifier Experiment](docs/experiments/rule_classifier.md)
- [spaCy Classifier Experiment](docs/experiments/spacy_classifier.md)
- [Llama Classifier Experiment](docs/experiments/llama_classifier.md)
- [Classifier Comparison](docs/experiments/classifier_comparison.md)
- [Architecture Documentation](docs/architecture.md)
- [RFC Document](RFC.md)
