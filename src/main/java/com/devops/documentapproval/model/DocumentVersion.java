package com.devops.documentapproval.model;

import java.time.Instant;
import java.util.UUID;

public class DocumentVersion {
    private String versionId;
    private String versionNumber;
    private String summary;
    private String content;
    private ChangeType changeType;
    private String author;
    private Instant createdAt;

    public DocumentVersion() {
        this.versionId = UUID.randomUUID().toString();
        this.createdAt = Instant.now();
    }

    public DocumentVersion(String versionNumber, String summary, String content, ChangeType changeType, String author) {
        this.versionId = UUID.randomUUID().toString();
        this.versionNumber = versionNumber;
        this.summary = summary;
        this.content = content;
        this.changeType = changeType;
        this.author = author;
        this.createdAt = Instant.now();
    }

    public String getVersionId() {
        return versionId;
    }

    public void setVersionId(String versionId) {
        this.versionId = versionId;
    }

    public String getVersionNumber() {
        return versionNumber;
    }

    public void setVersionNumber(String versionNumber) {
        this.versionNumber = versionNumber;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public ChangeType getChangeType() {
        return changeType;
    }

    public void setChangeType(ChangeType changeType) {
        this.changeType = changeType;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }
}
