-- ============================================
-- Job Title Standardization Pipeline Schema Migration - Data Model
-- Migration: 001_add_job_title_standardization_schema.sql
-- Description: Adds normalized taxonomy lookup tables and standardized fields
--              to member and member_experience tables.
--              This migration focuses on the core data model only.
--              See migration 005 for cache table.
--              See migration 004 for change detection features.
-- ============================================

BEGIN;

-- ============================================
-- 1. Create taxonomy lookup tables
-- ============================================
CREATE TABLE IF NOT EXISTS member_seniority_levels (
  id SMALLSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS member_departments (
  id SMALLSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS member_functions (
  id SMALLSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  department_id SMALLINT REFERENCES member_departments(id)
);

CREATE INDEX IF NOT EXISTS idx_member_functions_department_id ON member_functions(department_id);

-- ============================================
-- 2. Extend member table with standardized fields
-- ============================================
ALTER TABLE member 
ADD COLUMN IF NOT EXISTS department_id SMALLINT REFERENCES member_departments(id),
ADD COLUMN IF NOT EXISTS function_id SMALLINT REFERENCES member_functions(id),
ADD COLUMN IF NOT EXISTS seniority_id SMALLINT REFERENCES member_seniority_levels(id);

-- ============================================
-- 3. Extend member_experience table with standardized fields
-- ============================================
ALTER TABLE member_experience
ADD COLUMN IF NOT EXISTS department_id SMALLINT REFERENCES member_departments(id),
ADD COLUMN IF NOT EXISTS function_id SMALLINT REFERENCES member_functions(id),
ADD COLUMN IF NOT EXISTS seniority_id SMALLINT REFERENCES member_seniority_levels(id);

-- ============================================
-- 4. Create indexes for member table
-- ============================================
CREATE INDEX IF NOT EXISTS idx_member_dept_seniority 
  ON member(department_id, seniority_id) 
  WHERE department_id IS NOT NULL;

-- ============================================
-- 5. Create indexes for member_experience table
-- ============================================
CREATE INDEX IF NOT EXISTS idx_member_experience_dept_seniority 
  ON member_experience(department_id, seniority_id) 
  WHERE department_id IS NOT NULL;

-- ============================================
-- 6. Add comments
-- ============================================
COMMENT ON TABLE member_seniority_levels IS 'Lookup table for standardized seniority levels';
COMMENT ON TABLE member_departments IS 'Lookup table for standardized departments';
COMMENT ON TABLE member_functions IS 'Lookup table for standardized functions, linked to departments';

COMMENT ON COLUMN member.department_id IS 'Foreign key to member_departments table';
COMMENT ON COLUMN member.function_id IS 'Foreign key to member_functions table';
COMMENT ON COLUMN member.seniority_id IS 'Foreign key to member_seniority_levels table';

COMMENT ON COLUMN member_experience.department_id IS 'Foreign key to member_departments table';
COMMENT ON COLUMN member_experience.function_id IS 'Foreign key to member_functions table';
COMMENT ON COLUMN member_experience.seniority_id IS 'Foreign key to member_seniority_levels table';

COMMIT;
