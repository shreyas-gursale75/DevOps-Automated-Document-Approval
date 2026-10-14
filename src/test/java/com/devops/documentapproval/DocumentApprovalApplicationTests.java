package com.devops.documentapproval;

import com.devops.documentapproval.dto.ApprovalRequestDto;
import com.devops.documentapproval.dto.CreateDocumentRequest;
import com.devops.documentapproval.dto.CreateVersionRequest;
import com.devops.documentapproval.model.ApprovalStatus;
import com.devops.documentapproval.model.ChangeType;
import com.devops.documentapproval.model.Document;
import com.devops.documentapproval.service.DocumentService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class DocumentApprovalApplicationTests {

    @Autowired
    private DocumentService documentService;

    @Test
    @DisplayName("Test 1: Context loads successfully")
    void contextLoads() {
        assertNotNull(documentService, "DocumentService should be wired into application context");
    }

    @Test
    @DisplayName("Test 2: Create new document draft with initial version 1.0")
    void testCreateDocumentDraft() {
        CreateDocumentRequest req = new CreateDocumentRequest();
        req.setTitle("CI/CD Pipeline Security Architecture");
        req.setCategory("Specification");
        req.setAuthor("DevOps Engineer");
        req.setSummary("Initial security baseline for Jenkins runners");
        req.setContent("All runner containers must execute in isolated network namespaces.");

        Document doc = documentService.createDocument(req);
        assertNotNull(doc.getId(), "Document ID should be generated");
        assertNotNull(doc.getDocNumber(), "Document Number should be generated");
        assertEquals("1.0", doc.getCurrentVersion(), "Initial version should be 1.0");
        assertEquals(ApprovalStatus.DRAFT, doc.getStatus(), "Initial status should be DRAFT");
        assertEquals(1, doc.getVersions().size(), "Should have exactly 1 version record");
        assertEquals(1, doc.getAuditLogs().size(), "Should have initial creation audit log");
    }

    @Test
    @DisplayName("Test 3: Full Approval Lifecycle (Draft -> Pending -> Approved -> Released)")
    void testApprovalLifecycle() {
        // 1. Create
        CreateDocumentRequest req = new CreateDocumentRequest();
        req.setTitle("Disaster Recovery and Backup Policy");
        req.setCategory("Policy");
        req.setAuthor("Sara Connor");
        req.setSummary("Daily offsite encrypted snapshots");
        req.setContent("Snapshots are taken daily at 00:00 UTC and replicated across regions.");

        Document doc = documentService.createDocument(req);

        // 2. Submit for approval
        Document submitted = documentService.submitForApproval(doc.getId(), "Sara Connor");
        assertEquals(ApprovalStatus.PENDING_APPROVAL, submitted.getStatus());

        // 3. Approve
        ApprovalRequestDto approval = new ApprovalRequestDto();
        approval.setReviewer("Auditor John");
        approval.setComments("RPO and RTO meet business continuity SLA. Approved.");

        Document approved = documentService.approveDocument(doc.getId(), approval);
        assertEquals(ApprovalStatus.APPROVED, approved.getStatus());
        assertEquals("Auditor John", approved.getReviewer());
        assertEquals("RPO and RTO meet business continuity SLA. Approved.", approved.getReviewerComments());

        // 4. Release
        Document released = documentService.releaseDocument(doc.getId(), "Operations Lead");
        assertEquals(ApprovalStatus.RELEASED, released.getStatus());

        // 5. Verify Audit Trail completeness
        assertTrue(released.getAuditLogs().size() >= 4, "Should have audit logs for create, submit, approve, release");
    }

    @Test
    @DisplayName("Test 4: Rejection Workflow with Feedback Comments")
    void testRejectionWorkflow() {
        CreateDocumentRequest req = new CreateDocumentRequest();
        req.setTitle("Container Registry Access Control");
        req.setCategory("SOP");
        req.setAuthor("Alex Mercer");
        req.setSummary("Registry permissions");
        req.setContent("Public anonymous pull access is permitted.");

        Document doc = documentService.createDocument(req);
        documentService.submitForApproval(doc.getId(), "Alex Mercer");

        ApprovalRequestDto rejection = new ApprovalRequestDto();
        rejection.setReviewer("Security Lead");
        rejection.setComments("Rejected: Public anonymous pulls violate zero-trust architecture.");

        Document rejected = documentService.rejectDocument(doc.getId(), rejection);
        assertEquals(ApprovalStatus.REJECTED, rejected.getStatus());
        assertEquals("Security Lead", rejected.getReviewer());
    }

    @Test
    @DisplayName("Test 5: Semantic Versioning Increments (Minor: 1.0 -> 1.1, Major: 1.1 -> 2.0)")
    void testSemanticVersioning() {
        CreateDocumentRequest req = new CreateDocumentRequest();
        req.setTitle("Software Release Guideline");
        req.setCategory("Manual");
        req.setAuthor("Release Team");
        req.setSummary("Initial release");
        req.setContent("Version 1 content");

        Document doc = documentService.createDocument(req);
        assertEquals("1.0", doc.getCurrentVersion());

        // Minor revision
        CreateVersionRequest minorReq = new CreateVersionRequest();
        minorReq.setChangeType(ChangeType.MINOR);
        minorReq.setAuthor("Release Team");
        minorReq.setSummary("Minor typo fix in section 2");
        minorReq.setContent("Version 1.1 content with fix");

        Document minorDoc = documentService.createNewVersion(doc.getId(), minorReq);
        assertEquals("1.1", minorDoc.getCurrentVersion());
        assertEquals(ApprovalStatus.PENDING_APPROVAL, minorDoc.getStatus());
        assertEquals(2, minorDoc.getVersions().size());

        // Major revision
        CreateVersionRequest majorReq = new CreateVersionRequest();
        majorReq.setChangeType(ChangeType.MAJOR);
        majorReq.setAuthor("Lead Architect");
        majorReq.setSummary("Major migration to Kubernetes native orchestrations");
        majorReq.setContent("Version 2.0 complete rewrite");

        Document majorDoc = documentService.createNewVersion(doc.getId(), majorReq);
        assertEquals("2.0", majorDoc.getCurrentVersion());
        assertEquals(ApprovalStatus.PENDING_APPROVAL, majorDoc.getStatus());
        assertEquals(3, majorDoc.getVersions().size());
    }

    @Test
    @DisplayName("Test 6: Guard against illegal state transition (Cannot approve DRAFT directly)")
    void testIllegalStateTransitionGuard() {
        CreateDocumentRequest req = new CreateDocumentRequest();
        req.setTitle("Network Segmentation Standard");
        req.setCategory("Policy");
        req.setAuthor("NetAdmin");
        req.setSummary("VLAN configs");
        req.setContent("VLAN segmentation rules");

        Document doc = documentService.createDocument(req);
        assertEquals(ApprovalStatus.DRAFT, doc.getStatus());

        ApprovalRequestDto approval = new ApprovalRequestDto();
        approval.setReviewer("CISO");
        approval.setComments("Direct approval attempt");

        assertThrows(IllegalStateException.class, () -> {
            documentService.approveDocument(doc.getId(), approval);
        }, "Should throw IllegalStateException when approving a document in DRAFT status");
    }
}
