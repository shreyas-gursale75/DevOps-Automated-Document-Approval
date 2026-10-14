package com.devops.documentapproval.repository;

import com.devops.documentapproval.model.ApprovalStatus;
import com.devops.documentapproval.model.ChangeType;
import com.devops.documentapproval.model.Document;
import com.devops.documentapproval.model.DocumentVersion;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

@Repository
public class DocumentRepository {
    private final Map<String, Document> storage = new ConcurrentHashMap<>();
    private final AtomicInteger sequence = new AtomicInteger(1000);

    public DocumentRepository() {
        seedSampleData();
    }

    public Document save(Document document) {
        if (document.getId() == null) {
            document.setId(UUID.randomUUID().toString());
        }
        if (document.getDocNumber() == null) {
            document.setDocNumber("DOC-2026-" + sequence.incrementAndGet());
        }
        document.setUpdatedAt(Instant.now());
        storage.put(document.getId(), document);
        return document;
    }

    public Optional<Document> findById(String id) {
        return Optional.ofNullable(storage.get(id));
    }

    public List<Document> findAll() {
        return storage.values().stream()
                .sorted(Comparator.comparing(Document::getCreatedAt).reversed())
                .collect(Collectors.toList());
    }

    public List<Document> findByStatus(ApprovalStatus status) {
        return storage.values().stream()
                .filter(d -> d.getStatus() == status)
                .sorted(Comparator.comparing(Document::getCreatedAt).reversed())
                .collect(Collectors.toList());
    }

    public List<Document> search(String query) {
        if (query == null || query.isBlank()) {
            return findAll();
        }
        String q = query.toLowerCase().trim();
        return storage.values().stream()
                .filter(d -> (d.getTitle() != null && d.getTitle().toLowerCase().contains(q)) ||
                             (d.getDocNumber() != null && d.getDocNumber().toLowerCase().contains(q)) ||
                             (d.getCategory() != null && d.getCategory().toLowerCase().contains(q)) ||
                             (d.getAuthor() != null && d.getAuthor().toLowerCase().contains(q)))
                .sorted(Comparator.comparing(Document::getCreatedAt).reversed())
                .collect(Collectors.toList());
    }

    public long count() {
        return storage.size();
    }

    public long countByStatus(ApprovalStatus status) {
        return storage.values().stream().filter(d -> d.getStatus() == status).count();
    }

    private void seedSampleData() {
        // Document 1: Approved and Released SOP
        Document doc1 = new Document(
                "DOC-2026-1001",
                "Standard Operating Procedure for Production Deployment",
                "SOP",
                "Dr. Aris Thorne",
                "Baseline SOP for containerized microservice deployments",
                "All production deployments must follow continuous integration tests in Jenkins and Docker image signing."
        );
        doc1.setStatus(ApprovalStatus.RELEASED);
        doc1.setReviewer("Marcus Vance (Lead QA)");
        doc1.setReviewerComments("Verified complete test matrix and Jenkinsfile. Approved for global release.");
        doc1.addAuditLog("DOCUMENT_SUBMITTED", "Dr. Aris Thorne", "Draft submitted for formal QA review.");
        doc1.addAuditLog("DOCUMENT_APPROVED", "Marcus Vance (Lead QA)", "Approved for release. Remarks: Passed all compliance checks.");
        doc1.addAuditLog("DOCUMENT_RELEASED", "Marcus Vance (Lead QA)", "Official release into organization document index.");
        storage.put(doc1.getId(), doc1);

        // Document 2: Pending Approval Document
        Document doc2 = new Document(
                "DOC-2026-1002",
                "Cloud Infrastructure Data Residency and Encryption Policy",
                "Policy",
                "Elena Rostova",
                "Mandatory data-at-rest encryption standards using AES-256-GCM",
                "All customer PII and financial records stored across cloud regions must utilize HSM-backed encryption keys."
        );
        doc2.setStatus(ApprovalStatus.PENDING_APPROVAL);
        doc2.addAuditLog("DOCUMENT_SUBMITTED", "Elena Rostova", "Draft submitted for Security Committee sign-off.");
        storage.put(doc2.getId(), doc2);

        // Document 3: Draft Specification with version revision
        Document doc3 = new Document(
                "DOC-2026-1003",
                "Automated Document Approval System Technical Architecture Specification",
                "Specification",
                "Shreyas Gursale",
                "Architecture overview for Java 17, Spring Boot, Tomcat and Docker pipeline",
                "System incorporates 3-tier architecture, append-only audit trail, and semantic version branching."
        );
        doc3.setStatus(ApprovalStatus.DRAFT);
        storage.put(doc3.getId(), doc3);
    }
}
