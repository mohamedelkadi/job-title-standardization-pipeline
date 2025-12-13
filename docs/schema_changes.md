# Database Schema Changes for Job Title Standardization Pipeline

## Overview

This document describes the database schema changes required to support the AI-powered job title standardization pipeline. The pipeline enriches job titles with standardized **Department**, **Function**, and **Seniority** classifications.

**Design:** Normalized schema with lookup tables and foreign keys for data integrity and easier taxonomy management.

**Migration Structure:** Schema changes are split into three migrations:
- **Migration 001**: Data model (taxonomy tables, standardized fields)
- **Migration 005**: Cache table (optimization for cost reduction)
- **Migration 004**: Change detection (dirty-flag polling, triggers, functions)

---

# Part I: Data Model (Migration 001)

## Overview

The data model provides the foundation for storing standardized job title classifications. It includes taxonomy lookup tables and standardized fields on member tables.

## Schema Changes Summary

1. **Create taxonomy lookup tables** - Normalized tables for departments, functions, and seniority levels
2. **Extend `member` table** - Add standardized fields using foreign keys
3. **Extend `member_experience` table** - Add standardized fields using foreign keys
4. **Add indexes** - Optimize query performance

---

## 1. Create Taxonomy Lookup Tables

Create normalized lookup tables for departments, functions, and seniority levels.

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

---

## 2. Extend `member` Table

Add standardized classification fields using foreign keys to taxonomy lookup tables.

```sql
ALTER TABLE member 
ADD COLUMN department_id SMALLINT REFERENCES member_departments(id),
ADD COLUMN function_id SMALLINT REFERENCES member_functions(id),
ADD COLUMN seniority_id SMALLINT REFERENCES member_seniority_levels(id);
```

### Field Descriptions

| Column | Type | Description |
|--------|------|-------------|
| `department_id` | SMALLINT | Foreign key to member_departments table |
| `function_id` | SMALLINT | Foreign key to member_functions table |
| `seniority_id` | SMALLINT | Foreign key to member_seniority_levels table |

---

## 3. Extend `member_experience` Table

Add standardized classification fields using foreign keys to taxonomy lookup tables.

```sql
ALTER TABLE member_experience
ADD COLUMN department_id SMALLINT REFERENCES member_departments(id),
ADD COLUMN function_id SMALLINT REFERENCES member_functions(id),
ADD COLUMN seniority_id SMALLINT REFERENCES member_seniority_levels(id);
```

### Field Descriptions

Same structure as `member` table (see above).

---

## 4. Performance Indexes

```sql
-- Indexes for member table
CREATE INDEX idx_member_dept_seniority 
  ON member(department_id, seniority_id) 
  WHERE department_id IS NOT NULL;

-- Indexes for member_experience table
CREATE INDEX idx_member_experience_dept_seniority 
  ON member_experience(department_id, seniority_id) 
  WHERE department_id IS NOT NULL;
```

---

## 5. Example Queries

### Query with Joins

```sql
-- Find all senior engineers
SELECT m.id, m.name, m.title, 
       d.name as department, 
       f.name as function, 
       s.name as seniority
FROM member m
JOIN member_departments d ON m.department_id = d.id
JOIN member_functions f ON m.function_id = f.id
JOIN member_seniority_levels s ON m.seniority_id = s.id
WHERE d.name = 'Engineering & Technical'
  AND s.name = 'Senior';
```

### Find All People in Senior Sales Positions

```sql
SELECT m.id, m.name, m.title, 
       d.name as department, 
       f.name as function, 
       s.name as seniority
FROM member m
JOIN member_departments d ON m.department_id = d.id
JOIN member_functions f ON m.function_id = f.id
JOIN member_seniority_levels s ON m.seniority_id = s.id
WHERE d.name = 'Sales'
  AND s.name = 'Senior';
```

---

## 6. Complete Data Model Migration Script

See `migrations/001_add_job_title_standardization_schema.sql` for the complete migration script.

---

# Part II: Cache Table (Migration 005)

## Overview

The cache table stores standardized classifications for normalized job titles, enabling cost optimization by avoiding re-processing identical titles.

**Requires:** Migration 001 (data model) must be applied first.

## Schema Changes Summary

1. **Create cache table** - Store standardized classifications keyed by normalized title hash
2. **Add indexes** - Optimize cache lookups

---

## 1. Create Cache Table

Cache table to store standardized classifications for normalized job titles. Essential for cost optimization.

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
```

### Field Descriptions

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Primary key |
| `normalized_title_hash` | VARCHAR(64) | SHA-256 hash of normalized title (unique) |
| `normalized_title` | VARCHAR(1024) | Normalized job title |
| `department_id` | SMALLINT | Foreign key to member_departments table |
| `function_id` | SMALLINT | Foreign key to member_functions table |
| `seniority_id` | SMALLINT | Foreign key to member_seniority_levels table |
| `confidence` | DECIMAL(3,2) | Classification confidence |
| `classification_method` | VARCHAR(20) | Method: `rule_based`, `llm_gpt35`, `llm_gpt4` |
| `created_at` | TIMESTAMP | Creation timestamp |

---

## 2. Create Indexes

```sql
CREATE INDEX idx_member_job_title_standardization_cache_normalized_title_hash 
  ON member_job_title_standardization_cache(normalized_title_hash);
```

---

## 3. Cache Usage Pattern

The cache table is used to avoid re-processing identical job titles:

1. **Before Processing**: Check if `normalized_title_hash` exists in cache
2. **Cache Hit**: Use cached classification (no AI API call needed)
3. **Cache Miss**: Process title with AI, then store result in cache

### Example Cache Lookup

```sql
-- Check cache before processing
SELECT department_id, function_id, seniority_id, confidence, classification_method
FROM member_job_title_standardization_cache
WHERE normalized_title_hash = 'abc123...';

-- Store new classification in cache
INSERT INTO member_job_title_standardization_cache 
  (normalized_title_hash, normalized_title, department_id, function_id, seniority_id, confidence, classification_method)
VALUES 
  ('abc123...', 'software engineer', 2, 15, 8, 0.95, 'llm_gpt4');
```

---

## 4. Complete Cache Table Migration Script

See `migrations/005_add_cache_table.sql` for the complete migration script.

---

# Part III: Change Detection (Migration 004)

## Overview

Change detection enables automatic processing of job titles when they are created or updated. It uses a **dirty-flag polling approach** that is reliable, simple to operate, and easy to evolve.

**Requires:** Migration 001 (data model) must be applied first.  
**Optional:** Migration 005 (cache table) is recommended but not required.

## Schema Changes Summary

1. **Add change detection fields** - `title_hash` and `needs_standardization` to member tables
2. **Create indexes** - Optimize dirty-flag polling queries
3. **Create helper functions** - Normalize and hash job titles
4. **Create triggers** - Automatically detect title changes and set dirty flags

---

## 1. Add Change Detection Fields

Add fields to track title changes and mark records needing standardization.

```sql
-- Add to member table
ALTER TABLE member 
ADD COLUMN title_hash VARCHAR(64),
ADD COLUMN needs_standardization BOOLEAN NOT NULL DEFAULT FALSE;

-- Add to member_experience table
ALTER TABLE member_experience
ADD COLUMN title_hash VARCHAR(64),
ADD COLUMN needs_standardization BOOLEAN NOT NULL DEFAULT FALSE;
```

### Field Descriptions

| Column | Type | Description |
|--------|------|-------------|
| `title_hash` | VARCHAR(64) | SHA-256 hash of normalized job title (computed automatically) |
| `needs_standardization` | BOOLEAN | Dirty flag: TRUE when title_hash changes, cleared after standardization |

---

## 2. Create Indexes for Dirty-Flag Polling

Indexes optimize queries that poll for records needing standardization.

```sql
-- Partial indexes for efficient batch processing
CREATE INDEX idx_member_needs_standardization 
  ON member(needs_standardization, id) 
  WHERE needs_standardization = TRUE;

CREATE INDEX idx_member_experience_needs_standardization 
  ON member_experience(needs_standardization, id) 
  WHERE needs_standardization = TRUE;

-- Indexes for title_hash lookups
CREATE INDEX idx_member_title_hash ON member(title_hash);
CREATE INDEX idx_member_experience_title_hash ON member_experience(title_hash);
```

---

## 3. Create Helper Functions

### Normalize and Hash Function

```sql
CREATE OR REPLACE FUNCTION normalize_and_hash_title(title_text TEXT)
RETURNS VARCHAR(64) AS $$
DECLARE
  normalized TEXT;
BEGIN
  -- Normalize: lowercase, trim whitespace, collapse multiple spaces
  normalized := LOWER(TRIM(REGEXP_REPLACE(COALESCE(title_text, ''), '\s+', ' ', 'g')));
  
  -- Return SHA-256 hash (64 hex characters)
  RETURN ENCODE(DIGEST(normalized, 'sha256'), 'hex');
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

### Trigger Function

```sql
CREATE OR REPLACE FUNCTION check_title_change()
RETURNS TRIGGER AS $$
DECLARE
  new_hash VARCHAR(64);
BEGIN
  -- Compute hash of normalized title
  new_hash := normalize_and_hash_title(NEW.title);
  
  -- If hash changed, mark as needing standardization
  IF NEW.title_hash IS DISTINCT FROM new_hash THEN
    NEW.title_hash := new_hash;
    NEW.needs_standardization := TRUE;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## 4. Create Triggers

Triggers automatically detect title changes and set the dirty flag.

```sql
-- Trigger for member table
CREATE TRIGGER trigger_member_title_change
  BEFORE INSERT OR UPDATE OF title ON member
  FOR EACH ROW
  EXECUTE FUNCTION check_title_change();

-- Trigger for member_experience table
CREATE TRIGGER trigger_member_experience_title_change
  BEFORE INSERT OR UPDATE OF title ON member_experience
  FOR EACH ROW
  EXECUTE FUNCTION check_title_change();
```

---

## 5. How Change Detection Works

### Dirty-Flag Polling Flow

1. **Title Change**: When a job title is inserted or updated, the trigger fires
2. **Hash Computation**: The trigger normalizes the title and computes `title_hash`
3. **Flag Setting**: If the hash changed, `needs_standardization = TRUE` is set
4. **Background Worker**: A worker polls records where `needs_standardization = TRUE` in batches
5. **Processing**: Worker standardizes the job title and updates classification fields
6. **Flag Clearing**: After successful standardization, `needs_standardization = FALSE`

### Benefits

- **Reliable**: Database-level triggers ensure no changes are missed
- **Simple**: No complex event infrastructure required
- **Efficient**: Only meaningful title changes trigger processing (cosmetic edits ignored)
- **Self-healing**: Periodic reconciliation can backfill any missed records

### Polling Query Example

```sql
-- Get next batch of records needing standardization (member table)
SELECT id, title, title_hash
FROM member
WHERE needs_standardization = TRUE
ORDER BY id
LIMIT 100;

-- After successful standardization, clear the flag
UPDATE member
SET needs_standardization = FALSE
WHERE id IN (...);
```

---

## 6. Change Detection Strategy

### Default: Dirty-Flag Polling

- On insert/update of a job title:
  - Normalize the title and compute a `title_hash`
  - If the hash changed, mark the record as `needs_standardization = true`
- A background worker (Candidate Selector) polls flagged records in small batches
- After successful standardization, the flag is cleared

Normalization and hashing ensure that only **meaningful title changes** trigger the pipeline, avoiding reprocessing on cosmetic edits.

### Preferred (If Available): Event-Driven Triggering

If the platform already emits reliable events for job title changes, the pipeline can hook into those events instead. Even in this mode, a lightweight reconciliation job runs periodically to backfill any missed records.

---

## 7. Complete Change Detection Migration Script

See `migrations/004_add_change_detection.sql` for the complete migration script.

---

# General Information

## Migration Dependencies

```
001 (Data Model)
  ├── 005 (Cache Table) - Optional but recommended
  └── 004 (Change Detection) - Optional
```

**Note:** Migrations 002 and 003 exist for seeding taxonomy data and renaming tables, but are not part of the core schema changes documented here.

---

## Benefits of Normalized Design

1. **Data Integrity** - Foreign keys prevent invalid taxonomy values
2. **Easy Updates** - Update taxonomy in one place (lookup tables)
3. **Storage Efficiency** - IDs are smaller than VARCHAR strings
4. **Consistency** - Prevents typos and data inconsistencies
5. **Query Performance** - Indexes on foreign keys are efficient

---

## Taxonomy Values

See PROJECT_DESCRIPTION.md for the complete taxonomy:
- **Seniority Levels**: Owner, Founder, C-suite, Partner, VP, Head, Director, Manager, Senior, Entry, Intern
- **Departments**: 13 departments (C-Suite, Engineering & Technical, Sales, etc.)
- **Functions**: ~150+ functions linked to departments

---

**Document Version:** 4.0  
**Last Updated:** 2024-12-12  
**Status:** Ready for Implementation
