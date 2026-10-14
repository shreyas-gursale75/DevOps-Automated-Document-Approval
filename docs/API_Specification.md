# RESTful API Specification
## Project: Automated Controlled Document Version Approval System

Base URL: `http://localhost:8080/api`

---

## 1. Document Management Endpoints

### 1.1 List All Documents
- **Method:** `GET`
- **Path:** `/api/documents`
- **Query Parameters (Optional):**
  - `status`: Filter by status (`DRAFT`, `PENDING_APPROVAL`, `APPROVED`, `REJECTED`, `RELEASED`)
  - `query`: Text search in title, docNumber, or author
- **Response:** `200 OK`
```json
[
  {
    "id": "e4b2f150-1c6e-4c7b-b5ea-7a13c9883bf1",
    "docNumber": "DOC-2026-1001",
    "title": "Standard Operating Procedure for Production Deployment",
    "category": "SOP",
    "currentVersion": "1.0",
    "status": "APPROVED",
    "author": "Dr. Aris Thorne",
    "createdAt": "2026-10-14T09:00:00Z",
    "updatedAt": "2026-10-14T09:15:00Z",
    "versionsCount": 1
  }
]
```

---

### 1.2 Get Document By ID
- **Method:** `GET`
- **Path:** `/api/documents/{id}`
- **Response:** `200 OK`
```json
{
  "id": "e4b2f150-1c6e-4c7b-b5ea-7a13c9883bf1",
  "docNumber": "DOC-2026-1001",
  "title": "Standard Operating Procedure for Production Deployment",
  "category": "SOP",
  "currentVersion": "1.0",
  "status": "APPROVED",
  "author": "Dr. Aris Thorne",
  "createdAt": "2026-10-14T09:00:00Z",
  "updatedAt": "2026-10-14T09:15:00Z",
  "versions": [
    {
      "versionId": "v101",
      "versionNumber": "1.0",
      "summary": "Initial baseline draft for CI/CD SOP",
      "content": "All deployments must pass Jenkins automated tests before containerization.",
      "changeType": "MAJOR",
      "author": "Dr. Aris Thorne",
      "createdDate": "2026-10-14T09:00:00Z"
    }
  ],
  "auditLogs": [
    {
      "logId": "log-01",
      "action": "DOCUMENT_CREATED",
      "actor": "Dr. Aris Thorne",
      "details": "Document created with initial version 1.0",
      "timestamp": "2026-10-14T09:00:00Z"
    }
  ]
}
```

---

### 1.3 Create New Document Draft
- **Method:** `POST`
- **Path:** `/api/documents`
- **Request Body:**
```json
{
  "title": "Data Governance Policy 2026",
  "category": "Policy",
  "author": "Elena Rostova",
  "summary": "Initial policy draft for data residency and encryption",
  "content": "Encryption at rest using AES-256 is mandatory across all databases."
}
```
- **Response:** `201 Created`
```json
{
  "id": "7bfa8812-4d2a-4318-8f81-591b6e414c22",
  "docNumber": "DOC-2026-1002",
  "title": "Data Governance Policy 2026",
  "category": "Policy",
  "currentVersion": "1.0",
  "status": "DRAFT",
  "author": "Elena Rostova",
  "createdAt": "2026-10-14T09:20:00Z"
}
```

---

## 2. Approval Workflow Endpoints

### 2.1 Submit Document for Approval
- **Method:** `POST`
- **Path:** `/api/documents/{id}/submit`
- **Response:** `200 OK`
```json
{
  "id": "7bfa8812-4d2a-4318-8f81-591b6e414c22",
  "status": "PENDING_APPROVAL",
  "message": "Document successfully submitted for review."
}
```

---

### 2.2 Approve Document Version
- **Method:** `POST`
- **Path:** `/api/documents/{id}/approve`
- **Request Body:**
```json
{
  "reviewer": "Marcus Vance (QA Director)",
  "comments": "Verified compliance with ISO-27001 standards. Approved."
}
```
- **Response:** `200 OK`
```json
{
  "id": "7bfa8812-4d2a-4318-8f81-591b6e414c22",
  "status": "APPROVED",
  "currentVersion": "1.0",
  "message": "Document version approved."
}
```

---

### 2.3 Reject Document Version
- **Method:** `POST`
- **Path:** `/api/documents/{id}/reject`
- **Request Body:**
```json
{
  "reviewer": "Marcus Vance (QA Director)",
  "comments": "Mandatory TLS 1.3 requirement is missing in Section 3."
}
```
- **Response:** `200 OK`
```json
{
  "id": "7bfa8812-4d2a-4318-8f81-591b6e414c22",
  "status": "REJECTED",
  "message": "Document version rejected with feedback."
}
```

---

### 2.4 Release Approved Document
- **Method:** `POST`
- **Path:** `/api/documents/{id}/release`
- **Response:** `200 OK`
```json
{
  "id": "7bfa8812-4d2a-4318-8f81-591b6e414c22",
  "status": "RELEASED",
  "message": "Document officially released for organization use."
}
```

---

### 2.5 Submit New Version Revision (Semantic Versioning)
- **Method:** `POST`
- **Path:** `/api/documents/{id}/versions`
- **Request Body:**
```json
{
  "changeType": "MINOR", // or "MAJOR"
  "author": "Elena Rostova",
  "summary": "Added Section 3: Mandated TLS 1.3 protocol",
  "content": "All external API gateways must enforce TLS 1.3 cipher suites."
}
```
- **Response:** `201 Created`
```json
{
  "id": "7bfa8812-4d2a-4318-8f81-591b6e414c22",
  "currentVersion": "1.1",
  "status": "PENDING_APPROVAL",
  "message": "New minor revision 1.1 created and submitted for approval."
}
```

---

## 3. DevOps & Monitoring Endpoints

### 3.1 System Health & Uptime Probe
- **Method:** `GET`
- **Path:** `/api/health`
- **Response:** `200 OK`
```json
{
  "status": "UP",
  "service": "Automated Controlled Document Version Approval System",
  "timestamp": "2026-10-14T09:30:00Z",
  "runtime": "Java 17 (Amazon Corretto) on Apache Tomcat",
  "totalDocuments": 12,
  "pendingApprovals": 2,
  "memoryUsedMB": 48,
  "memoryMaxMB": 512
}
```
