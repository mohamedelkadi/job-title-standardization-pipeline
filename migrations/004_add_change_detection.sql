-- ============================================
-- Job Title Standardization Pipeline Schema Migration - Change Detection
-- Migration: 004_add_change_detection.sql
-- Description: Adds automatic change detection for job titles using dirty-flag polling
--              Requires migration 001 to be applied first (data model)
--              Cache table (migration 005) is optional but recommended
-- ============================================

BEGIN;

-- ============================================
-- 1. Add change detection fields to member table
-- ============================================
ALTER TABLE member 
ADD COLUMN IF NOT EXISTS title_hash VARCHAR(64),
ADD COLUMN IF NOT EXISTS needs_standardization BOOLEAN NOT NULL DEFAULT FALSE;

-- ============================================
-- 2. Add change detection fields to member_experience table
-- ============================================
ALTER TABLE member_experience
ADD COLUMN IF NOT EXISTS title_hash VARCHAR(64),
ADD COLUMN IF NOT EXISTS needs_standardization BOOLEAN NOT NULL DEFAULT FALSE;

-- ============================================
-- 3. Create indexes for dirty-flag polling
-- ============================================
CREATE INDEX IF NOT EXISTS idx_member_needs_standardization 
  ON member(needs_standardization, id) 
  WHERE needs_standardization = TRUE;

CREATE INDEX IF NOT EXISTS idx_member_experience_needs_standardization 
  ON member_experience(needs_standardization, id) 
  WHERE needs_standardization = TRUE;

CREATE INDEX IF NOT EXISTS idx_member_title_hash ON member(title_hash);
CREATE INDEX IF NOT EXISTS idx_member_experience_title_hash ON member_experience(title_hash);

-- ============================================
-- 4. Create helper function to normalize and hash job titles
-- ============================================
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

-- ============================================
-- 5. Create trigger function to handle title changes
-- ============================================
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

-- ============================================
-- 6. Create triggers for automatic change detection
-- ============================================
DROP TRIGGER IF EXISTS trigger_member_title_change ON member;
CREATE TRIGGER trigger_member_title_change
  BEFORE INSERT OR UPDATE OF title ON member
  FOR EACH ROW
  EXECUTE FUNCTION check_title_change();

DROP TRIGGER IF EXISTS trigger_member_experience_title_change ON member_experience;
CREATE TRIGGER trigger_member_experience_title_change
  BEFORE INSERT OR UPDATE OF title ON member_experience
  FOR EACH ROW
  EXECUTE FUNCTION check_title_change();

-- ============================================
-- 7. Add comments
-- ============================================
COMMENT ON COLUMN member.title_hash IS 'SHA-256 hash of normalized job title (computed automatically on insert/update)';
COMMENT ON COLUMN member.needs_standardization IS 'Dirty flag: set to TRUE when title_hash changes, cleared after successful standardization';

COMMENT ON COLUMN member_experience.title_hash IS 'SHA-256 hash of normalized job title (computed automatically on insert/update)';
COMMENT ON COLUMN member_experience.needs_standardization IS 'Dirty flag: set to TRUE when title_hash changes, cleared after successful standardization';

COMMENT ON FUNCTION normalize_and_hash_title IS 'Normalizes a job title (lowercase, trim, collapse spaces) and returns SHA-256 hash';
COMMENT ON FUNCTION check_title_change IS 'Trigger function that computes title_hash and sets needs_standardization flag when title changes';

COMMIT;
