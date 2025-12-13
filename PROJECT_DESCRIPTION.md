# AI Data Standardization Pipeline - Project Description

## Project Overview

Build an AI-powered data standardization pipeline that enriches job titles with standardized department, function, and seniority classifications. The pipeline will process LinkedIn member data and automatically classify job titles into a structured taxonomy, enabling powerful querying and analytics capabilities.

## Business Goals

### Primary Objectives
1. **Standardize job titles** - Transform unstructured job titles into structured classifications (Department, Function, Seniority)
2. **Enable querying** - Allow queries like "find all people in senior sales positions"
3. **Auto-triggered processing** - Automatically process new profiles and job title changes
4. **Extensible architecture** - Support future standardization pipelines (education majors, age estimation, startup flags, skill extraction, etc.)

### Success Criteria
- Successfully classify job titles into standardized taxonomy
- Process millions of records efficiently
- Automatically trigger on new data
- Support downstream features and pipelines
- Cost-effective AI usage
- Fault-tolerant and resilient

## Data Source

**Location:** `/Users/mo/work/villagehq/standardization_pipeline/li_member_csv_202403`

**Key Tables:**
- `member` - Contains member profiles with `title` field (current job title)
- `member_experience` - Contains work experience with `title` field (historical job titles)
- Additional tables: education, skills, certifications, etc.

**Data Format:**
- PostgreSQL/MySQL compatible CSV dumps
- Compressed `.csv.gz` files
- Database structure files provided (`db_structure_postgresql.sql`, `db_structure_mysql.sql`)

## Standardization Taxonomy

### Seniority Levels
- Owner
- Founder
- C-suite
- Partner
- VP
- Head
- Director
- Manager
- Senior
- Entry
- Intern

### Departments & Functions

1. **C-Suite**
   - Executive, Finance Executive, Founder, Human Resources Executive, Information Technology Executive, Legal Executive, Marketing Executive, Medical & Health Executive, Operations Executive, Sales Leader

2. **Engineering & Technical**
   - Artificial Intelligence / Machine Learning, Bioengineering, Biometrics, Business Intelligence, Chemical Engineering, Cloud / Mobility, Data Science, DevOps, Digital Transformation, Emerging Technology / Innovation, Engineering & Technical, Industrial Engineering, Mechanic, Mobile Development, Product Development, Product Management, Project Management, Research & Development, Scrum Master / Agile Coach, Software Development, Support / Technical Services, Technician, Technology Operations, Test / Quality Assurance, UI / UX, Web Development

3. **Design**
   - All Design, Product or UI/UX Design, Graphic / Visual / Brand Design

4. **Education**
   - Teacher, Principal, Superintendent, Professor

5. **Finance**
   - Accounting, Finance, Financial Planning & Analysis, Financial Reporting, Financial Strategy, Financial Systems, Internal Audit & Control, Investor Relations, Mergers & Acquisitions, Real Estate Finance, Financial Risk, Shared Services, Sourcing / Procurement, Tax, Treasury

6. **Human Resources**
   - Compensation & Benefits, Culture, Diversity & Inclusion, Employee & Labor Relations, Health & Safety, Human Resource Information System, Human Resources, HR Business Partner, Learning & Development, Organizational Development, Recruiting & Talent Acquisition, Talent Management, Workforce Management, People Operations

7. **Information Technology**
   - Application Development, Business Service Management / ITSM, Collaboration & Web App, Data Center, Data Warehouse, Database Administration, eCommerce Development, Enterprise Architecture, Help Desk / Desktop Services, HR / Financial / ERP Systems, Information Security, Information Technology, Infrastructure, IT Asset Management, IT Audit / IT Compliance, IT Operations, IT Procurement, IT Strategy, IT Training, Networking, Project & Program Management, Quality Assurance, Retail / Store Systems, Servers, Storage & Disaster Recovery, Telecommunications, Virtualization

8. **Legal**
   - Acquisitions, Compliance, Contracts, Corporate Secretary, eDiscovery, Ethics, Governance, Governmental Affairs & Regulatory Law, Intellectual Property & Patent, Labor & Employment, Lawyer / Attorney, Legal, Legal Counsel, Legal Operations, Litigation, Privacy

9. **Marketing**
   - Advertising, Brand Management, Content Marketing, Customer Experience, Customer Marketing, Demand Generation, Digital Marketing, eCommerce Marketing, Event Marketing, Field Marketing, Lead Generation, Marketing, Marketing Analytics / Insights, Marketing Communications, Marketing Operations, Product Marketing, Public Relations, Search Engine Optimization / Pay Per Click, Social Media Marketing, Strategic Communications, Technical Marketing

10. **Medical & Health**
    - Anesthesiology, Chiropractics, Clinical Systems, Dentistry, Dermatology, Doctors / Physicians, Epidemiology, First Responder, Infectious Disease, Medical Administration, Medical Education & Training, Medical Research, Medicine, Neurology, Nursing, Nutrition & Dietetics, Obstetrics / Gynecology, Oncology, Ophthalmology, Optometry, Orthopedics, Pathology, Pediatrics, Pharmacy, Physical Therapy, Psychiatry, Psychology, Public Health, Radiology, Social Work

11. **Operations**
    - Call Center, Construction, Corporate Strategy, Customer Service / Support, Enterprise Resource Planning, Facilities Management, Leasing, Logistics, Office Operations, Operations, Physical Security, Project Development, Quality Management, Real Estate, Safety, Store Operations, Supply Chain

12. **Sales**
    - Account Management, Business Development, Channel Sales, Customer Retention & Development, Customer Success, Field / Outside Sales, Inside Sales, Partnerships, Revenue Operations, Sales, Sales Enablement, Sales Engineering, Sales Operations, Sales Training

13. **Consulting**
    - Business Strategy Consulting, Change Management Consulting, Customer Experience Consulting, Data Analytics Consulting, Digital Transformation Consulting, Environmental Consulting, Financial Advisory Consulting, Healthcare Consulting, Human Resources Consulting, Information Technology Consulting, Management Consulting, Marketing Consulting, Mergers & Acquisitions Consulting, Organizational Development Consulting, Process Improvement Consulting, Risk Management Consulting, Sales Strategy Consulting, Supply Chain Consulting, Sustainability Consulting, Tax Consulting, Technology Implementation Consulting, Training & Development Consulting

## Example Classifications

| Job Title (Before) | Department | Function | Seniority |
|-------------------|-----------|---------|-----------|
| Backend Engineer | Engineering & Technical | Software Development | Entry |
| Head of Sales | Sales | Sales | Head |
| Sales Executive | Sales | Sales | Entry |
| SWE Intern | Engineering & Technical | Software Development | Intern |

## Functional Requirements

### Core Features
1. **Job Title Standardization**
   - Accept raw job title as input
   - Return standardized Department, Function, and Seniority
   - Use AI/LLM for classification
   - Enforce strict taxonomy (no custom classifications)

2. **Data Processing**
   - Process job titles from `member.title` (current title)
   - Process job titles from `member_experience.title` (historical titles)
   - Handle millions of records efficiently
   - Support batch and streaming processing

3. **Auto-Triggered Pipeline**
   - Detect new member profiles
   - Detect new job titles (e.g., from job changes)
   - Automatically trigger standardization
   - Update standardized fields in database

4. **Query Interface**
   - Query by standardized fields (Department, Function, Seniority)
   - Example: "Find all people in senior sales positions"
   - Support complex queries (e.g., "Senior engineers at tech companies")

5. **Extensibility**
   - Modular architecture for adding new pipelines
   - Plugin system for downstream features
   - Event-driven architecture for pipeline triggers

### Future Pipeline Examples
- Standardize education major and estimate years
- Estimate age based on education and first experience
- Worked at a venture-backed startup flag
- Auto-extract skills from job descriptions
- Total years of experience in a certain skill (e.g., neo4j experience)

## Non-Functional Requirements

### Performance
- Process millions of records efficiently
- Support batch processing for historical data
- Support real-time/streaming for new data
- Optimize AI API calls (batching, caching, rate limiting)

### Scalability
- Horizontal scaling capability
- Handle increasing data volume
- Support concurrent processing

### Reliability
- Fault-tolerant design
- Error handling and retry logic
- Data consistency guarantees
- Idempotent operations

### Cost Efficiency
- Optimize AI API costs
- Caching strategies for repeated classifications
- Batch processing to reduce API calls
- Cost monitoring and alerting

### Maintainability
- Modular, reusable components
- Clear separation of concerns
- Comprehensive logging and monitoring
- Easy to extend with new pipelines

## Technical Considerations

### Architecture Patterns
- **Microservices** - Separate services for different concerns
- **Event-driven** - Trigger pipelines on data changes
- **Pipeline pattern** - Reusable pipeline components
- **Plugin architecture** - Extensible downstream features

### Technology Stack (To Be Determined)
- **Database**: PostgreSQL (recommended) or MySQL
- **AI/LLM**: OpenAI GPT-4, Anthropic Claude, or similar
- **Processing**: Python, Apache Airflow, or similar
- **Message Queue**: RabbitMQ, Apache Kafka, or similar
- **Caching**: Redis or similar
- **Monitoring**: Prometheus, Grafana, or similar

### Key Design Decisions Needed
1. **AI Provider Selection**
   - Cost vs. accuracy trade-offs
   - API rate limits and quotas
   - Response time requirements

2. **Processing Strategy**
   - Batch vs. streaming
   - Processing frequency
   - Backfill strategy for historical data

3. **Caching Strategy**
   - Cache identical job titles
   - Cache invalidation policy
   - Cache storage (Redis, database, etc.)

4. **Database Schema**
   - Add standardized fields to existing tables
   - Create separate standardization table
   - Indexing strategy for query performance

5. **Change Detection**
   - How to detect new/updated job titles
   - Polling vs. event-driven
   - Change tracking mechanism

## Deliverables

### Stage 1: Tech Spec (2 days - unpaid)
**Deadline:** Maximum 2 days for first version

**Contents:**
- High-level architecture diagram
- Component breakdown and responsibilities
- Technology stack selection with rationale
- Database schema design
- API design (if applicable)
- Processing flow diagrams
- Caching and optimization strategies
- Error handling and fault tolerance
- Cost estimation and optimization plan
- Milestones and time estimates
- Risk assessment and mitigation strategies

**Format:** Markdown document with diagrams (Mermaid, PlantUML, or images)

### Stage 2: Fully Functioning Pipeline (7 days - paid)
**Deadline:** Maximum 7 days after tech spec alignment

**Contents:**
- Deployed application on chosen platform
- Working standardization pipeline
- Database with standardized data
- Query interface/demo
- Documentation

**Demo Video Requirements:**
1. Add 1,000 sample job titles to database
2. Show standardization pipeline processing new data
3. Execute query using standardized fields to show unique people results
4. Demonstrate auto-trigger functionality (if implemented)

## Project Evaluation Criteria

1. **Spec Structure & Clarity** - Should exceed expectations
   - Clear, well-organized documentation
   - Comprehensive coverage of requirements
   - Easy to understand for technical and non-technical stakeholders

2. **Architecture & API Design** - Should exceed expectations
   - Scalable, maintainable architecture
   - Well-designed interfaces and APIs
   - Extensible for future pipelines
   - Performance and cost optimizations

3. **Collaboration and Alignment** - Should exceed expectations
   - Proactive communication
   - Responsive to feedback
   - Clear explanation of decisions
   - Alignment with business goals

## Project Timeline

### Phase 1: Tech Spec (Days 1-2)
- Day 1: Research, architecture design, initial spec draft
- Day 2: Refinement, review, alignment meeting

### Phase 2: Implementation (Days 3-9)
- Days 3-4: Core infrastructure setup
- Days 5-6: Standardization pipeline implementation
- Days 7-8: Auto-trigger and query interface
- Day 9: Testing, deployment, demo preparation

## Next Steps

1. Review and align on project description
2. Begin Stage 1: Tech Spec development
3. Schedule alignment meeting after spec completion
4. Proceed to Stage 2: Implementation after spec approval

## Questions to Resolve

1. **Data Access**
   - Database connection details
   - Preferred database (PostgreSQL vs. MySQL)
   - Read/write access requirements

2. **AI Provider**
   - Preferred AI/LLM provider
   - API key management
   - Budget constraints

3. **Deployment**
   - Preferred deployment platform (AWS, GCP, Azure, etc.)
   - Infrastructure preferences (containers, serverless, etc.)
   - Access and credentials

4. **Priority**
   - Which tables to prioritize (member vs. member_experience)
   - Historical data backfill requirements
   - Real-time vs. batch processing priority

5. **Downstream Features**
   - Which future pipelines are highest priority
   - Integration requirements
   - Event/notification requirements

---

**Document Version:** 1.0  
**Last Updated:** 2024-03  
**Status:** Initial Draft


