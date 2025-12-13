# Experiments Overview

This directory contains documentation of all experiments conducted during the development of the job title standardization pipeline. These experiments were crucial in understanding the trade-offs between different classification approaches and informing the final architecture decisions.

## Experiment Timeline

### Phase 1: Rule-Based Classification
**Goal**: Build a fast, deterministic classifier using pattern matching

**Findings**:
- ✅ Very fast (0.1ms per title)
- ✅ High coverage (93% on test set)
- ✅ Deterministic results
- ⚠ Limited to known patterns (~50-60% real-world coverage)

**Documentation**: [rule_classifier.md](rule_classifier.md)

### Phase 2: NLP-Based Classification (spaCy)
**Goal**: Explore linguistic features for better pattern matching

**Findings**:
- ✅ Perfect seniority detection (100% agreement)
- ✅ Better handling of complex linguistic structures
- ⚠ Slower (32x slower than rule-based)
- ⚠ Lower coverage (83% vs 93%)

**Documentation**: [spacy_classifier.md](spacy_classifier.md)

### Phase 3: Local LLM Classification (Llama)
**Goal**: Test local LLM for classification without API costs

**Findings**:
- ✅ No API costs
- ✅ Good accuracy for complex titles
- ⚠ Slow inference (1-5 seconds per title)
- ⚠ High memory requirements (2-4GB RAM)

**Documentation**: [llama_classifier.md](llama_classifier.md)

### Phase 4: Comparison Analysis
**Goal**: Compare all approaches to inform architecture decisions

**Key Insights**:
1. **Hybrid approach is optimal**: Use rule-based for speed, LLM for ambiguous cases
2. **Caching is critical**: 90%+ cache hit rate needed for cost efficiency
3. **Validation layer essential**: Ensures taxonomy compliance across all methods

**Documentation**: [classifier_comparison.md](classifier_comparison.md)

## Decision Rationale

### Why Hybrid Rule + LLM?

Based on the experiments, we chose a hybrid approach:

1. **Rule Classifier First** (Fast path)
   - Handles ~40% of titles instantly
   - Zero cost, deterministic
   - High confidence for known patterns

2. **LLM Classifier Second** (Fallback)
   - Handles ambiguous/novel titles
   - Higher cost but necessary for coverage
   - Batching reduces cost by 80-90%

3. **Caching Layer** (Cost optimization)
   - Redis for hot cache (frequently accessed)
   - PostgreSQL for warm cache (persistent)
   - Target 90%+ cache hit rate

### Why Not spaCy?

While spaCy showed promise, it was:
- Slower than rule-based (32x)
- Lower coverage than rule-based
- Added complexity without clear benefits

**Decision**: Use rule-based patterns instead, which are faster and more maintainable.

### Why Not Local LLM Only?

Llama showed good accuracy but:
- Too slow for production (1-5s per title)
- High memory requirements
- Still requires API for best models (GPT-4)

**Decision**: Use cloud LLM (GPT-4) with batching and caching for cost efficiency.

## Experiment Results Summary

| Approach | Speed | Coverage | Cost | Accuracy |
|----------|-------|----------|------|----------|
| Rule-based | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| spaCy | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Llama (local) | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GPT-4 (cloud) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

## Key Learnings

1. **Pattern matching is fast but limited** - Need LLM for coverage
2. **Caching is essential** - Without it, costs would be prohibitive
3. **Validation is critical** - Ensures quality across all methods
4. **Batching matters** - 50-200 titles per LLM call reduces cost by 80-90%
5. **Hybrid approach balances speed, cost, and accuracy**

## Next Steps

Based on these experiments, the next phase includes:

1. **Production LLM Integration** - GPT-4 with batching
2. **Caching Implementation** - Redis + PostgreSQL
3. **Queue System** - Redis-based job queue
4. **Change Detection** - Auto-trigger on new data
5. **Monitoring** - Track cache hit rates, costs, accuracy

## Files

- `rule_classifier.md` - Rule-based classifier experiment details
- `spacy_classifier.md` - spaCy classifier experiment details
- `llama_classifier.md` - Llama classifier experiment details
- `classifier_comparison.md` - Comprehensive comparison analysis
