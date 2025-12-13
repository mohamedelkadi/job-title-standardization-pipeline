-- ============================================
-- Seed Taxonomy Data for Job Title Standardization
-- Migration: 002_seed_taxonomy_data.sql
-- Description: Populates seniority_levels, departments, and functions tables
--              with the complete taxonomy
-- ============================================

BEGIN;

-- ============================================
-- 1. Insert Seniority Levels
-- ============================================
INSERT INTO member_seniority_levels (name) VALUES
('Owner'),
('Founder'),
('C-suite'),
('Partner'),
('VP'),
('Head'),
('Director'),
('Manager'),
('Senior'),
('Entry'),
('Intern')
ON CONFLICT (name) DO NOTHING;

-- ============================================
-- 2. Insert Departments
-- ============================================
INSERT INTO member_departments (name) VALUES
('C-Suite'),
('Engineering & Technical'),
('Design'),
('Education'),
('Finance'),
('Human Resources'),
('Information Technology'),
('Legal'),
('Marketing'),
('Medical & Health'),
('Operations'),
('Sales'),
('Consulting')
ON CONFLICT (name) DO NOTHING;

-- ============================================
-- 3. Insert Functions (linked to Departments)
-- ============================================

-- C-Suite functions
INSERT INTO member_functions (name, department_id) VALUES
('Executive', (SELECT id FROM member_departments WHERE name = 'C-Suite')),
('Finance Executive', (SELECT id FROM member_departments WHERE name = 'C-Suite')),
('Founder', (SELECT id FROM member_departments WHERE name = 'C-Suite')),
('Human Resources Executive', (SELECT id FROM member_departments WHERE name = 'C-Suite')),
('Information Technology Executive', (SELECT id FROM member_departments WHERE name = 'C-Suite')),
('Legal Executive', (SELECT id FROM member_departments WHERE name = 'C-Suite')),
('Marketing Executive', (SELECT id FROM member_departments WHERE name = 'C-Suite')),
('Medical & Health Executive', (SELECT id FROM member_departments WHERE name = 'C-Suite')),
('Operations Executive', (SELECT id FROM member_departments WHERE name = 'C-Suite')),
('Sales Leader', (SELECT id FROM member_departments WHERE name = 'C-Suite'))
ON CONFLICT (name) DO NOTHING;

-- Engineering & Technical functions
INSERT INTO member_functions (name, department_id) VALUES
('Artificial Intelligence / Machine Learning', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Bioengineering', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Biometrics', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Business Intelligence', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Chemical Engineering', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Cloud / Mobility', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Data Science', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('DevOps', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Digital Transformation', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Emerging Technology / Innovation', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Engineering & Technical', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Industrial Engineering', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Mechanic', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Mobile Development', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Product Development', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Product Management', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Project Management', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Research & Development', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Scrum Master / Agile Coach', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Software Development', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Support / Technical Services', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Technician', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Technology Operations', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Test / Quality Assurance', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('UI / UX', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical')),
('Web Development', (SELECT id FROM member_departments WHERE name = 'Engineering & Technical'))
ON CONFLICT (name) DO NOTHING;

-- Design functions
INSERT INTO functions (name, department_id) VALUES
('All Design', (SELECT id FROM member_departments WHERE name = 'Design')),
('Product or UI/UX Design', (SELECT id FROM member_departments WHERE name = 'Design')),
('Graphic / Visual / Brand Design', (SELECT id FROM member_departments WHERE name = 'Design'))
ON CONFLICT (name) DO NOTHING;

-- Education functions
INSERT INTO functions (name, department_id) VALUES
('Teacher', (SELECT id FROM member_departments WHERE name = 'Education')),
('Principal', (SELECT id FROM member_departments WHERE name = 'Education')),
('Superintendent', (SELECT id FROM member_departments WHERE name = 'Education')),
('Professor', (SELECT id FROM member_departments WHERE name = 'Education'))
ON CONFLICT (name) DO NOTHING;

-- Finance functions
INSERT INTO functions (name, department_id) VALUES
('Accounting', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Finance', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Financial Planning & Analysis', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Financial Reporting', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Financial Strategy', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Financial Systems', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Internal Audit & Control', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Investor Relations', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Mergers & Acquisitions', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Real Estate Finance', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Financial Risk', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Shared Services', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Sourcing / Procurement', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Tax', (SELECT id FROM member_departments WHERE name = 'Finance')),
('Treasury', (SELECT id FROM member_departments WHERE name = 'Finance'))
ON CONFLICT (name) DO NOTHING;

-- Human Resources functions
INSERT INTO functions (name, department_id) VALUES
('Compensation & Benefits', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('Culture, Diversity & Inclusion', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('Employee & Labor Relations', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('Health & Safety', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('Human Resource Information System', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('Human Resources', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('HR Business Partner', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('Learning & Development', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('Organizational Development', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('Recruiting & Talent Acquisition', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('Talent Management', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('Workforce Management', (SELECT id FROM member_departments WHERE name = 'Human Resources')),
('People Operations', (SELECT id FROM member_departments WHERE name = 'Human Resources'))
ON CONFLICT (name) DO NOTHING;

-- Information Technology functions
INSERT INTO functions (name, department_id) VALUES
('Application Development', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Business Service Management / ITSM', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Collaboration & Web App', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Data Center', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Data Warehouse', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Database Administration', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('eCommerce Development', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Enterprise Architecture', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Help Desk / Desktop Services', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('HR / Financial / ERP Systems', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Information Security', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Information Technology', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Infrastructure', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('IT Asset Management', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('IT Audit / IT Compliance', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('IT Operations', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('IT Procurement', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('IT Strategy', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('IT Training', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Networking', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Project & Program Management', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Quality Assurance', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Retail / Store Systems', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Servers', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Storage & Disaster Recovery', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Telecommunications', (SELECT id FROM member_departments WHERE name = 'Information Technology')),
('Virtualization', (SELECT id FROM member_departments WHERE name = 'Information Technology'))
ON CONFLICT (name) DO NOTHING;

-- Legal functions
INSERT INTO functions (name, department_id) VALUES
('Acquisitions', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Compliance', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Contracts', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Corporate Secretary', (SELECT id FROM member_departments WHERE name = 'Legal')),
('eDiscovery', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Ethics', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Governance', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Governmental Affairs & Regulatory Law', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Intellectual Property & Patent', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Labor & Employment', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Lawyer / Attorney', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Legal', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Legal Counsel', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Legal Operations', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Litigation', (SELECT id FROM member_departments WHERE name = 'Legal')),
('Privacy', (SELECT id FROM member_departments WHERE name = 'Legal'))
ON CONFLICT (name) DO NOTHING;

-- Marketing functions
INSERT INTO functions (name, department_id) VALUES
('Advertising', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Brand Management', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Content Marketing', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Customer Experience', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Customer Marketing', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Demand Generation', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Digital Marketing', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('eCommerce Marketing', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Event Marketing', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Field Marketing', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Lead Generation', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Marketing', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Marketing Analytics / Insights', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Marketing Communications', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Marketing Operations', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Product Marketing', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Public Relations', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Search Engine Optimization / Pay Per Click', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Social Media Marketing', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Strategic Communications', (SELECT id FROM member_departments WHERE name = 'Marketing')),
('Technical Marketing', (SELECT id FROM member_departments WHERE name = 'Marketing'))
ON CONFLICT (name) DO NOTHING;

-- Medical & Health functions
INSERT INTO functions (name, department_id) VALUES
('Anesthesiology', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Chiropractics', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Clinical Systems', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Dentistry', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Dermatology', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Doctors / Physicians', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Epidemiology', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('First Responder', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Infectious Disease', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Medical Administration', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Medical Education & Training', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Medical Research', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Medicine', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Neurology', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Nursing', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Nutrition & Dietetics', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Obstetrics / Gynecology', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Oncology', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Ophthalmology', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Optometry', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Orthopedics', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Pathology', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Pediatrics', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Pharmacy', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Physical Therapy', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Psychiatry', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Psychology', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Public Health', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Radiology', (SELECT id FROM member_departments WHERE name = 'Medical & Health')),
('Social Work', (SELECT id FROM member_departments WHERE name = 'Medical & Health'))
ON CONFLICT (name) DO NOTHING;

-- Operations functions
INSERT INTO functions (name, department_id) VALUES
('Call Center', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Construction', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Corporate Strategy', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Customer Service / Support', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Enterprise Resource Planning', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Facilities Management', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Leasing', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Logistics', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Office Operations', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Operations', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Physical Security', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Project Development', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Quality Management', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Real Estate', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Safety', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Store Operations', (SELECT id FROM member_departments WHERE name = 'Operations')),
('Supply Chain', (SELECT id FROM member_departments WHERE name = 'Operations'))
ON CONFLICT (name) DO NOTHING;

-- Sales functions
INSERT INTO functions (name, department_id) VALUES
('Account Management', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Business Development', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Channel Sales', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Customer Retention & Development', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Customer Success', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Field / Outside Sales', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Inside Sales', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Partnerships', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Revenue Operations', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Sales', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Sales Enablement', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Sales Engineering', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Sales Operations', (SELECT id FROM member_departments WHERE name = 'Sales')),
('Sales Training', (SELECT id FROM member_departments WHERE name = 'Sales'))
ON CONFLICT (name) DO NOTHING;

-- Consulting functions
INSERT INTO functions (name, department_id) VALUES
('Business Strategy Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Change Management Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Customer Experience Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Data Analytics Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Digital Transformation Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Environmental Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Financial Advisory Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Healthcare Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Human Resources Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Information Technology Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Management Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Marketing Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Mergers & Acquisitions Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Organizational Development Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Process Improvement Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Risk Management Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Sales Strategy Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Supply Chain Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Sustainability Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Tax Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Technology Implementation Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting')),
('Training & Development Consulting', (SELECT id FROM member_departments WHERE name = 'Consulting'))
ON CONFLICT (name) DO NOTHING;

COMMIT;

