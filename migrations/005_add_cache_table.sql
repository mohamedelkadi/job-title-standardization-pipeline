-- ============================================
-- Job Title Standardization Pipeline Schema Migration - Cache Table
-- Migration: 005_add_cache_table.sql
-- Description: Adds cache table for standardized job title classifications
--              Requires migration 001 to be applied first (data model)
--              This cache table optimizes cost by avoiding re-processing identical titles
-- ============================================

BEGIN;

-- ============================================
-- 1. Create job_title_standardization_cache table
-- ============================================
CREATE TABLE IF NOT EXISTS member_job_title_standardization_cache (
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

-- ============================================
-- 2. Create indexes for cache table
-- ============================================
CREATE INDEX IF NOT EXISTS idx_member_job_title_standardization_cache_normalized_title_hash 
  ON member_job_title_standardization_cache(normalized_title_hash);

-- ============================================
-- 3. Add comments
-- ============================================
COMMENT ON TABLE member_job_title_standardization_cache IS 'Cache for standardized job title classifications to avoid re-processing identical titles';
COMMENT ON COLUMN member_job_title_standardization_cache.normalized_title_hash IS 'SHA-256 hash of the normalized title (used for fast lookups)';
COMMENT ON COLUMN member_job_title_standardization_cache.normalized_title IS 'Normalized version of the job title (lowercase, trimmed, etc.)';
COMMENT ON COLUMN member_job_title_standardization_cache.classification_method IS 'Method used: rule_based, llm_gpt35, llm_gpt4, etc.';

COMMIT;
