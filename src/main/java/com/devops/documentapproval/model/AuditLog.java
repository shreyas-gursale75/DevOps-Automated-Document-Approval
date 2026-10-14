package com.devops.documentapproval.model;

import java.time.Instant;
import java.util.UUID;

public class AuditLog {
    private String logId;
    private String action;
    private String actor;
    private String details;
    private Instant timestamp;

    public AuditLog() {
        this.logId = UUID.randomUUID().toString();
        this.timestamp = Instant.now();
    }

    public AuditLog(String action, String actor, String details) {
        this.logId = UUID.randomUUID().toString();
        this.action = action;
        this.actor = actor;
        this.details = details;
        this.timestamp = Instant.now();
    }

    public String getLogId() {
        return logId;
    }

    public void setLogId(String logId) {
        this.logId = logId;
    }

    public String getAction() {
        return action;
    }

    public void setAction(String action) {
        this.action = action;
    }

    public String getActor() {
        return actor;
    }

    public void setActor(String actor) {
        this.actor = actor;
    }

    public String getDetails() {
        return details;
    }

    public void setDetails(String details) {
        this.details = details;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Instant timestamp) {
        this.timestamp = timestamp;
    }
}
