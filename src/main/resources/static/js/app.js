/**
 * Automated Controlled Document Version Approval System
 * Frontend Client Controller
 */

document.addEventListener('DOMContentLoaded', () => {
    // State
    let currentFilter = '';
    let searchQuery = '';
    let documents = [];
    let selectedDoc = null;

    // DOM Elements
    const documentTableBody = document.getElementById('documentTableBody');
    const searchInput = document.getElementById('searchInput');
    const statusFilterGroup = document.getElementById('statusFilterGroup');

    // Metrics elements
    const metricTotalDocs = document.getElementById('metricTotalDocs');
    const metricPendingDocs = document.getElementById('metricPendingDocs');
    const metricApprovedDocs = document.getElementById('metricApprovedDocs');
    const healthStatusText = document.getElementById('healthStatusText');
    const systemHealthBadge = document.getElementById('systemHealthBadge');

    // Modals
    const modalCreateDoc = document.getElementById('modalCreateDoc');
    const modalReviewDoc = document.getElementById('modalReviewDoc');
    const modalDocDetails = document.getElementById('modalDocDetails');
    const modalNewVersion = document.getElementById('modalNewVersion');

    // Forms
    const formCreateDoc = document.getElementById('formCreateDoc');
    const formReviewDoc = document.getElementById('formReviewDoc');
    const formNewVersion = document.getElementById('formNewVersion');

    // Review Modal Elements
    const reviewDocId = document.getElementById('reviewDocId');
    const reviewDocSummary = document.getElementById('reviewDocSummary');
    const reviewerName = document.getElementById('reviewerName');
    const reviewerComments = document.getElementById('reviewerComments');
    const btnApproveDecision = document.getElementById('btnApproveDecision');
    const btnRejectDecision = document.getElementById('btnRejectDecision');

    // Document Details Elements
    const detailsDocTitle = document.getElementById('detailsDocTitle');
    const detailsDocNumber = document.getElementById('detailsDocNumber');
    const versionTimelineContainer = document.getElementById('versionTimelineContainer');
    const auditLogContainer = document.getElementById('auditLogContainer');
    const contentPreviewBox = document.getElementById('contentPreviewBox');
    const btnOpenNewVersionModal = document.getElementById('btnOpenNewVersionModal');

    // Setup Event Listeners
    initEventListeners();

    // Initial Data Fetch
    fetchDocuments();
    fetchHealth();
    setInterval(fetchHealth, 15000);

    function initEventListeners() {
        // Open Create Modal
        document.getElementById('btnOpenNewDocModal').addEventListener('click', () => {
            openModal(modalCreateDoc);
        });

        // Close Modals on click of [data-close]
        document.querySelectorAll('[data-close]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const targetId = btn.getAttribute('data-close');
                closeModal(document.getElementById(targetId));
            });
        });

        // Close modal clicking outside card
        document.querySelectorAll('.modal-backdrop').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    closeModal(modal);
                }
            });
        });

        // Search Input with debounce
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                searchQuery = e.target.value.trim();
                fetchDocuments();
            }, 300);
        });

        // Status Filter Tabs
        statusFilterGroup.querySelectorAll('.filter-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                statusFilterGroup.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentFilter = tab.getAttribute('data-status');
                fetchDocuments();
            });
        });

        // Tab Switching in Document Details Modal
        document.querySelectorAll('.details-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.details-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.details-tab-pane').forEach(p => p.classList.remove('active'));

                tab.classList.add('active');
                const targetPane = document.getElementById(tab.getAttribute('data-tab'));
                if (targetPane) targetPane.classList.add('active');
            });
        });

        // Create New Document Form Submit
        formCreateDoc.addEventListener('submit', async (e) => {
            e.preventDefault();
            const payload = {
                title: document.getElementById('docTitle').value.trim(),
                category: document.getElementById('docCategory').value,
                author: document.getElementById('docAuthor').value.trim(),
                summary: document.getElementById('docSummary').value.trim(),
                content: document.getElementById('docContent').value.trim()
            };

            try {
                const res = await fetch('/api/documents', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.message || 'Failed to create document');
                }

                showToast('Controlled document draft created successfully (v1.0)', 'success');
                formCreateDoc.reset();
                closeModal(modalCreateDoc);
                fetchDocuments();
                fetchHealth();
            } catch (err) {
                showToast(err.message, 'error');
            }
        });

        // Approve Action in Review Modal
        btnApproveDecision.addEventListener('click', async () => {
            await handleReviewDecision('approve');
        });

        // Reject Action in Review Modal
        btnRejectDecision.addEventListener('click', async () => {
            await handleReviewDecision('reject');
        });

        // Open New Version Modal from Details Modal
        btnOpenNewVersionModal.addEventListener('click', () => {
            if (!selectedDoc) return;
            document.getElementById('newVersionDocId').value = selectedDoc.id;
            openModal(modalNewVersion);
        });

        // Submit New Version Revision Form
        formNewVersion.addEventListener('submit', async (e) => {
            e.preventDefault();
            const docId = document.getElementById('newVersionDocId').value;
            const changeType = document.querySelector('input[name="versionChangeType"]:checked').value;
            const payload = {
                changeType: changeType,
                author: document.getElementById('newVersionAuthor').value.trim(),
                summary: document.getElementById('newVersionSummary').value.trim(),
                content: document.getElementById('newVersionContent').value.trim()
            };

            try {
                const res = await fetch(`/api/documents/${docId}/versions`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.message || 'Failed to submit revision');
                }

                const updatedDoc = await res.json();
                showToast(`New revision ${updatedDoc.currentVersion} created and submitted for approval!`, 'success');
                formNewVersion.reset();
                closeModal(modalNewVersion);
                closeModal(modalDocDetails);
                fetchDocuments();
                fetchHealth();
            } catch (err) {
                showToast(err.message, 'error');
            }
        });
    }

    // Fetch Documents List
    async function fetchDocuments() {
        let url = '/api/documents?';
        const params = new URLSearchParams();
        if (currentFilter) params.append('status', currentFilter);
        if (searchQuery) params.append('query', searchQuery);

        try {
            const res = await fetch(url + params.toString());
            if (!res.ok) throw new Error('Failed to retrieve documents');
            documents = await res.json();
            renderDocumentTable(documents);
        } catch (err) {
            documentTableBody.innerHTML = `<tr><td colspan="7" class="loading-cell" style="color:var(--red);">Error loading documents: ${err.message}</td></tr>`;
        }
    }

    // Render Table
    function renderDocumentTable(docs) {
        if (!docs || docs.length === 0) {
            documentTableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="loading-cell">
                        No controlled documents match your current filter criteria.
                    </td>
                </tr>`;
            return;
        }

        documentTableBody.innerHTML = docs.map(doc => {
            const updatedDate = new Date(doc.updatedAt).toLocaleString('en-US', {
                month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
            });

            return `
                <tr>
                    <td><span class="mono-badge">${escapeHtml(doc.docNumber || 'DOC-NEW')}</span></td>
                    <td>
                        <div class="doc-title-cell">
                            <span class="doc-title-text">${escapeHtml(doc.title)}</span>
                            <span class="category-tag">${escapeHtml(doc.category)}</span>
                        </div>
                    </td>
                    <td>${escapeHtml(doc.author)}</td>
                    <td><span class="version-pill">v${escapeHtml(doc.currentVersion)}</span></td>
                    <td>${getStatusBadge(doc.status)}</td>
                    <td style="color:var(--text-muted); font-size:0.8rem;">${updatedDate}</td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn btn-secondary btn-sm" onclick="window.viewDocDetails('${doc.id}')">View</button>
                            ${getActionButtons(doc)}
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }

    // Dynamic Action Buttons per Document Status
    function getActionButtons(doc) {
        if (doc.status === 'DRAFT' || doc.status === 'REJECTED') {
            return `<button class="btn btn-primary btn-sm" onclick="window.submitDoc('${doc.id}')">Submit for Review</button>`;
        } else if (doc.status === 'PENDING_APPROVAL') {
            return `<button class="btn btn-success btn-sm" onclick="window.openReviewModal('${doc.id}')">Review Gate</button>`;
        } else if (doc.status === 'APPROVED') {
            return `<button class="btn btn-success btn-sm" onclick="window.releaseDoc('${doc.id}')">Release to Prod</button>`;
        } else if (doc.status === 'RELEASED') {
            return `<button class="btn btn-secondary btn-sm" onclick="window.prepareNewVersion('${doc.id}')">+ Revise</button>`;
        }
        return '';
    }

    // Status Badge Component
    function getStatusBadge(status) {
        switch (status) {
            case 'DRAFT':
                return '<span class="status-badge badge-draft">Draft</span>';
            case 'PENDING_APPROVAL':
                return '<span class="status-badge badge-pending">Pending Review</span>';
            case 'APPROVED':
                return '<span class="status-badge badge-approved">Approved</span>';
            case 'REJECTED':
                return '<span class="status-badge badge-rejected">Rejected</span>';
            case 'RELEASED':
                return '<span class="status-badge badge-released">Released</span>';
            default:
                return `<span class="status-badge">${status}</span>`;
        }
    }

    // Review Decision (Approve / Reject)
    async function handleReviewDecision(type) {
        const id = reviewDocId.value;
        const reviewer = reviewerName.value.trim();
        const comments = reviewerComments.value.trim();

        if (!reviewer) {
            showToast('Reviewer name is required', 'error');
            return;
        }
        if (!comments) {
            showToast('Comments/Remarks are required for review decisions', 'error');
            return;
        }

        const endpoint = `/api/documents/${id}/${type}`;
        try {
            const res = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ reviewer, comments })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.message || `Failed to ${type} document`);
            }

            showToast(`Document version successfully ${type === 'approve' ? 'approved' : 'rejected'}!`, 'success');
            closeModal(modalReviewDoc);
            formReviewDoc.reset();
            fetchDocuments();
            fetchHealth();
        } catch (err) {
            showToast(err.message, 'error');
        }
    }

    // Health & Metrics Poller
    async function fetchHealth() {
        try {
            const res = await fetch('/api/health');
            if (res.ok) {
                const data = await res.json();
                metricTotalDocs.textContent = data.metrics.totalDocuments || '0';
                metricPendingDocs.textContent = data.metrics.pendingApprovals || '0';
                metricApprovedDocs.textContent = (data.metrics.approvedDocuments + data.metrics.releasedDocuments) || '0';
                healthStatusText.textContent = `Tomcat 10 : ${data.status}`;
                systemHealthBadge.classList.remove('offline');
            }
        } catch (e) {
            healthStatusText.textContent = 'Tomcat : Offline';
            systemHealthBadge.classList.add('offline');
        }
    }

    // Window helpers for table actions
    window.submitDoc = async function(id) {
        try {
            const res = await fetch(`/api/documents/${id}/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ actor: 'Document Author' })
            });
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.message || 'Failed to submit document');
            }
            showToast('Document submitted into the review approval queue', 'success');
            fetchDocuments();
            fetchHealth();
        } catch (err) {
            showToast(err.message, 'error');
        }
    };

    window.openReviewModal = function(id) {
        const doc = documents.find(d => d.id === id);
        if (!doc) return;

        reviewDocId.value = doc.id;
        reviewDocSummary.innerHTML = `
            <h4>${escapeHtml(doc.title)} (v${escapeHtml(doc.currentVersion)})</h4>
            <p><strong>Category:</strong> ${escapeHtml(doc.category)} | <strong>Author:</strong> ${escapeHtml(doc.author)}</p>
            <p style="margin-top:0.4rem; color:#cbd5e1;"><strong>Latest Summary:</strong> ${escapeHtml(doc.versions && doc.versions.length > 0 ? doc.versions[doc.versions.length - 1].summary : 'N/A')}</p>
        `;
        openModal(modalReviewDoc);
    };

    window.releaseDoc = async function(id) {
        try {
            const res = await fetch(`/api/documents/${id}/release`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ actor: 'Release Lead' })
            });
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.message || 'Failed to release document');
            }
            showToast('Document released to production!', 'success');
            fetchDocuments();
            fetchHealth();
        } catch (err) {
            showToast(err.message, 'error');
        }
    };

    window.viewDocDetails = function(id) {
        const doc = documents.find(d => d.id === id);
        if (!doc) return;
        selectedDoc = doc;

        detailsDocTitle.textContent = doc.title;
        detailsDocNumber.textContent = `${doc.docNumber} | v${doc.currentVersion} (${doc.status})`;

        // Render Version Timeline
        if (doc.versions && doc.versions.length > 0) {
            versionTimelineContainer.innerHTML = doc.versions.slice().reverse().map(ver => `
                <div class="timeline-item">
                    <div class="timeline-header">
                        <span class="timeline-title">Version ${escapeHtml(ver.versionNumber)} (${ver.changeType})</span>
                        <span class="timeline-date">${new Date(ver.createdAt).toLocaleString()}</span>
                    </div>
                    <p class="timeline-desc"><strong>Author:</strong> ${escapeHtml(ver.author)}</p>
                    <p class="timeline-desc" style="margin-top:0.25rem;"><strong>Summary:</strong> ${escapeHtml(ver.summary)}</p>
                </div>
            `).join('');

            // Content preview of latest version
            const latestVer = doc.versions[doc.versions.length - 1];
            contentPreviewBox.textContent = latestVer.content || 'No content recorded.';
        } else {
            versionTimelineContainer.innerHTML = '<p style="color:var(--text-muted);">No version history available.</p>';
            contentPreviewBox.textContent = 'No content available.';
        }

        // Render Audit Logs
        if (doc.auditLogs && doc.auditLogs.length > 0) {
            auditLogContainer.innerHTML = doc.auditLogs.slice().reverse().map(log => `
                <div class="audit-item">
                    <div class="audit-header">
                        <span class="mono-badge" style="font-size:0.75rem;">${escapeHtml(log.action)}</span>
                        <span class="audit-time">${new Date(log.timestamp).toLocaleString()}</span>
                    </div>
                    <p class="audit-details"><strong>Actor:</strong> ${escapeHtml(log.actor)}</p>
                    <p class="audit-details" style="margin-top:0.2rem;">${escapeHtml(log.details)}</p>
                </div>
            `).join('');
        } else {
            auditLogContainer.innerHTML = '<p style="color:var(--text-muted);">No audit events recorded.</p>';
        }

        openModal(modalDocDetails);
    };

    window.prepareNewVersion = function(id) {
        selectedDoc = documents.find(d => d.id === id);
        if (!selectedDoc) return;
        document.getElementById('newVersionDocId').value = selectedDoc.id;
        openModal(modalNewVersion);
    };

    // Modal Utility Functions
    function openModal(modal) {
        if (!modal) return;
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
    }

    function closeModal(modal) {
        if (!modal) return;
        modal.classList.remove('open');
        document.body.style.overflow = '';
    }

    // Toast Function
    function showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
