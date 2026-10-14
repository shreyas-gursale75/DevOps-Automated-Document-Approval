package com.devops.documentapproval.controller;

import com.devops.documentapproval.model.ApprovalStatus;
import com.devops.documentapproval.service.DocumentService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/health")
@CrossOrigin(origins = "*")
public class HealthController {

    private final DocumentService documentService;
    private final Instant startTime = Instant.now();

    public HealthController(DocumentService documentService) {
        this.documentService = documentService;
    }

    @GetMapping
    public ResponseEntity<Map<String, Object>> getHealth() {
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory() / (1024 * 1024);
        long freeMemory = runtime.freeMemory() / (1024 * 1024);
        long usedMemory = totalMemory - freeMemory;

        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("service", "Automated Controlled Document Version Approval System");
        health.put("server", "Apache Tomcat / Spring Boot 3.2.5");
        health.put("javaVersion", System.getProperty("java.version"));
        health.put("startedAt", startTime.toString());
        health.put("currentTime", Instant.now().toString());

        Map<String, Object> stats = new HashMap<>();
        stats.put("totalDocuments", documentService.getTotalCount());
        stats.put("pendingApprovals", documentService.getCountByStatus(ApprovalStatus.PENDING_APPROVAL));
        stats.put("approvedDocuments", documentService.getCountByStatus(ApprovalStatus.APPROVED));
        stats.put("releasedDocuments", documentService.getCountByStatus(ApprovalStatus.RELEASED));
        health.put("metrics", stats);

        Map<String, Object> memory = new HashMap<>();
        memory.put("usedMemoryMB", usedMemory);
        memory.put("totalMemoryMB", totalMemory);
        health.put("memory", memory);

        return ResponseEntity.ok(health);
    }
}
