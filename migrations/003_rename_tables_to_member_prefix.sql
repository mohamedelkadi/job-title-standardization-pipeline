-- ============================================
-- Rename Tables to Match member_ Naming Convention
-- Migration: 003_rename_tables_to_member_prefix.sql
-- Description: Renames taxonomy tables to use member_ prefix
-- ============================================

BEGIN;

-- Drop existing foreign key constraints first
ALTER TABLE member DROP CONSTRAINT IF EXISTS member_department_id_fkey;
ALTER TABLE member DROP CONSTRAINT IF EXISTS member_function_id_fkey;
ALTER TABLE member DROP CONSTRAINT IF EXISTS member_seniority_id_fkey;

ALTER TABLE member_experience DROP CONSTRAINT IF EXISTS member_experience_department_id_fkey;
ALTER TABLE member_experience DROP CONSTRAINT IF EXISTS member_experience_function_id_fkey;
ALTER TABLE member_experience DROP CONSTRAINT IF EXISTS member_experience_seniority_id_fkey;

ALTER TABLE job_title_standardization_cache DROP CONSTRAINT IF EXISTS job_title_standardization_cache_department_id_fkey;
ALTER TABLE job_title_standardization_cache DROP CONSTRAINT IF EXISTS job_title_standardization_cache_function_id_fkey;
ALTER TABLE job_title_standardization_cache DROP CONSTRAINT IF EXISTS job_title_standardization_cache_seniority_id_fkey;

ALTER TABLE functions DROP CONSTRAINT IF EXISTS functions_department_id_fkey;

-- Rename tables
ALTER TABLE seniority_levels RENAME TO member_seniority_levels;
ALTER TABLE departments RENAME TO member_departments;
ALTER TABLE functions RENAME TO member_functions;
ALTER TABLE job_title_standardization_cache RENAME TO member_job_title_standardization_cache;

-- Recreate foreign key constraints with new table names
ALTER TABLE member_functions 
ADD CONSTRAINT member_functions_department_id_fkey 
FOREIGN KEY (department_id) REFERENCES member_departments(id);

ALTER TABLE member 
ADD CONSTRAINT member_department_id_fkey 
FOREIGN KEY (department_id) REFERENCES member_departments(id);

ALTER TABLE member 
ADD CONSTRAINT member_function_id_fkey 
FOREIGN KEY (function_id) REFERENCES member_functions(id);

ALTER TABLE member 
ADD CONSTRAINT member_seniority_id_fkey 
FOREIGN KEY (seniority_id) REFERENCES member_seniority_levels(id);

ALTER TABLE member_experience 
ADD CONSTRAINT member_experience_department_id_fkey 
FOREIGN KEY (department_id) REFERENCES member_departments(id);

ALTER TABLE member_experience 
ADD CONSTRAINT member_experience_function_id_fkey 
FOREIGN KEY (function_id) REFERENCES member_functions(id);

ALTER TABLE member_experience 
ADD CONSTRAINT member_experience_seniority_id_fkey 
FOREIGN KEY (seniority_id) REFERENCES member_seniority_levels(id);

ALTER TABLE member_job_title_standardization_cache 
ADD CONSTRAINT member_job_title_standardization_cache_department_id_fkey 
FOREIGN KEY (department_id) REFERENCES member_departments(id);

ALTER TABLE member_job_title_standardization_cache 
ADD CONSTRAINT member_job_title_standardization_cache_function_id_fkey 
FOREIGN KEY (function_id) REFERENCES member_functions(id);

ALTER TABLE member_job_title_standardization_cache 
ADD CONSTRAINT member_job_title_standardization_cache_seniority_id_fkey 
FOREIGN KEY (seniority_id) REFERENCES member_seniority_levels(id);

-- Rename indexes
ALTER INDEX IF EXISTS idx_functions_department_id RENAME TO idx_member_functions_department_id;
ALTER INDEX IF EXISTS idx_cache_normalized_title_hash RENAME TO idx_member_job_title_standardization_cache_normalized_title_hash;

COMMIT;

