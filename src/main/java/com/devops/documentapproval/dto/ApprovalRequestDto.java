package com.devops.documentapproval.dto;

import jakarta.validation.constraints.NotBlank;

public class ApprovalRequestDto {
    @NotBlank(message = "Reviewer name/ID is required")
    private String reviewer;

    @NotBlank(message = "Comments/Remarks are required for review decisions")
    private String comments;

    public String getReviewer() {
        return reviewer;
    }

    public void setReviewer(String reviewer) {
        this.reviewer = reviewer;
    }

    public String getComments() {
        return comments;
    }

    public void setComments(String comments) {
        this.comments = comments;
    }
}
