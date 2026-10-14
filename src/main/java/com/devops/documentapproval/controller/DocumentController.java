package com.devops.documentapproval.controller;

import com.devops.documentapproval.dto.ApprovalRequestDto;
import com.devops.documentapproval.dto.CreateDocumentRequest;
import com.devops.documentapproval.dto.CreateVersionRequest;
import com.devops.documentapproval.model.ApprovalStatus;
import com.devops.documentapproval.model.Document;
import com.devops.documentapproval.service.DocumentService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/documents")
@CrossOrigin(origins = "*")
public class DocumentController {

    private final DocumentService documentService;

    public DocumentController(DocumentService documentService) {
        this.documentService = documentService;
    }

    @GetMapping
    public ResponseEntity<List<Document>> getAllDocuments(
            @RequestParam(required = false) ApprovalStatus status,
            @RequestParam(required = false) String query) {
        return ResponseEntity.ok(documentService.getAllDocuments(status, query));
    }

    @GetMapping("/{id}")
    public ResponseEntity<Document> getDocumentById(@PathVariable String id) {
        return ResponseEntity.ok(documentService.getDocumentById(id));
    }

    @PostMapping
    public ResponseEntity<Document> createDocument(@Valid @RequestBody CreateDocumentRequest request) {
        Document created = documentService.createDocument(request);
        return new ResponseEntity<>(created, HttpStatus.CREATED);
    }

    @PostMapping("/{id}/submit")
    public ResponseEntity<Document> submitForApproval(
            @PathVariable String id,
            @RequestBody(required = false) Map<String, String> body) {
        String actor = (body != null) ? body.get("actor") : null;
        Document submitted = documentService.submitForApproval(id, actor);
        return ResponseEntity.ok(submitted);
    }

    @PostMapping("/{id}/approve")
    public ResponseEntity<Document> approveDocument(
            @PathVariable String id,
            @Valid @RequestBody ApprovalRequestDto approvalRequest) {
        Document approved = documentService.approveDocument(id, approvalRequest);
        return ResponseEntity.ok(approved);
    }

    @PostMapping("/{id}/reject")
    public ResponseEntity<Document> rejectDocument(
            @PathVariable String id,
            @Valid @RequestBody ApprovalRequestDto approvalRequest) {
        Document rejected = documentService.rejectDocument(id, approvalRequest);
        return ResponseEntity.ok(rejected);
    }

    @PostMapping("/{id}/release")
    public ResponseEntity<Document> releaseDocument(
            @PathVariable String id,
            @RequestBody(required = false) Map<String, String> body) {
        String actor = (body != null) ? body.get("actor") : null;
        Document released = documentService.releaseDocument(id, actor);
        return ResponseEntity.ok(released);
    }

    @PostMapping("/{id}/versions")
    public ResponseEntity<Document> createNewVersion(
            @PathVariable String id,
            @Valid @RequestBody CreateVersionRequest request) {
        Document updated = documentService.createNewVersion(id, request);
        return new ResponseEntity<>(updated, HttpStatus.CREATED);
    }
}
