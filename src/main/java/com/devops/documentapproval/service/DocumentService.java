package com.devops.documentapproval.service;

import com.devops.documentapproval.dto.ApprovalRequestDto;
import com.devops.documentapproval.dto.CreateDocumentRequest;
import com.devops.documentapproval.dto.CreateVersionRequest;
import com.devops.documentapproval.model.ApprovalStatus;
import com.devops.documentapproval.model.ChangeType;
import com.devops.documentapproval.model.Document;
import com.devops.documentapproval.model.DocumentVersion;
import com.devops.documentapproval.repository.DocumentRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.NoSuchElementException;

@Service
public class DocumentService {
    private final DocumentRepository documentRepository;

    public DocumentService(DocumentRepository documentRepository) {
        this.documentRepository = documentRepository;
    }

    public List<Document> getAllDocuments(ApprovalStatus status, String query) {
        if (query != null && !query.isBlank()) {
            return documentRepository.search(query);
        }
        if (status != null) {
            return documentRepository.findByStatus(status);
        }
        return documentRepository.findAll();
    }

    public Document getDocumentById(String id) {
        return documentRepository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Document not found with ID: " + id));
    }

    public Document createDocument(CreateDocumentRequest request) {
        Document document = new Document(
                null,
                request.getTitle().trim(),
                request.getCategory().trim(),
                request.getAuthor().trim(),
                request.getSummary().trim(),
                request.getContent().trim()
        );
        return documentRepository.save(document);
    }

    public Document submitForApproval(String id, String actor) {
        Document document = getDocumentById(id);
        if (document.getStatus() != ApprovalStatus.DRAFT && document.getStatus() != ApprovalStatus.REJECTED) {
            throw new IllegalStateException("Only DRAFT or REJECTED documents can be submitted for approval. Current status: " + document.getStatus());
        }

        document.setStatus(ApprovalStatus.PENDING_APPROVAL);
        String submitter = (actor != null && !actor.isBlank()) ? actor : document.getAuthor();
        document.addAuditLog("DOCUMENT_SUBMITTED", submitter, "Document version " + document.getCurrentVersion() + " submitted for review.");
        return documentRepository.save(document);
    }

    public Document approveDocument(String id, ApprovalRequestDto approvalRequest) {
        Document document = getDocumentById(id);
        if (document.getStatus() != ApprovalStatus.PENDING_APPROVAL) {
            throw new IllegalStateException("Only documents in PENDING_APPROVAL status can be approved. Current status: " + document.getStatus());
        }

        document.setStatus(ApprovalStatus.APPROVED);
        document.setReviewer(approvalRequest.getReviewer());
        document.setReviewerComments(approvalRequest.getComments());

        document.addAuditLog(
                "DOCUMENT_APPROVED",
                approvalRequest.getReviewer(),
                "Approved version " + document.getCurrentVersion() + ". Remarks: " + approvalRequest.getComments()
        );
        return documentRepository.save(document);
    }

    public Document rejectDocument(String id, ApprovalRequestDto approvalRequest) {
        Document document = getDocumentById(id);
        if (document.getStatus() != ApprovalStatus.PENDING_APPROVAL) {
            throw new IllegalStateException("Only documents in PENDING_APPROVAL status can be rejected. Current status: " + document.getStatus());
        }

        document.setStatus(ApprovalStatus.REJECTED);
        document.setReviewer(approvalRequest.getReviewer());
        document.setReviewerComments(approvalRequest.getComments());

        document.addAuditLog(
                "DOCUMENT_REJECTED",
                approvalRequest.getReviewer(),
                "Rejected version " + document.getCurrentVersion() + ". Reason: " + approvalRequest.getComments()
        );
        return documentRepository.save(document);
    }

    public Document releaseDocument(String id, String actor) {
        Document document = getDocumentById(id);
        if (document.getStatus() != ApprovalStatus.APPROVED) {
            throw new IllegalStateException("Only APPROVED documents can be officially released. Current status: " + document.getStatus());
        }

        document.setStatus(ApprovalStatus.RELEASED);
        String releaser = (actor != null && !actor.isBlank()) ? actor : (document.getReviewer() != null ? document.getReviewer() : "System Admin");
        document.addAuditLog("DOCUMENT_RELEASED", releaser, "Document version " + document.getCurrentVersion() + " officially released for operational use.");
        return documentRepository.save(document);
    }

    public Document createNewVersion(String id, CreateVersionRequest request) {
        Document document = getDocumentById(id);

        String currentVer = document.getCurrentVersion();
        String nextVer = calculateNextVersion(currentVer, request.getChangeType());

        DocumentVersion newVersion = new DocumentVersion(
                nextVer,
                request.getSummary().trim(),
                request.getContent().trim(),
                request.getChangeType(),
                request.getAuthor().trim()
        );

        document.getVersions().add(newVersion);
        document.setCurrentVersion(nextVer);
        document.setStatus(ApprovalStatus.PENDING_APPROVAL);
        document.setReviewer(null);
        document.setReviewerComments(null);

        document.addAuditLog(
                "VERSION_INCREMENTED",
                request.getAuthor(),
                "New " + request.getChangeType() + " revision " + nextVer + " created and routed for review."
        );

        return documentRepository.save(document);
    }

    private String calculateNextVersion(String currentVersion, ChangeType changeType) {
        try {
            String[] parts = currentVersion.split("\\.");
            int major = Integer.parseInt(parts[0]);
            int minor = parts.length > 1 ? Integer.parseInt(parts[1]) : 0;

            if (changeType == ChangeType.MAJOR) {
                return (major + 1) + ".0";
            } else {
                return major + "." + (minor + 1);
            }
        } catch (Exception e) {
            return currentVersion + ".1";
        }
    }

    public long getTotalCount() {
        return documentRepository.count();
    }

    public long getCountByStatus(ApprovalStatus status) {
        return documentRepository.countByStatus(status);
    }
}
