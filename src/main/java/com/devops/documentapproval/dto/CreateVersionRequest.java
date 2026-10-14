package com.devops.documentapproval.dto;

import com.devops.documentapproval.model.ChangeType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class CreateVersionRequest {
    @NotNull(message = "Change type (MINOR or MAJOR) is required")
    private ChangeType changeType;

    @NotBlank(message = "Author name is required")
    private String author;

    @NotBlank(message = "Summary of changes is required")
    private String summary;

    @NotBlank(message = "Document content cannot be blank")
    private String content;

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
}
