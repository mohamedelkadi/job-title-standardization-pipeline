# Standardization Taxonomy

This document defines the complete taxonomy used for job title standardization. All classifications must conform to these exact values - no custom classifications are allowed.

## Seniority Levels

The taxonomy includes 11 seniority levels, ordered from highest to lowest:

1. **Owner** - Business owner, proprietor
2. **Founder** - Company founder, co-founder
3. **C-suite** - Chief Executive Officer, Chief Technology Officer, etc.
4. **Partner** - Business partner, law firm partner
5. **VP** - Vice President
6. **Head** - Head of department, Head of function
7. **Director** - Director level
8. **Manager** - Manager level
9. **Senior** - Senior individual contributor
10. **Entry** - Entry level, junior, associate
11. **Intern** - Intern, intern-level

## Departments

The taxonomy includes 13 departments:

### 1. C-Suite
Executive leadership roles across all functions.

**Functions**:
- Executive
- Finance Executive
- Founder
- Human Resources Executive
- Information Technology Executive
- Legal Executive
- Marketing Executive
- Medical & Health Executive
- Operations Executive
- Sales Leader

### 2. Engineering & Technical
Technical roles in software, hardware, and engineering.

**Functions**:
- Artificial Intelligence / Machine Learning
- Bioengineering
- Biometrics
- Business Intelligence
- Chemical Engineering
- Cloud / Mobility
- Data Science
- DevOps
- Digital Transformation
- Emerging Technology / Innovation
- Engineering & Technical
- Industrial Engineering
- Mechanic
- Mobile Development
- Product Development
- Product Management
- Project Management
- Research & Development
- Scrum Master / Agile Coach
- Software Development
- Support / Technical Services
- Technician
- Technology Operations
- Test / Quality Assurance
- UI / UX
- Web Development

### 3. Design
Design-related roles across product, UI/UX, and visual design.

**Functions**:
- All Design
- Product or UI/UX Design
- Graphic / Visual / Brand Design

### 4. Education
Educational roles in schools, universities, and training.

**Functions**:
- Teacher
- Principal
- Superintendent
- Professor

### 5. Finance
Financial management, accounting, and related roles.

**Functions**:
- Accounting
- Finance
- Financial Planning & Analysis
- Financial Reporting
- Financial Strategy
- Financial Systems
- Internal Audit & Control
- Investor Relations
- Mergers & Acquisitions
- Real Estate Finance
- Financial Risk
- Shared Services
- Sourcing / Procurement
- Tax
- Treasury

### 6. Human Resources
HR, talent management, and people operations.

**Functions**:
- Compensation & Benefits
- Culture
- Diversity & Inclusion
- Employee & Labor Relations
- Health & Safety
- Human Resource Information System
- Human Resources
- HR Business Partner
- Learning & Development
- Organizational Development
- Recruiting & Talent Acquisition
- Talent Management
- Workforce Management
- People Operations

### 7. Information Technology
IT infrastructure, systems, and operations.

**Functions**:
- Application Development
- Business Service Management / ITSM
- Collaboration & Web App
- Data Center
- Data Warehouse
- Database Administration
- eCommerce Development
- Enterprise Architecture
- Help Desk / Desktop Services
- HR / Financial / ERP Systems
- Information Security
- Information Technology
- Infrastructure
- IT Asset Management
- IT Audit / IT Compliance
- IT Operations
- IT Procurement
- IT Strategy
- IT Training
- Networking
- Project & Program Management
- Quality Assurance
- Retail / Store Systems
- Servers
- Storage & Disaster Recovery
- Telecommunications
- Virtualization

### 8. Legal
Legal, compliance, and regulatory roles.

**Functions**:
- Acquisitions
- Compliance
- Contracts
- Corporate Secretary
- eDiscovery
- Ethics
- Governance
- Governmental Affairs & Regulatory Law
- Intellectual Property & Patent
- Labor & Employment
- Lawyer / Attorney
- Legal
- Legal Counsel
- Legal Operations
- Litigation
- Privacy

### 9. Marketing
Marketing, communications, and brand management.

**Functions**:
- Advertising
- Brand Management
- Content Marketing
- Customer Experience
- Customer Marketing
- Demand Generation
- Digital Marketing
- eCommerce Marketing
- Event Marketing
- Field Marketing
- Lead Generation
- Marketing
- Marketing Analytics / Insights
- Marketing Communications
- Marketing Operations
- Product Marketing
- Public Relations
- Search Engine Optimization / Pay Per Click
- Social Media Marketing
- Strategic Communications
- Technical Marketing

### 10. Medical & Health
Healthcare, medical, and health-related roles.

**Functions**:
- Anesthesiology
- Chiropractics
- Clinical Systems
- Dentistry
- Dermatology
- Doctors / Physicians
- Epidemiology
- First Responder
- Infectious Disease
- Medical Administration
- Medical Education & Training
- Medical Research
- Medicine
- Neurology
- Nursing
- Nutrition & Dietetics
- Obstetrics / Gynecology
- Oncology
- Ophthalmology
- Optometry
- Orthopedics
- Pathology
- Pediatrics
- Pharmacy
- Physical Therapy
- Psychiatry
- Psychology
- Public Health
- Radiology
- Social Work

### 11. Operations
Operations, facilities, logistics, and general operations.

**Functions**:
- Call Center
- Construction
- Corporate Strategy
- Customer Service / Support
- Enterprise Resource Planning
- Facilities Management
- Leasing
- Logistics
- Office Operations
- Operations
- Physical Security
- Project Development
- Quality Management
- Real Estate
- Safety
- Store Operations
- Supply Chain

### 12. Sales
Sales, business development, and customer success.

**Functions**:
- Account Management
- Business Development
- Channel Sales
- Customer Retention & Development
- Customer Success
- Field / Outside Sales
- Inside Sales
- Partnerships
- Revenue Operations
- Sales
- Sales Enablement
- Sales Engineering
- Sales Operations
- Sales Training

### 13. Consulting
Consulting roles across various domains.

**Functions**:
- Business Strategy Consulting
- Change Management Consulting
- Customer Experience Consulting
- Data Analytics Consulting
- Digital Transformation Consulting
- Environmental Consulting
- Financial Advisory Consulting
- Healthcare Consulting
- Human Resources Consulting
- Information Technology Consulting
- Management Consulting
- Marketing Consulting
- Mergers & Acquisitions Consulting
- Organizational Development Consulting
- Process Improvement Consulting
- Risk Management Consulting
- Sales Strategy Consulting
- Supply Chain Consulting
- Sustainability Consulting
- Tax Consulting
- Technology Implementation Consulting
- Training & Development Consulting

## Example Classifications

| Job Title (Before) | Department | Function | Seniority |
|-------------------|-----------|---------|-----------|
| Backend Engineer | Engineering & Technical | Software Development | Entry |
| Head of Sales | Sales | Sales | Head |
| Sales Executive | Sales | Sales | Entry |
| SWE Intern | Engineering & Technical | Software Development | Intern |
| Senior Software Engineer | Engineering & Technical | Software Development | Senior |
| VP of Engineering | Engineering & Technical | Engineering & Technical | VP |
| CEO | C-Suite | Executive | C-suite |
| Founder | C-Suite | Founder | Founder |
| Product Manager | Engineering & Technical | Product Management | Manager |
| Data Scientist | Engineering & Technical | Data Science | Entry |
| Director of Marketing | Marketing | Marketing | Director |
| HR Manager | Human Resources | Human Resources | Manager |
| Finance Director | Finance | Finance | Director |

## Validation Rules

All classifications must:

1. **Department**: Must be one of the 13 valid departments listed above
2. **Function**: Must be a valid function that belongs to the specified department
3. **Seniority**: Must be one of the 11 valid seniority levels listed above
4. **Relationships**: Function must belong to the specified department (enforced by validator)

## Taxonomy Maintenance

The taxonomy is maintained in:
- Database lookup tables (`member_departments`, `member_functions`, `member_seniority_levels`)
- Validator component (`src/validator.py`)
- Migration scripts (`migrations/002_seed_taxonomy_data.sql`)

Changes to the taxonomy require:
1. Database migration
2. Validator update
3. Classifier pattern updates (if applicable)
4. Documentation update
