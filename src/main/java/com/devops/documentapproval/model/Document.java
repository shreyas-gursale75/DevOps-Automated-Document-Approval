package com.devops.documentapproval.model;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class Document {
    private String id;
    private String docNumber;
    private String title;
    private String category;
    private String currentVersion;
    private ApprovalStatus status;
    private String author;
    private String reviewer;
    private String reviewerComments;
    private Instant createdAt;
    private Instant updatedAt;
    private List<DocumentVersion> versions = new ArrayList<>();
    private List<AuditLog> auditLogs = new ArrayList<>();

    public Document() {
        this.id = UUID.randomUUID().toString();
        this.status = ApprovalStatus.DRAFT;
        this.currentVersion = "1.0";
        this.createdAt = Instant.now();
        this.updatedAt = Instant.now();
    }

    public Document(String docNumber, String title, String category, String author, String summary, String content) {
        this.id = UUID.randomUUID().toString();
        this.docNumber = docNumber;
        this.title = title;
        this.category = category;
        this.author = author;
        this.status = ApprovalStatus.DRAFT;
        this.currentVersion = "1.0";
        this.createdAt = Instant.now();
        this.updatedAt = Instant.now();

        DocumentVersion initialVersion = new DocumentVersion("1.0", summary, content, ChangeType.INITIAL, author);
        this.versions.add(initialVersion);

        AuditLog initialAudit = new AuditLog("DOCUMENT_CREATED", author, "Initial document created in DRAFT state with version 1.0");
        this.auditLogs.add(initialAudit);
    }

    public void addAuditLog(String action, String actor, String details) {
        this.auditLogs.add(new AuditLog(action, actor, details));
        this.updatedAt = Instant.now();
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getDocNumber() {
        return docNumber;
    }

    public void setDocNumber(String docNumber) {
        this.docNumber = docNumber;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getCurrentVersion() {
        return currentVersion;
    }

    public void setCurrentVersion(String currentVersion) {
        this.currentVersion = currentVersion;
    }

    public ApprovalStatus getStatus() {
        return status;
    }

    public void setStatus(ApprovalStatus status) {
        this.status = status;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getReviewer() {
        return reviewer;
    }

    public void setReviewer(String reviewer) {
        this.reviewer = reviewer;
    }

    public String getReviewerComments() {
        return reviewerComments;
    }

    public void setReviewerComments(String reviewerComments) {
        this.reviewerComments = reviewerComments;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Instant updatedAt) {
        this.updatedAt = updatedAt;
    }

    public List<DocumentVersion> getVersions() {
        return versions;
    }

    public void setVersions(List<DocumentVersion> versions) {
        this.versions = versions;
    }

    public List<AuditLog> getAuditLogs() {
        return auditLogs;
    }

    public void setAuditLogs(List<AuditLog> auditLogs) {
        this.auditLogs = auditLogs;
    }
}
