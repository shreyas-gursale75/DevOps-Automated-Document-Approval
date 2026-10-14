# DevOps Mini Project

**Topic:** Automated Controlled Document Version Approval System  
*(Template Reference: Conference Registration Portal / Controlled Document Workflow)*

---

## Phases & Deliverables Overview

### Phase 1: Problem Definition and Scope
- **Task:** Study the real-time need for the system. Identify target users, existing pain points, stakeholders, constraints and measurable success criteria. Freeze a small 15-Task MVP scope.
- **Deliverable:** Problem statement, stakeholder list, objectives, constraints, and approved MVP scope.

### Phase 2: Agile Planning and DevOps Workflow
- **Task:** Create user stories and acceptance criteria. Prepare a product backlog, 15-Task Kanban/Scrum plan, Definition of Done, and a DevOps lifecycle diagram from development to operations.
- **Deliverable:** Backlog, task board, sprint plan, Definition of Done, and DevOps workflow diagram.

### Phase 3: Requirements, Architecture and Technology Setup
- **Task:** Design the minimum application architecture. The MVP should cover submission/registration form, validation, approval/confirmation, document/participant listing, and status tracking. Select the programming stack, build tool, database, deployment target, and local development setup.
- **Deliverable:** SRS summary, use-case diagram, architecture diagram, data model/API list, and working local setup.

### Phase 4: Git and GitHub Repository Initialization
- **Task:** Create a Git/GitHub repository. Add README, `.gitignore`, folder structure, issue templates, and branch naming rules. Commit the initial application skeleton using meaningful commit messages.
- **Deliverable:** Repository URL, README, initial commits, issues, and branch policy.

### Phase 5: Feature Development with Branching
- **Task:** Implement the first core workflow on a feature branch. Use `add`, `commit`, `push`, `pull`, and `log`. Raise a pull request, review changes, and merge into the development branch.
- **Deliverable:** Working feature 1, feature branch, pull request, review comments, and merge evidence.

### Phase 6: MVP Completion and Git Collaboration
- **Task:** Implement the remaining essential MVP functions: submission/registration form, validation, approval/confirmation workflow, listing, and status tracking. Demonstrate a second feature branch, conflict creation/resolution, tagging, and a release-ready source baseline.
- **Deliverable:** Functional MVP, resolved merge conflict, tagged version, and updated backlog.

### Phase 7: Jenkins Installation and Continuous Integration Job
- **Task:** Install and configure Jenkins. Connect the repository and create an automated build job triggered by commit or scheduled polling. Archive the build artefact.
- **Deliverable:** Configured Jenkins job, successful build log, trigger evidence, and archived artefact.

### Phase 8: Pipeline as Code and Server Deployment
- **Task:** Create a Jenkinsfile with checkout, build, package, and deploy stages. Deploy the build to Tomcat/Nginx or Node/Docker and parameterize at least one environment setting.
- **Deliverable:** Jenkinsfile, successful pipeline run, deployed application URL/screenshot, and configuration evidence.

### Phase 9: Selenium Test Design and Local Execution
- **Task:** Identify 3 to 5 critical user journeys. Write automated end-to-end / Selenium WebDriver test cases with assertions, test data, and screenshots for failures. Execute the suite locally.
- **Deliverable:** Test plan, automated test scripts, local test report, and failure screenshot mechanism.

### Phase 10: Continuous Testing in Jenkins
- **Task:** Integrate the automated test suite into Jenkins. Publish test reports and configure the pipeline so failed tests stop deployment. Correct at least one deliberately introduced defect and rerun the pipeline.
- **Deliverable:** Jenkins test report, failed pipeline evidence, defect correction commit, and successful rerun.

### Phase 11: Docker Image and Container Lifecycle
- **Task:** Create a Dockerfile. Build and tag the image, run the container, map ports, inspect logs, stop/restart/remove containers, and document the complete container lifecycle.
- **Deliverable:** Dockerfile, image details, Docker command log, and running container evidence.

### Phase 12: Jenkins-Docker Continuous Deployment
- **Task:** Extend the Jenkins pipeline to build a versioned Docker image, publish it to Docker Hub or a local registry, and deploy a fresh container automatically after successful tests.
- **Deliverable:** Versioned image, registry evidence, and end-to-end commit-to-container pipeline.

### Phase 13: Configuration Management Script
- **Task:** Identify all server prerequisites: packages, users, folders, files, ports, and services. Create either an Ansible inventory and YAML playbook or Puppet manifest to configure the target node.
- **Deliverable:** Configuration specification, Ansible playbook / Puppet manifest, and first execution log.

### Phase 14: Automated Provisioning and Reliability Validation
- **Task:** Provision a clean target environment using Ansible / Puppet. Deploy the application or container, rerun the automation to demonstrate idempotency, perform a health check, and test rollback/recovery to the previous stable release.
- **Deliverable:** Provisioned node, idempotency evidence, health-check result, and rollback/recovery demonstration.
