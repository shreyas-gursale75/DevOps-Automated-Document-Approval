# Software Requirements Specification (SRS) & Architecture Document
## Project: Automated Controlled Document Version Approval System

---

## 1. Executive Summary & Problem Definition

### 1.1 Problem Statement
In regulated industries (such as healthcare, aerospace, financial services, and ISO 9001/CMMI-certified software organizations), Standard Operating Procedures (SOPs), policy manuals, technical specifications, and release artifacts cannot simply be edited in place. Uncontrolled modifications introduce compliance violations, operational downtime, and legal liability. 

Existing traditional approaches rely on manual email exchanges, shared network drives, or fragmented paper-based routing sheets. These legacy methods suffer from:
- Lack of centralized traceability and tamper-evident audit trails.
- High risk of using obsolete or unapproved document versions in production.
- Ambiguous approval chains leading to bottlenecks and lost change requests.
- Absence of automated version increments (Major vs. Minor version semantics).

### 1.2 Proposed Solution: Automated Controlled Document Version Approval System
The **Automated Controlled Document Version Approval System** is a lightweight, high-integrity web application built with **Java 17, Maven, and Apache Tomcat (via Spring Boot Web)**. It automates the entire controlled document lifecycle:
1. **Creation & Drafting:** Authors initiate document records with metadata, categorization, and version 1.0 drafts.
2. **Controlled Modification & Versioning:** Modifications trigger semantic version branching (e.g., v1.1 for minor errata; v2.0 for major policy changes).
3. **Formal Review & Electronic Sign-off:** Documents transition to a `PENDING_APPROVAL` gate where designated reviewers approve or reject changes with mandatory review notes.
4. **Immutable Audit Logging:** Every lifecycle event (creation, submission, approval, rejection, version release) is captured with timestamps and actor identities in an append-only audit trail.
5. **Continuous DevOps Integration:** Packaged and delivered through an automated CI/CD pipeline using Maven, Jenkins, Docker, and Selenium.

---

## 2. Target Users, Stakeholders & Pain Points

| Stakeholder / Role | Key Responsibilities | Existing Pain Points | System Benefits |
|---|---|---|---|
| **Author / Originator** | Creates drafts, writes technical specifications, submits revisions. | Unclear status of submitted drafts; accidental overwrites of existing drafts. | Single portal to draft, track review progress, and submit version bumps. |
| **Reviewer / Approver** (Lead, Dept Head) | Inspects document content, verifies compliance, approves or rejects with feedback. | Overwhelmed with email requests; difficulty comparing versions. | Dedicated approval queue with one-click approval/rejection and comment logging. |
| **QA / Compliance Auditor** | Audits change history, verifies adherence to ISO/SOP standards. | Manual inspection of email logs; no immutable proof of who approved what. | Instant access to chronological, immutable audit logs with timestamps. |
| **DevOps / Release Engineer** | Packages, tests, containers, and deploys the system reliably. | Inconsistent manual deployments, lack of regression test suites. | Standardized Maven build, Dockerized deployment, automated Selenium tests. |

---

## 3. Measurable Success Criteria & Constraints

### 3.1 Measurable Objectives
- **Zero Unapproved Releases:** 100% of released documents must have a recorded approval timestamp and reviewer signature.
- **Traceability:** 100% of document modifications must generate a corresponding audit log entry.
- **Cycle Time Reduction:** Reduce document approval turnaround time from days to under 2 hours.
- **API Performance:** 95% of document retrieval and status transition requests respond in `< 150 ms`.

### 3.2 System Constraints
- **Stack Constraint:** Java 17, Apache Maven build system, Apache Tomcat web runtime (Spring Boot Embedded Tomcat).
- **Audit Immutability:** Audit trail records cannot be edited or deleted through any client API.
- **State Transition Guard:** An unapproved draft cannot directly enter the `RELEASED` state without passing the `APPROVED` gate.

---

## 4. 15-Task MVP Scope Breakdown

| Task ID | Component / Module | Scope Description |
|---|---|---|
| **TASK-01** | Architecture & SRS | Finalize SRS summary, Use-Case diagram, Architecture diagram, and Data Model. |
| **TASK-02** | Project Skeleton & Maven | Initialize Maven multi-tier structure with Java 17 and Spring Boot Web / Tomcat. |
| **TASK-03** | Core Data Model | Implement `Document`, `DocumentVersion`, `ApprovalStatus`, and `AuditLog` domain entities. |
| **TASK-04** | Document Repository | Build in-memory thread-safe repository layer with search, filter, and persistence hooks. |
| **TASK-05** | Document Service Layer | Implement business logic for state transitions, validation, and semantic versioning. |
| **TASK-06** | Audit Trail Service | Implement append-only event logging for all CRUD and status transition operations. |
| **TASK-07** | RESTful API Controllers | Expose endpoints for document creation, versioning, submission, approval, and logs. |
| **TASK-08** | Request Validation & Error Handling | Enforce field constraints (non-empty title, valid enum transitions) with clean error responses. |
| **TASK-09** | Health Check & Metrics | Implement `/api/health` endpoint for DevOps readiness and liveness probes. |
| **TASK-10** | Modern Web Frontend | Build responsive Glassmorphic dashboard (HTML5, Vanilla CSS3, modern JavaScript). |
| **TASK-11** | Document Submission UI | Implement client-side submission form with category selection and real-time validation. |
| **TASK-12** | Approval Queue UI | Implement review modal with approve/reject actions and mandatory feedback remarks. |
| **TASK-13** | Version History & Diff Viewer | Implement side-by-side or chronological version timeline displaying revisions. |
| **TASK-14** | Audit Log Timeline UI | Build compliance view rendering chronological audit events with role badges. |
| **TASK-15** | Unit & Integration Test Suite | Develop JUnit 5 test cases validating approval transitions, version increments, and audit events. |

---

## 5. System Architecture

### 5.1 Three-Tier Architecture Diagram (Mermaid)

```mermaid
graph TD
    subgraph ClientLayer ["Client Layer (Presentation)"]
        UI["Modern Web Interface\n(HTML5 / CSS3 / Vanilla JS Fetch)"]
        BrowserTest["Selenium WebDriver\nAutomated Test Suite"]
    end

    subgraph ServerLayer ["Application Server Layer (Apache Tomcat)"]
        REST["Spring Boot REST API Controllers\n(/api/documents, /api/health)"]
        Val["Validation & Exception Handler Layer"]
        Service["Business Logic & Workflow Engine\n(DocumentService, AuditService)"]
        StateMachine["Controlled State Machine\n(DRAFT -> PENDING -> APPROVED -> RELEASED)"]
    end

    subgraph DataLayer ["Data & Storage Layer"]
        Repo["Thread-Safe In-Memory / H2 Data Store\n(ConcurrentHashMap / JPA Repository)"]
        AuditStore["Immutable Audit Log Store"]
    end

    subgraph DevOpsLayer ["DevOps & CI/CD Pipeline"]
        GitRepo["Git / GitHub Repository"]
        Jenkins["Jenkins CI/CD Automation Server"]
        Maven["Apache Maven 3.9+ Build Tool"]
        Docker["Docker Containerization Engine"]
        Ansible["Ansible / Puppet Configuration Management"]
    end

    UI -->|RESTful JSON Requests| REST
    BrowserTest -->|E2E Test Execution| UI
    REST --> Val
    Val --> Service
    Service --> StateMachine
    StateMachine --> Repo
    Service --> AuditStore

    GitRepo -->|Webhook / Polling| Jenkins
    Jenkins -->|Compile & Package| Maven
    Maven -->|Run Tests| BrowserTest
    Jenkins -->|Build & Tag| Docker
    Docker -->|Container Deployment| ServerLayer
    Ansible -->|Environment Provisioning| ServerLayer
```

---

## 6. Use-Case Diagram

```mermaid
graph LR
    actorAuthor((Author / Originator))
    actorReviewer((Reviewer / Approver))
    actorAuditor((QA / Compliance Auditor))
    actorDevOps((DevOps Engineer))

    subgraph SystemBoundary ["Automated Controlled Document Version Approval System"]
        UC1["Create New Document Draft"]
        UC2["Submit Draft for Approval"]
        UC3["Create Minor/Major Version Revision"]
        UC4["View Approval Queue"]
        UC5["Approve Version with Comments"]
        UC6["Reject Version with Reason"]
        UC7["Track Document Status & History"]
        UC8["Inspect Immutable Audit Trail"]
        UC9["Check System Health / Metrics"]
        UC10["Trigger Automated CI/CD Pipeline"]
    end

    actorAuthor --> UC1
    actorAuthor --> UC2
    actorAuthor --> UC3
    actorAuthor --> UC7

    actorReviewer --> UC4
    actorReviewer --> UC5
    actorReviewer --> UC6
    actorReviewer --> UC7

    actorAuditor --> UC7
    actorAuditor --> UC8

    actorDevOps --> UC9
    actorDevOps --> UC10
```

---

## 7. Data Model & Entity Relationship

```mermaid
erDiagram
    DOCUMENT ||--o{ DOCUMENT_VERSION : contains
    DOCUMENT ||--o{ AUDIT_LOG : generates
    DOCUMENT_VERSION ||--o| APPROVAL_REQUEST : undergoes

    DOCUMENT {
        string id PK "UUID"
        string docNumber UK "DOC-2026-XXXX"
        string title "Document Title"
        string category "SOP | Policy | Spec | Manual"
        string currentVersion "e.g. 1.0, 1.1, 2.0"
        string status "DRAFT | PENDING_APPROVAL | APPROVED | REJECTED | RELEASED"
        string author "Originator Name/Email"
        timestamp createdAt "Creation Timestamp"
        timestamp updatedAt "Last Modified Timestamp"
    }

    DOCUMENT_VERSION {
        string versionId PK "UUID"
        string documentId FK "UUID"
        string versionNumber "1.0, 1.1, 2.0"
        string summary "Change summary / Release notes"
        string content "Document body text"
        string changeType "MAJOR | MINOR"
        string author "Version Author"
        timestamp createdDate "Submission Timestamp"
    }

    APPROVAL_REQUEST {
        string requestId PK "UUID"
        string versionId FK "UUID"
        string reviewer "Designated Approver"
        string decision "APPROVED | REJECTED"
        string comments "Reviewer remarks"
        timestamp decisionDate "Approval Timestamp"
    }

    AUDIT_LOG {
        string logId PK "UUID"
        string documentId FK "UUID"
        string action "CREATED | SUBMITTED | APPROVED | REJECTED | VERSION_INCREMENTED"
        string actor "Username / System"
        string details "Human-readable event description"
        timestamp timestamp "ISO-8601 Timestamp"
    }
```

---

## 8. State Transition Lifecycle (Document Versioning)

```mermaid
stateDiagram-v2
    [*] --> DRAFT : Author drafts document (v1.0)
    DRAFT --> PENDING_APPROVAL : Author submits for approval
    PENDING_APPROVAL --> APPROVED : Reviewer approves with remarks
    PENDING_APPROVAL --> REJECTED : Reviewer rejects with feedback
    REJECTED --> DRAFT : Author revises content
    APPROVED --> RELEASED : Released into production
    RELEASED --> PENDING_APPROVAL : Author submits Minor revision (e.g. v1.1)
    RELEASED --> PENDING_APPROVAL : Author submits Major overhaul (e.g. v2.0)
```
