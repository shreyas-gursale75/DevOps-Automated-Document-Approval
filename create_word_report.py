import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_full_report():
    doc = docx.Document()

    # Page Margins: 1 inch on all sides
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Palette
    COLOR_PRIMARY = RGBColor(15, 23, 42)      # Deep Navy
    COLOR_SECONDARY = RGBColor(14, 116, 144)  # Deep Cyan/Teal
    COLOR_BODY = RGBColor(51, 65, 85)         # Slate Gray
    COLOR_MUTED = RGBColor(100, 116, 139)

    def set_cell_background(cell, hex_color):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def format_paragraph(p, space_before=0, space_after=6, line_spacing=1.15):
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing

    def add_custom_heading(text, level, space_before=12, space_after=4):
        p = doc.add_paragraph()
        format_paragraph(p, space_before, space_after)
        run = p.add_run(text)
        run.bold = True
        if level == 1:
            run.font.size = Pt(17)
            run.font.color.rgb = COLOR_PRIMARY
            # Add bottom border / rule under major headings
            pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="2" w:color="0E7490"/></w:pBdr>')
            p._p.get_or_add_pPr().append(pBdr)
        elif level == 2:
            run.font.size = Pt(13)
            run.font.color.rgb = COLOR_SECONDARY
        elif level == 3:
            run.font.size = Pt(11.5)
            run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_bullet(p, bold_prefix, text):
        p.paragraph_format.left_indent = Inches(0.25)
        format_paragraph(p, 0, 4, 1.15)
        run_b = p.add_run(f"•  {bold_prefix}: ")
        run_b.bold = True
        run_b.font.size = Pt(10.5)
        run_b.font.color.rgb = COLOR_PRIMARY
        
        run_t = p.add_run(text)
        run_t.font.size = Pt(10.5)
        run_t.font.color.rgb = COLOR_BODY

    # =========================================================================
    # HEADER / STUDENT METADATA (Above project title)
    # =========================================================================
    p_meta = doc.add_paragraph()
    format_paragraph(p_meta, 0, 8)
    run_meta = p_meta.add_run("Name: Shreyas Gursale   |   Roll no: 23102C0061   |   DevOps Engineering Project")
    run_meta.bold = True
    run_meta.font.size = Pt(11)
    run_meta.font.color.rgb = COLOR_SECONDARY

    # Divider
    p_div = doc.add_paragraph()
    format_paragraph(p_div, 0, 14)
    run_div = p_div.add_run("―" * 68)
    run_div.font.size = Pt(10)
    run_div.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # PROJECT TITLE & SUBTITLE
    # =========================================================================
    p_title = doc.add_paragraph()
    format_paragraph(p_title, 0, 4)
    run_title = p_title.add_run("Automated Controlled Document Version Approval System")
    run_title.bold = True
    run_title.font.size = Pt(22)
    run_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, 0, 16)
    run_sub = p_sub.add_run("Production-Grade CI/CD Delivery Pipeline with Jenkins, Docker, Private Registry & Selenium Acceptance Gates")
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = COLOR_SECONDARY

    # =========================================================================
    # 1. EXECUTIVE SUMMARY & OBJECTIVE
    # =========================================================================
    add_custom_heading("1. Executive Summary & Objective", 1)
    p_exec = doc.add_paragraph()
    format_paragraph(p_exec, 0, 8)
    r = p_exec.add_run(
        "In strictly regulated domains such as healthcare, pharmaceuticals, defense, and enterprise engineering, "
        "uncontrolled document modification presents severe legal, regulatory, and operational risks. Standard Operating "
        "Procedures (SOPs), clinical protocols, and security compliance policies mandate verified author attribution, "
        "mandatory reviewer decision gates, semantic revision numbering, and non-repudiable audit histories.\n\n"
        "This project delivers an enterprise Automated Controlled Document Version Approval System integrated with a "
        "complete, production-grade DevOps lifecycle. The solution eliminates manual deployment bottlenecks by automating "
        "code compilation, JUnit unit testing, executable JAR packaging, Docker containerization with an Alpine JRE base, "
        "publishing to an enterprise local private registry (localhost:5000), container deployment, and end-to-end "
        "browser acceptance testing using headless Selenium WebDriver."
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    # =========================================================================
    # 2. PROBLEM STATEMENT & REGULATORY CONTEXT
    # =========================================================================
    add_custom_heading("2. Problem Statement & Regulatory Context", 1)
    p_prob = doc.add_paragraph()
    format_paragraph(p_prob, 0, 6)
    r = p_prob.add_run(
        "Organizations subject to FDA 21 CFR Part 11, ISO 9001, and GxP standards face severe non-compliance penalties "
        "when operating with manual or ad-hoc document workflows. The primary pain points addressed by this project include:"
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    p1 = doc.add_paragraph()
    add_bullet(p1, "Lack of Version Control", "Manual edits without strict semantic version tagging cause dangerous version drift between departments.")
    p2 = doc.add_paragraph()
    add_bullet(p2, "Audit Trail Deficiencies", "Paper or file-share systems lack immutable logging of actor identities, timestamps, and reviewer rationales.")
    p3 = doc.add_paragraph()
    add_bullet(p3, "Deployment Downtime & Drift", "Manual server installations lead to environment inconsistencies ('works on my machine') and service disruption.")
    p4 = doc.add_paragraph()
    add_bullet(p4, "Absence of Automated Verification", "Deployments without automated browser quality gates allow broken UI workflows to reach production staff.")

    # =========================================================================
    # 3. SYSTEM ARCHITECTURE & END-TO-END TECH STACK
    # =========================================================================
    add_custom_heading("3. System Architecture & End-to-End Technology Stack", 1)
    p_arch = doc.add_paragraph()
    format_paragraph(p_arch, 0, 8)
    r = p_arch.add_run(
        "The application is engineered as a cloud-ready 3-tier microservice backed by an automated DevOps delivery toolchain:"
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    # Tech Stack Table
    table = doc.add_table(rows=7, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Architecture Layer", "Technology / Tool", "Specific Role in System"]
    widths = [Inches(1.8), Inches(2.0), Inches(2.7)]

    # Style Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        hdr_cells[i].width = widths[i]
        set_cell_background(hdr_cells[i], "0F172A")
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ("Backend Framework", "Java 17 (Temurin) & Spring Boot 3.2.5", "Core REST controllers, service state machine, Jakarta Validation, and embedded Tomcat 10."),
        ("Frontend Client", "HTML5, Vanilla CSS3 & Modern JS", "Glassmorphic responsive dark dashboard, debounced instant search, and live health metrics."),
        ("Build & Compilation", "Apache Maven 3.9.9", "Dependency resolution, bytecode compilation, Surefire test runner, and fat JAR packaging."),
        ("CI/CD Orchestration", "Jenkins 2.580 LTS", "Two-tier automation: Freestyle continuous integration job and Declarative release pipeline."),
        ("Container Engine", "Docker 29 & Alpine JRE 17", "Lightweight immutable packaging (~345MB), non-root execution, and health probe monitoring."),
        ("Artifact Registry", "Local Private Docker Registry v2", "Secure internal repository on port 5000 for versioned immutable image distribution (:v2, :latest).")
    ]

    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = cell_value
            row_cells[col_idx].width = widths[col_idx]
            p = row_cells[col_idx].paragraphs[0]
            format_paragraph(p, 2, 2)
            p.runs[0].font.size = Pt(9)
            p.runs[0].font.color.rgb = COLOR_BODY
            if row_idx % 2 == 1:
                set_cell_background(row_cells[col_idx], "F8FAFC")

    # =========================================================================
    # 4. CONTROLLED DOCUMENT LIFECYCLE & AUDIT TRAIL
    # =========================================================================
    add_custom_heading("4. Controlled Document Lifecycle & Audit Trail", 1)
    p_lc = doc.add_paragraph()
    format_paragraph(p_lc, 0, 6)
    r = p_lc.add_run(
        "The system enforces a strict 4-phase state machine ensuring no document can reach the RELEASED state without "
        "passing formal review and recording a tamper-evident audit log:"
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    p_s1 = doc.add_paragraph()
    add_bullet(p_s1, "1. DRAFT State", "Created by an author with initial semantic version 1.0. The document remains editable only by the author. A DOCUMENT_CREATED audit event is logged.")
    p_s2 = doc.add_paragraph()
    add_bullet(p_s2, "2. PENDING_APPROVAL State", "Author submits draft for formal review. Content is automatically locked against further edits. A DOCUMENT_SUBMITTED audit event is logged.")
    p_s3 = doc.add_paragraph()
    add_bullet(p_s3, "3. APPROVED State", "Authorized reviewer (e.g. Lead QA) evaluates the document, provides mandatory justification remarks, and grants sign-off. A DOCUMENT_APPROVED audit event is logged.")
    p_s4 = doc.add_paragraph()
    add_bullet(p_s4, "4. RELEASED State", "Document is made active organization-wide. Subsequent revisions force a semantic version increment (v1.1 for minor revisions, v2.0 for major updates). A DOCUMENT_RELEASED audit event is logged.")

    # =========================================================================
    # 5. TWO-TIER JENKINS PIPELINE ARCHITECTURE
    # =========================================================================
    add_custom_heading("5. Two-Tier Jenkins Pipeline Architecture", 1)
    p_j = doc.add_paragraph()
    format_paragraph(p_j, 0, 6)
    r = p_j.add_run(
        "To separate concerns between rapid developer feedback and production release promotion, the system employs two specialized Jenkins jobs:"
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    p_j1 = doc.add_paragraph()
    add_bullet(p_j1, "Job 1: Document-Approval-CI (Freestyle Project)", 
               "Runs automatically on a 15-minute scheduled cron (H/15 * * * *) and on code commits. "
               "Executes pre-build port cleanup, compiles code, runs unit tests (DocumentApprovalApplicationTests), "
               "packages the JAR, and archives the artifact in ~15 seconds. Guarantees broken code is caught immediately.")
    
    p_j2 = doc.add_paragraph()
    add_bullet(p_j2, "Job 2: Document-Approval-Pipeline (Declarative Pipeline)", 
               "Triggered on releases via versioned Jenkinsfile. Executes a full 7-stage delivery lifecycle: "
               "Git sync, unit testing, packaging, multi-tag Docker build, pushing to the local private registry (:5000), "
               "container deployment, and automated Selenium acceptance testing in ~2 minutes 50 seconds.")

    # =========================================================================
    # 6. DETAILED 7-STAGE CI/CD PIPELINE BREAKDOWN
    # =========================================================================
    add_custom_heading("6. Detailed 7-Stage End-to-End CI/CD Pipeline", 1)
    p_p7 = doc.add_paragraph()
    format_paragraph(p_p7, 0, 6)
    r = p_p7.add_run(
        "The Declarative Jenkinsfile pipeline coordinates 7 fully automated stages from source checkout to acceptance verification:"
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    stages_detail = [
        ("Stage 1: Checkout", "Synchronizes workspace from local Git repository, verifying commit hash and working tree integrity."),
        ("Stage 2: Build & Unit Tests", "Invokes Maven Surefire to run JUnit 5 unit tests (DocumentApprovalApplicationTests), validating business logic before packaging."),
        ("Stage 3: Package Artefact", "Executes 'mvn package -DskipTests', produces automated-document-approval-1.0.0.jar, and records cryptographic fingerprints."),
        ("Stage 4: Docker Image Build & Tagging", "Builds multi-tagged Docker images using Alpine JRE 17: 'automated-document-approval:v2', ':latest', and registry tags."),
        ("Stage 5: Registry Publish", "Executes 'docker push' to upload the immutable versioned image to the local private registry at localhost:5000."),
        ("Stage 6: Continuous Deployment", "Gracefully stops obsolete containers, frees host port 8080, and launches a fresh container instance from the private registry."),
        ("Stage 7: Automated Acceptance Tests (Selenium)", "Performs HTTP liveness checks on /api/health, boots headless Google Chrome, and executes 5 critical user journeys with UI screenshot archiving.")
    ]

    for st_title, st_desc in stages_detail:
        p_st = doc.add_paragraph()
        add_bullet(p_st, st_title, st_desc)

    # =========================================================================
    # 7. DOCKER CONTAINERIZATION & PRIVATE REGISTRY ARCHITECTURE
    # =========================================================================
    add_custom_heading("7. Docker Containerization & Private Registry Architecture", 1)
    p_dk = doc.add_paragraph()
    format_paragraph(p_dk, 0, 6)
    r = p_dk.add_run(
        "The application Docker container is built following enterprise security and efficiency standards:"
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    p_dk1 = doc.add_paragraph()
    add_bullet(p_dk1, "Minimal Attack Surface", "Based on eclipse-temurin:17-jre-alpine, producing a compact image (~345MB) with only required runtime dependencies.")
    p_dk2 = doc.add_paragraph()
    add_bullet(p_dk2, "Security Compliance (Non-Root User)", "Enforces least-privilege security by creating and executing under an unprivileged user (appuser:appgroup) instead of root.")
    p_dk3 = doc.add_paragraph()
    add_bullet(p_dk3, "Embedded Container Healthcheck", "Includes HEALTHCHECK --interval=15s --timeout=5s CMD wget --spider http://localhost:8080/api/health to enable continuous runtime self-monitoring.")
    p_dk4 = doc.add_paragraph()
    add_bullet(p_dk4, "Local Private Docker Registry", "Operates a dedicated registry:2 container on port 5000, isolating proprietary artifacts from public registries while supporting instant rollbacks.")

    # =========================================================================
    # 8. AUTOMATED QUALITY GATES: SELENIUM ACCEPTANCE TESTING
    # =========================================================================
    add_custom_heading("8. Automated Quality Gates: Selenium Acceptance Testing", 1)
    p_sel = doc.add_paragraph()
    format_paragraph(p_sel, 0, 6)
    r = p_sel.add_run(
        "Unit tests only validate isolated Java methods; Selenium WebDriver validates the complete user experience against the running container. "
        "The suite automatically tests 5 critical user journeys (CUJ) and archives screenshot proofs into Jenkins:"
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    cuj_list = [
        ("Journey 1 (Dashboard Load & Health)", "Verifies the web interface loads, backend server is reported UP, and statistics counters populate correctly."),
        ("Journey 2 (Create New Controlled Draft)", "Fills document metadata form, selects category (SOP/Policy), and validates the created draft in the document table."),
        ("Journey 3 (Submit Draft for Review)", "Clicks Submit for Review, confirms state transition to PENDING_APPROVAL, and verifies author edit locking."),
        ("Journey 4 (Formal Review & Sign-Off)", "Opens review decision gate modal, enters reviewer remarks, approves document, and confirms transition to RELEASED."),
        ("Journey 5 (Search & Filter Navigation)", "Exercises instant debounced search bar and verifies real-time filtering across SOP, Policy, and Specification category tabs.")
    ]

    for cuj_title, cuj_desc in cuj_list:
        p_c = doc.add_paragraph()
        add_bullet(p_c, cuj_title, cuj_desc)

    # =========================================================================
    # 9. DEVOPS RELIABILITY & REAL-WORLD TROUBLESHOOTING
    # =========================================================================
    add_custom_heading("9. DevOps Reliability & Real-World Troubleshooting", 1)
    p_tr = doc.add_paragraph()
    format_paragraph(p_tr, 0, 6)
    r = p_tr.add_run(
        "A critical engineering challenge encountered during CI pipeline execution was Windows file locking. "
        "When the Spring Boot application was actively running on port 8080, Windows prevented 'mvn clean' from deleting "
        "the locked file target/automated-document-approval-1.0.0.jar, causing Build #54 to fail.\n\n"
        "To achieve self-healing, automated resilience without human intervention, an automated pre-build process cleanup hook was "
        "engineered and embedded directly into the Jenkins CI job configuration:"
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    p_code = doc.add_paragraph()
    format_paragraph(p_code, 4, 6)
    p_code.paragraph_format.left_indent = Inches(0.4)
    r_code = p_code.add_run(
        "for /f \"tokens=5\" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1 || ver >nul"
    )
    r_code.font.name = "Consolas"
    r_code.font.size = Pt(9.5)
    r_code.bold = True
    r_code.font.color.rgb = COLOR_SECONDARY

    p_tr_res = doc.add_paragraph()
    format_paragraph(p_tr_res, 0, 8)
    r = p_tr_res.add_run(
        "With this automated self-healing hook in place, every subsequent build (Builds #55 through #61) completed with status SUCCESS (blue), "
        "guaranteeing reliable unattended continuous integration on Windows host environments."
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    # =========================================================================
    # 10. CONCLUSION & OPERATIONAL IMPACT
    # =========================================================================
    add_custom_heading("10. Conclusion & Operational Impact", 1)
    p_conc = doc.add_paragraph()
    format_paragraph(p_conc, 0, 8)
    r = p_conc.add_run(
        "The Automated Controlled Document Version Approval System successfully bridges enterprise regulatory compliance "
        "with modern DevOps engineering practices. By coupling state machine compliance logic with two-tier Jenkins automation, "
        "immutable Docker packaging, private registry distribution, and automated Selenium quality gates, the project delivers:\n"
        "• 100% elimination of unapproved document releases reaching production.\n"
        "• Sub-3-minute commit-to-deployment cycle with zero manual intervention.\n"
        "• Complete non-repudiable audit trails for GxP and ISO 9001 audit readiness.\n"
        "• Instant rollback capability through immutable, versioned container images."
    )
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_BODY

    # Save to both paths
    path1 = os.path.abspath("DevOps_Project_Report.docx")
    path2 = os.path.abspath("DevOps_Project_Report_Shreyas_Gursale.docx")
    doc.save(path1)
    doc.save(path2)
    print(f"Word Document successfully saved to:\n  1. {path1}\n  2. {path2}")

create_full_report()
