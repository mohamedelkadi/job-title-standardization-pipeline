# RFC: Job Title Standardization Pipeline

**Version:** 1.0  
**Date:** 2024-03  
**Status:** Draft

---

## 1. Overview

Build an AI pipeline to standardize job titles into Department, Function, and Seniority using a hybrid rule-based + LLM approach.

**Goals:**
- Process millions of records efficiently
- Auto-trigger on new/updated titles
- Enable querying by standardized fields
- Cost-effective (<$0.001 per title after caching)
- Extensible for future pipelines

---

## 2. Architecture

```
CSV/DB → Change Detection → Queue → Normalizer → Cache → Rules → LLM → Validator → DB
                                                                                    ↓
                                                                              Query API
```

**Components:**
- **Change Detector**: Identifies new/updated titles
- **Queue**: Redis-based job queue (RQ/Celery)
- **Normalizer**: Normalizes titles for caching
- **Cache**: Redis (hot) + PostgreSQL (warm)
- **Rule Classifier**: Fast pattern matching (~40% coverage)
- **LLM Classifier**: GPT-4 for ambiguous titles
- **Validator**: Ensures taxonomy compliance
- **Query API**: REST API + SQL views

---

## 3. Database Schema

### Taxonomy Lookup Tables (Normalized)

```sql
-- Seniority Levels lookup table
CREATE TABLE member_seniority_levels (
  id SMALLSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);

-- Departments lookup table
CREATE TABLE member_departments (
  id SMALLSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
);

-- Functions lookup table (linked to departments)
CREATE TABLE member_functions (
  id SMALLSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  department_id SMALLINT REFERENCES member_departments(id)
);

CREATE INDEX idx_member_functions_department_id ON member_functions(department_id);
```

### Extend Existing Tables

```sql
-- Add standardized fields to member table (using foreign keys)
ALTER TABLE member 
ADD COLUMN department_id SMALLINT REFERENCES member_departments(id),
ADD COLUMN function_id SMALLINT REFERENCES member_functions(id),
ADD COLUMN seniority_id SMALLINT REFERENCES member_seniority_levels(id);

-- Add standardized fields to member_experience table (using foreign keys)
ALTER TABLE member_experience
ADD COLUMN department_id SMALLINT REFERENCES member_departments(id),
ADD COLUMN function_id SMALLINT REFERENCES member_functions(id),
ADD COLUMN seniority_id SMALLINT REFERENCES member_seniority_levels(id);

-- Indexes for query performance
CREATE INDEX idx_member_dept_seniority 
  ON member(department_id, seniority_id) 
  WHERE department_id IS NOT NULL;

CREATE INDEX idx_member_experience_dept_seniority 
  ON member_experience(department_id, seniority_id) 
  WHERE department_id IS NOT NULL;
```

### Cache Table

Cache table to avoid re-processing identical titles (required for cost optimization).

```sql
CREATE TABLE member_job_title_standardization_cache (
  id BIGSERIAL PRIMARY KEY,
  normalized_title_hash VARCHAR(64) NOT NULL UNIQUE,
  normalized_title VARCHAR(1024) NOT NULL,
  department_id SMALLINT NOT NULL REFERENCES member_departments(id),
  function_id SMALLINT NOT NULL REFERENCES member_functions(id),
  seniority_id SMALLINT NOT NULL REFERENCES member_seniority_levels(id),
  confidence DECIMAL(3,2) NOT NULL,
  classification_method VARCHAR(20) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_member_job_title_standardization_cache_normalized_title_hash ON member_job_title_standardization_cache(normalized_title_hash);
```

---

## 4. Processing Flow

### Single Title Classification

1. **Normalize**: Clean title, generate hash
2. **Check Cache**: Redis → PostgreSQL cache table → Rules
3. **Rule Classify**: Pattern matching (if cache miss)
4. **LLM Classify**: Batch API call (if rule confidence < 0.7)
5. **Validate**: Ensure taxonomy compliance
6. **Save**: Cache + Update member/member_experience tables

### Batch Processing

1. **Deduplicate**: Find unique titles
2. **Classify Unique**: Process each unique title once
3. **Propagate**: Update all records with same title

---

## 5. Cost Optimization

**Strategy:**
- **Caching**: 90%+ hit rate target (Redis + DB + Rules)
- **Batching**: 50-200 titles per LLM call (80-90% cost reduction)
- **Deduplication**: Process unique titles only (90% reduction)
- **Model Selection**: GPT-3.5 for common, GPT-4 for ambiguous

**Cost Estimate:**
- Initial (1M titles): ~$600-900
- Monthly (10K new titles): ~$100-200
- Per title (after caching): <$0.001

---

## 6. Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| Database | PostgreSQL 15+ |
| Cache | Redis 7+ |
| Queue | RQ or Celery |
| API | FastAPI |
| LLM | OpenAI GPT-4 Turbo |

---

## 7. API Design

### Query People

```
GET /api/v1/people?department=Sales&seniority=Senior&limit=100
```

**Response:**
```json
{
  "count": 150,
  "results": [
    {
      "id": 12345,
      "name": "John Doe",
      "current_title": "Senior Sales Manager",
      "department": "Sales",
      "function": "Sales",
      "seniority": "Senior",
      "confidence": 0.92
    }
  ]
}
```

### Standardize Title

```
POST /api/v1/standardize
{
  "title": "Backend Engineer"
}
```

---

## 8. Error Handling

**Retry Strategy:**
- Transient failures: 3 retries with exponential backoff
- Validation failures: Automatic repair attempt
- Persistent failures: Dead letter queue

**Idempotency:**
- Use (source_type, source_id) as key
- Prevents duplicate processing

---

## 9. Monitoring

**Key Metrics:**
- Cache hit rate
- LLM API calls and cost
- Processing throughput (titles/hour)
- Error rate by type
- Queue depth

**Tools:**
- Prometheus for metrics
- Grafana for dashboards
- Structured logging (JSON)

---

## 10. Deployment

**Development:**
- Docker Compose (PostgreSQL + Redis + API + Worker)

**Production:**
- Kubernetes (API: 2-3 replicas, Workers: 5-10 replicas)
- Managed PostgreSQL (RDS/Cloud SQL)
- Managed Redis (ElastiCache/Memorystore)

---

## 11. Timeline

| Phase | Days | Tasks |
|-------|------|-------|
| Foundation | 1-2 | Schema, Normalizer, Rules, Cache |
| LLM Integration | 3-4 | LLM Classifier, Validator, Repair |
| Batch Processing | 5 | Deduplication, Batch Processor |
| Auto-Trigger | 6 | Change Detection, Queue, Triggers |
| Query Interface | 7 | REST API, SQL Views |
| Monitoring | 8-9 | Metrics, Dashboard, Docs |

**Total: 9 days**

---

## 12. Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| LLM API rate limits | Rate limiting, multiple keys, batching |
| Invalid responses | Validation layer, repair mechanism |
| Cost overrun | Cost monitoring, alerts, budget limits |
| Low accuracy | Confidence thresholds, manual review |

---

## 13. Open Questions

1. **Data Source**: Live DB or CSV-only? (Affects auto-trigger design)
2. **Scope**: Process all `member_experience` or only current? (Affects cost)
3. **Budget**: What's the limit for initial/ongoing costs?
4. **Accuracy**: What's the acceptable threshold? (Target: 90%+)

---

## 14. Success Criteria

- ✅ Process 1M+ titles efficiently
- ✅ 90%+ cache hit rate
- ✅ <$0.001 per title cost
- ✅ Auto-trigger on new data
- ✅ Query interface functional
- ✅ 90%+ classification accuracy

---

**Next Steps:**
1. Review and align on open questions
2. Approve architecture
3. Begin implementation (Stage 2)

