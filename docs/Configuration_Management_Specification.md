# Server Configuration Management Specification

**Project:** Automated Controlled Document Version Approval System  
**Document Code:** CMS-2026-SPEC-01  
**Author:** DevOps & Site Reliability Engineering Team  
**Scope:** Target Node Infrastructure Requirements & Configuration Baseline  

---

## 1. Executive Summary

This document specifies the exact environment prerequisites, operating system configurations, directory topologies, user security boundaries, service configurations, and network policies required to provision, deploy, and maintain the **Automated Controlled Document Version Approval System**.

The target node is managed using **Ansible** declarative configuration automation, ensuring repeatable, automated, and idempotent infrastructure provisioning across development, staging, and production environments.

---

## 2. Server Prerequisites Matrix

| Dimension | Specification | Verification Command / Target |
|---|---|---|
| **Operating System** | Linux (Alpine Linux 3.19+, Ubuntu 22.04 LTS+, RHEL 9+) or Windows Server / Container Host | `uname -a` or `cat /etc/os-release` |
| **Java Runtime** | OpenJDK 17 LTS / Eclipse Temurin 17 JRE | `java -version` (Version: `17.0.x`) |
| **Network & Ports** | HTTP Port `8080` (App), Registry `5000` (Docker registry), Jenkins `8085` | `netstat -tlpn` or `ss -tulpn` |
| **Security Service User** | `appuser` (System account, non-login shell `/sbin/nologin`) | `id appuser` (`uid >= 1000`, `gid >= 1000`) |
| **Security Group** | `appgroup` | `getent group appgroup` |
| **Application Directory** | `/opt/devops-app` (Permissions `0755`, Owner: `appuser:appgroup`) | `ls -ld /opt/devops-app` |
| **Log Directory** | `/opt/devops-app/logs` (Permissions `0755`) | `ls -ld /opt/devops-app/logs` |
| **Backup Directory** | `/opt/devops-app/backups` (Permissions `0750`) | `ls -ld /opt/devops-app/backups` |
| **System Utilities** | `curl`, `wget`, `bash`, `python3` (for telemetry and health probing) | `which curl wget bash python3` |

---

## 3. Directory Layout Topology

The target deployment host maintains the following directory structure:

```
/opt/devops-app/
├── automated-document-approval.jar   # Current active Spring Boot release JAR
├── application.properties            # Externalized configuration overrides (optional)
├── current_version.txt               # Semantic version marker (e.g., v1.0.0)
├── logs/
│   ├── app.log                       # Standard output / application log stream
│   └── gc.log                        # Garbage collection logging (when enabled)
└── backups/
    ├── automated-document-approval-v1.0.0.jar  # Stable release archive for rollback
    └── rollback_manifest.json                  # Rollback target metadata
```

---

## 4. User and Privilege Separation Architecture

In accordance with the **Principle of Least Privilege (PoLP)** and CIS Benchmark guidelines:
1. The application **must never run as root**.
2. A dedicated system service account `appuser` is created without interactive shell access (`/sbin/nologin` or `/bin/false`).
3. File ownership of all executable artifacts and runtime directories is assigned strictly to `appuser:appgroup`.
4. The service binds to unprivileged port `8080`, removing the need for elevated network capabilities (`CAP_NET_BIND_SERVICE`).

---

## 5. Network and Port Configuration

| Port | Protocol | Direction | Source | Purpose |
|---|---|---|---|---|
| `8080` | TCP | Inbound | Load Balancer / Reverse Proxy / Clients | Web UI Dashboard & REST API Endpoints |
| `5000` | TCP | Inbound / Internal | CI/CD Pipeline Agent | Local Docker Image Registry |
| `8085` | TCP | Inbound | DevOps Engineers & Webhooks | Jenkins Automation Server |

---

## 6. Service Lifecycle & Health Probing Protocol

The service lifecycle follows automated state transitions:
1. **Startup:** `java -Djava.security.egd=file:/dev/./urandom -Dserver.port=8080 -jar /opt/devops-app/automated-document-approval.jar`
2. **Readiness Probe:** HTTP GET request to `http://localhost:8080/api/health`
3. **Response Schema Requirements:**
   - HTTP Status: `200 OK`
   - Payload `status`: `"UP"`
   - Memory and metric fields present
4. **Failure Behavior:** If probe fails after 6 retries (30 seconds total elapsed), the automation triggers alert logging and initiates the automated rollback procedure.

---

## 7. Configuration Management Tool Selection: Ansible

Ansible was chosen as the configuration management engine because:
- **Agentless Architecture:** Operates over standard SSH or local connection without agent daemon overhead.
- **Declarative Idempotency:** State descriptions ensure rerun consistency without drift.
- **YAML Readability:** Auditable and version-controlled alongside application code.
