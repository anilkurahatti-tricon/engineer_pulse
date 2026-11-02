-- =============================================================================
-- Engineer Pulse: Seed Data for Supabase
-- Can be run directly in the Supabase SQL Editor:
-- https://supabase.com/dashboard/project/_/sql
-- =============================================================================

-- Ensure created_at has a server-side default timestamp so it never fails on NULL
ALTER TABLE employees ALTER COLUMN created_at SET DEFAULT NOW();
ALTER TABLE employee_projects ALTER COLUMN created_at SET DEFAULT NOW();
ALTER TABLE employee_skills ALTER COLUMN created_at SET DEFAULT NOW();
ALTER TABLE employee_feedback ALTER COLUMN created_at SET DEFAULT NOW();

-- 1. Insert Additional Employees (skips existing emails)
INSERT INTO employees (name, email, title, department, total_experience_years, bio, created_at)
VALUES
('Meera Nair', 'meera.nair@squad4.dev', 'Cloud Solutions Architect', 'Cloud Platform', 8.0, 'Specializes in multi-region cloud migrations, AWS/Azure hybrid infrastructure, and Terraform IaC.', NOW()),
('David Chen', 'david.chen@squad4.dev', 'Senior .NET Engineer', 'Enterprise Systems', 6.5, 'Expert in ASP.NET Core, C#, Entity Framework, and modernizing legacy enterprise systems.', NOW()),
('Sara Khan', 'sara.khan@squad4.dev', 'Machine Learning Specialist', 'AI Platform', 4.5, 'Focuses on NLP, LLM fine-tuning, retrieval-augmented generation (RAG), and vector embeddings.', NOW()),
('Marcus Johnson', 'marcus.johnson@squad4.dev', 'Security & Compliance Lead', 'InfoSec', 5.5, 'Specializes in application security, OAuth2/OIDC, zero-trust architectures, and OWASP compliance.', NOW()),
('Elena Rostova', 'elena.rostova@squad4.dev', 'Senior Frontend Engineer', 'UX Platform', 5.0, 'Builds accessible design systems, micro-frontends, and high-performance React/TypeScript SPAs.', NOW()),
('Rohan Patel', 'rohan.patel@squad4.dev', 'Data Platform Engineer', 'Data Engineering', 6.0, 'Experienced in real-time data streaming with Apache Kafka, Spark, and data lake pipelines.', NOW()),
('Sophie Martin', 'sophie.martin@squad4.dev', 'Mobile Solutions Engineer', 'Mobile Platform', 4.0, 'Builds cross-platform React Native apps, offline sync mechanisms, and mobile CI/CD pipelines.', NOW()),
('Liam O''Connor', 'liam.oconnor@squad4.dev', 'Site Reliability Engineer', 'Infrastructure', 5.0, 'Expert in Kubernetes cluster operations, Prometheus/Grafana observability, and chaos engineering.', NOW()),
('Ananya Joshi', 'ananya.joshi@squad4.dev', 'QA Automation Lead', 'Quality Engineering', 4.5, 'Designs end-to-end test automation frameworks with Playwright, Cypress, and continuous testing.', NOW()),
('Tyler Brooks', 'tyler.brooks@squad4.dev', 'Distributed Systems Architect', 'Core Platform', 7.5, 'Architects low-latency distributed microservices in Go, gRPC, and Redis message queues.', NOW())
ON CONFLICT (email) DO NOTHING;

-- 2. Insert Additional Projects (employee_projects table)
INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'David Chen', 'Customer Portal Modernization', 'Lead Application Architect',
       'ASP.NET Core Web API, REST API design, Angular, SQL Server, Docker, Azure App Service',
       'Rebuild legacy customer portal as an ASP.NET Core Web API backend with a high-performance REST API layer and modern single-page frontend.', 8, NOW()
FROM employees e WHERE e.name = 'David Chen'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Customer Portal Modernization');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Tyler Brooks', 'Inventory Management Microservices Platform', 'Distributed Systems Lead',
       '.NET Microservices, RabbitMQ, Docker, Kubernetes, gRPC, PostgreSQL, React',
       'Distributed inventory management architecture built with resilient event-driven microservices communicating over RabbitMQ queues.', 7, NOW()
FROM employees e WHERE e.name = 'Tyler Brooks'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Inventory Management Microservices Platform');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Rohan Patel', 'Real-Time Event Streaming Pipeline', 'Data Streaming Architect',
       'Apache Kafka, Python, PostgreSQL, Docker, Redis',
       'Engineered real-time telemetry streaming backbone processing over 50,000 sensor and system telemetry messages per second.', 6, NOW()
FROM employees e WHERE e.name = 'Rohan Patel'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Real-Time Event Streaming Pipeline');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Meera Nair', 'Cloud Migration & Multi-Region Kubernetes', 'Cloud Solutions Architect',
       'AWS, Kubernetes, Terraform (IaC), Prometheus & Grafana, CI/CD',
       'Led zero-downtime migration of multi-tier applications to AWS multi-region EKS clusters provisioned with automated Terraform infrastructure.', 9, NOW()
FROM employees e WHERE e.name = 'Meera Nair'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Cloud Migration & Multi-Region Kubernetes');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Sophie Martin', 'Field Service Mobile App Backend', 'Mobile Backend Lead',
       'React Native, GraphQL, Azure Functions, OAuth2, Azure SQL',
       'Developed resilient offline-first mobile sync backend serving thousands of field engineers with bi-directional conflict resolution.', 5, NOW()
FROM employees e WHERE e.name = 'Sophie Martin'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Field Service Mobile App Backend');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Marcus Johnson', 'Enterprise Identity & Zero Trust Access Gate', 'Security Lead',
       'OAuth2 / OpenID Connect, JWT Authentication, FastAPI, Redis, OWASP Security',
       'Centralized company-wide authentication and authorization gateway enforcing strict OAuth2 protocols and role-based policies.', 6, NOW()
FROM employees e WHERE e.name = 'Marcus Johnson'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Enterprise Identity & Zero Trust Access Gate');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Ananya Joshi', 'Automated End-to-End Testing Suite', 'Test Automation Architect',
       'Playwright & Cypress Testing, PyTest, GitHub Actions, Docker',
       'Architected unified cross-browser and regression test automation suite running parallelized runs in CI/CD pipelines.', 4, NOW()
FROM employees e WHERE e.name = 'Ananya Joshi'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Automated End-to-End Testing Suite');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Sara Khan', 'Autonomous RAG Knowledge Assistant', 'AI Application Engineer',
       'Python, LangChain, PyTorch, Vector Databases, OpenAI Embeddings, FastAPI',
       'Implemented enterprise RAG search system indexing codebase repositories and technical handbooks with hybrid vector retrieval.', 5, NOW()
FROM employees e WHERE e.name = 'Sara Khan'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Autonomous RAG Knowledge Assistant');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Tyler Brooks', 'High-Speed Market Data Ingestion Engine', 'Systems Architect',
       'Go (Golang), gRPC, Redis, Docker, PostgreSQL',
       'Low-latency ingestion daemon ingesting live financial order books with sub-millisecond gRPC processing and Redis buffering.', 6, NOW()
FROM employees e WHERE e.name = 'Tyler Brooks'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'High-Speed Market Data Ingestion Engine');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Elena Rostova', 'Design System & Accessible Component Library', 'Lead Frontend Designer',
       'React, TypeScript, Material UI & Styling, Web Performance Optimization',
       'Engineered enterprise design system adhering to WCAG 2.1 AA standards, consumed by 8 internal web applications.', 6, NOW()
FROM employees e WHERE e.name = 'Elena Rostova'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Design System & Accessible Component Library');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Rohan Patel', 'Data Warehouse & Analytics ETL Engine', 'Data Pipeline Lead',
       'Apache Spark, Python, PostgreSQL, AWS Cloud Architecture',
       'Built distributed analytical ETL pipeline aggregating daily product usage metrics into optimized columnar data lakes.', 5, NOW()
FROM employees e WHERE e.name = 'Rohan Patel'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Data Warehouse & Analytics ETL Engine');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Liam O''Connor', 'Observability & Distributed Tracing Stack', 'SRE Lead',
       'Kubernetes, Prometheus & Grafana Observability, Linux, Docker',
       'Standardized unified telemetry monitoring with OpenTelemetry, Prometheus metrics alerts, and Grafana interactive squad dashboards.', 4, NOW()
FROM employees e WHERE e.name = 'Liam O''Connor'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Observability & Distributed Tracing Stack');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Elena Rostova', 'Micro-Frontend Shell & Module Federation', 'Frontend Architect',
       'React, TypeScript, Vite, Material UI & Styling',
       'Designed pluggable micro-frontend shell allowing autonomous squad deployments without coordinated application rollouts.', 5, NOW()
FROM employees e WHERE e.name = 'Elena Rostova'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Micro-Frontend Shell & Module Federation');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Jane Doe', 'Scalable Asynchronous Job Queue', 'Senior Backend Engineer',
       'Python & FastAPI, Redis caching & Messaging, Docker, PostgreSQL',
       'Asynchronous job scheduling worker pool processing long-running analytics jobs with distributed rate-limiting and auto-retries.', 4, NOW()
FROM employees e WHERE e.name = 'Jane Doe'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Scalable Asynchronous Job Queue');

INSERT INTO employee_projects (employee_id, employee_name, project_name, role, technologies, description, duration_months, created_at)
SELECT e.id, 'Priya Sharma', 'Real-Time Feature Store for ML Models', 'ML Platform Engineer',
       'PostgreSQL & pgvector Search, Python, Redis, Machine Learning & Embeddings',
       'Engineered low-latency feature serving store enabling production ML pipelines to retrieve precomputed and online embeddings.', 5, NOW()
FROM employees e WHERE e.name = 'Priya Sharma'
AND NOT EXISTS (SELECT 1 FROM employee_projects WHERE project_name = 'Real-Time Feature Store for ML Models');

-- 3. Insert Additional Skills
INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'Meera Nair', 'AWS Cloud Architecture', 'Expert', 6.0, NOW() FROM employees e WHERE e.name = 'Meera Nair'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'Meera Nair' AND skill_name = 'AWS Cloud Architecture');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'Meera Nair', 'Terraform (IaC)', 'Advanced', 4.5, NOW() FROM employees e WHERE e.name = 'Meera Nair'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'Meera Nair' AND skill_name = 'Terraform (IaC)');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'David Chen', 'ASP.NET Core Web API', 'Expert', 6.0, NOW() FROM employees e WHERE e.name = 'David Chen'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'David Chen' AND skill_name = 'ASP.NET Core Web API');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'David Chen', 'C# & .NET 8', 'Expert', 6.5, NOW() FROM employees e WHERE e.name = 'David Chen'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'David Chen' AND skill_name = 'C# & .NET 8');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'Sara Khan', 'Vector Databases & RAG', 'Expert', 3.5, NOW() FROM employees e WHERE e.name = 'Sara Khan'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'Sara Khan' AND skill_name = 'Vector Databases & RAG');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'Marcus Johnson', 'OAuth2 / OpenID Connect', 'Expert', 5.0, NOW() FROM employees e WHERE e.name = 'Marcus Johnson'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'Marcus Johnson' AND skill_name = 'OAuth2 / OpenID Connect');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'Elena Rostova', 'React & Modern Hooks', 'Expert', 5.0, NOW() FROM employees e WHERE e.name = 'Elena Rostova'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'Elena Rostova' AND skill_name = 'React & Modern Hooks');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'Rohan Patel', 'Apache Kafka & Event Streaming', 'Expert', 5.0, NOW() FROM employees e WHERE e.name = 'Rohan Patel'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'Rohan Patel' AND skill_name = 'Apache Kafka & Event Streaming');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'Sophie Martin', 'React Native', 'Expert', 4.0, NOW() FROM employees e WHERE e.name = 'Sophie Martin'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'Sophie Martin' AND skill_name = 'React Native');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'Liam O''Connor', 'Kubernetes & Container Orchestration', 'Expert', 4.5, NOW() FROM employees e WHERE e.name = 'Liam O''Connor'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'Liam O''Connor' AND skill_name = 'Kubernetes & Container Orchestration');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'Ananya Joshi', 'Playwright & Cypress Testing', 'Expert', 4.0, NOW() FROM employees e WHERE e.name = 'Ananya Joshi'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'Ananya Joshi' AND skill_name = 'Playwright & Cypress Testing');

INSERT INTO employee_skills (employee_id, employee_name, skill_name, proficiency_level, years_of_experience, created_at)
SELECT e.id, 'Tyler Brooks', 'Go (Golang)', 'Expert', 5.5, NOW() FROM employees e WHERE e.name = 'Tyler Brooks'
AND NOT EXISTS (SELECT 1 FROM employee_skills WHERE employee_name = 'Tyler Brooks' AND skill_name = 'Go (Golang)');

-- 4. Verify Counts
SELECT
  (SELECT COUNT(*) FROM employees) AS total_employees,
  (SELECT COUNT(*) FROM employee_projects) AS total_projects,
  (SELECT COUNT(*) FROM employee_skills) AS total_skills,
  (SELECT COUNT(*) FROM employee_feedback) AS total_feedback;
