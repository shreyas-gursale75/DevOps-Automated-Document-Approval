import sys
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette - Modern Engineering Dark Theme
    BG_COLOR = RGBColor(15, 23, 42)        # Slate 900
    CARD_BG = RGBColor(30, 41, 59)         # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)     # Slate 700
    TEXT_MAIN = RGBColor(248, 250, 252)    # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)   # Slate 400
    ACCENT_CYAN = RGBColor(56, 189, 248)   # Sky 400
    ACCENT_GREEN = RGBColor(52, 211, 153)  # Emerald 400
    ACCENT_AMBER = RGBColor(251, 191, 36)  # Amber 400
    ACCENT_PURPLE = RGBColor(192, 132, 252)# Purple 400

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="AUTOMATED CONTROLLED DOCUMENT APPROVAL SYSTEM"):
        # Category badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN

        # Footer divider & meta
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.fill.background()

        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.35))
        tf_foot = footer_box.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Shreyas Gursale | Roll No: 23102C0061  •  DevOps Project Presentation"
        p_foot.font.size = Pt(10)
        p_foot.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, items, badge="", accent_color=ACCENT_CYAN):
        # Card background
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Header bar inside card
        header_box = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), Inches(0.45))
        tf_h = header_box.text_frame
        tf_h.word_wrap = True
        p_h = tf_h.paragraphs[0]
        p_h.text = title
        p_h.font.size = Pt(15)
        p_h.font.bold = True
        p_h.font.color.rgb = accent_color

        if badge:
            p_badge = tf_h.add_paragraph()
            p_badge.text = badge.upper()
            p_badge.font.size = Pt(9)
            p_badge.font.bold = True
            p_badge.font.color.rgb = TEXT_MUTED

        # Content bullets
        body_box = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.6), width - Inches(0.3), height - Inches(0.7))
        tf_b = body_box.text_frame
        tf_b.word_wrap = True

        for idx, item in enumerate(items):
            p = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
            p.text = f"•  {item}" if isinstance(item, str) else f"•  {item[0]}: {item[1]}"
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Title Card
    t_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(10.9), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "DEVOPS ENGINEERING & AUTOMATION"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN
    p0.space_after = Pt(10)

    p1 = tf1.add_paragraph()
    p1.text = "Automated Controlled Document\nVersion Approval System"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_MAIN
    p1.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "Production-Grade Multi-Stage CI/CD Pipeline with Jenkins, Docker, Private Registry & Selenium Quality Gates"
    p2.font.size = Pt(16)
    p2.font.color.rgb = TEXT_MUTED

    # Student metadata card
    meta_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.0), Inches(5.3), Inches(2.3))
    meta_card.fill.solid()
    meta_card.fill.fore_color.rgb = CARD_BG
    meta_card.line.color.rgb = ACCENT_CYAN
    meta_card.line.width = Pt(1.5)

    m_box = slide1.shapes.add_textbox(Inches(1.4), Inches(4.15), Inches(4.9), Inches(2.0))
    tf_m = m_box.text_frame
    tf_m.word_wrap = True
    pm0 = tf_m.paragraphs[0]
    pm0.text = "STUDENT & PROJECT METADATA"
    pm0.font.size = Pt(11)
    pm0.font.bold = True
    pm0.font.color.rgb = ACCENT_CYAN
    pm0.space_after = Pt(10)

    pm1 = tf_m.add_paragraph()
    pm1.text = "Student Name: Shreyas Gursale\nRoll No: 23102C0061\nRole: Lead DevOps & Backend Engineer\nDomain: Regulatory GxP / Document Lifecycle Automation"
    pm1.font.size = Pt(13)
    pm1.font.color.rgb = TEXT_MAIN

    # Key Tech Highlights card
    tech_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.0), Inches(5.3), Inches(2.3))
    tech_card.fill.solid()
    tech_card.fill.fore_color.rgb = CARD_BG
    tech_card.line.color.rgb = ACCENT_GREEN
    tech_card.line.width = Pt(1.5)

    t_box2 = slide1.shapes.add_textbox(Inches(7.0), Inches(4.15), Inches(4.9), Inches(2.0))
    tf_t2 = t_box2.text_frame
    tf_t2.word_wrap = True
    pt0 = tf_t2.paragraphs[0]
    pt0.text = "CORE ARCHITECTURAL HIGHLIGHTS"
    pt0.font.size = Pt(11)
    pt0.font.bold = True
    pt0.font.color.rgb = ACCENT_GREEN
    pt0.space_after = Pt(10)

    pt1 = tf_t2.add_paragraph()
    pt1.text = "• Core Framework: Spring Boot 3.2.5 on OpenJDK 17\n• Pipeline Engine: Jenkins LTS (2-Tier CI/CD Architecture)\n• Container Engine: Docker 29 with Local Private Registry (:5000)\n• Quality Gate: Selenium Headless WebDriver with UI Artifacts"
    pt1.font.size = Pt(13)
    pt1.font.color.rgb = TEXT_MAIN

    # -------------------------------------------------------------
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Industry Problem Statement & DevOps Motivation")

    add_card(slide2, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.1),
             "1. Regulatory Challenges",
             ["Regulated domains (FDA 21 CFR Part 11, ISO 9001, GxP) require strict change tracking.",
              "Manual paper or loose document workflows suffer from accidental deletions and lost audit histories.",
              "Lack of tamper-evident digital sign-offs invites regulatory audit failure and compliance fines.",
              "Human error leads to unapproved document releases reaching production teams."],
             "Compliance Bottleneck", ACCENT_AMBER)

    add_card(slide2, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.1),
             "2. The DevOps Deficit",
             ["Traditional document systems rely on manual server deployments and ad-hoc scripting.",
              "Environment drift causes 'works on my machine' errors between development and production.",
              "No automated regression or browser testing before releases go live.",
              "Zero rollback capability if a faulty version is released to users."],
             "Operational Gaps", ACCENT_CYAN)

    add_card(slide2, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.1),
             "3. The Engineered Solution",
             ["Cloud-ready Spring Boot microservice implementing a strict 4-phase approval state machine.",
              "Automated 2-Tier Jenkins pipeline that eliminates manual build and deployment steps.",
              "Immutable Docker containers pushed to a secure enterprise-grade local registry.",
              "Automated Selenium WebDriver quality gates with visual screenshot proof archiving."],
             "Project Scope", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 3: SYSTEM ARCHITECTURE & TECH STACK
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "System Architecture & End-to-End Technology Stack")

    add_card(slide3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1),
             "Core Application Layer (Spring Boot Microservice)",
             ["Backend Framework: Spring Boot 3.2.5 running on OpenJDK 17 LTS.",
              "Embedded Web Server: Apache Tomcat 10.1 with asynchronous servlet handling.",
              "Domain Logic: Document entity management, semantic version branching, and audit trail generation.",
              "RESTful API Endpoints: Health check (/api/health), document CRUD, workflow review gates, and search filters.",
              "Client Interface: Modern reactive dark-mode web dashboard featuring live statistics and category filtering."],
             "Application Tier", ACCENT_CYAN)

    add_card(slide3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1),
             "DevOps & Infrastructure Stack",
             ["Source Control: Git with strict commit history tracking and branch management.",
              "Build Automation: Apache Maven 3.9.9 managing compilation, dependencies, and packaging.",
              "CI/CD Engine: Jenkins 2.580 LTS driving declarative automated pipelines.",
              "Containerization: Docker 29 with Alpine JRE 17 base image (345 MB compact footprint).",
              "Artifact Repository: Local private Docker Registry (localhost:5000) for secure distribution.",
              "Acceptance Testing: Selenium WebDriver with Google Chrome headless browser automation."],
             "Infrastructure Tier", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 4: DOCUMENT STATE MACHINE & AUDIT TRAIL
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Controlled Document Lifecycle & Tamper-Evident Audit Trail")

    add_card(slide4, Inches(0.8), Inches(1.6), Inches(2.7), Inches(5.1),
             "State 1: DRAFT",
             ["Author creates new controlled document (SOP, Policy, Spec).",
              "Assigned unique identifier (e.g. DOC-2026-1003).",
              "Initial baseline semantic version: v1.0.",
              "Audit Log: DOCUMENT_CREATED recorded with actor and timestamp."],
             "Author Phase", ACCENT_CYAN)

    add_card(slide4, Inches(3.8), Inches(1.6), Inches(2.7), Inches(5.1),
             "State 2: PENDING",
             ["Author formally submits draft for committee review.",
              "Document locks: content is made immutable to author edits.",
              "Assigned to designated QA reviewer (e.g., Marcus Vance).",
              "Audit Log: DOCUMENT_SUBMITTED recorded."],
             "Review Phase", ACCENT_AMBER)

    add_card(slide4, Inches(6.8), Inches(1.6), Inches(2.7), Inches(5.1),
             "State 3: APPROVED",
             ["Reviewer performs regulatory compliance checks.",
              "Formal decision gate: Approved with mandatory reviewer comments.",
              "Audit Log: DOCUMENT_APPROVED recorded with sign-off identity.",
              "Eligible for organization-wide release."],
             "Sign-Off Phase", ACCENT_PURPLE)

    add_card(slide4, Inches(9.8), Inches(1.6), Inches(2.7), Inches(5.1),
             "State 4: RELEASED",
             ["Document published to active production inventory.",
              "Visible to all staff; serves as authorized working procedure.",
              "Future modifications force a semantic version bump (v1.1 or v2.0).",
              "Audit Log: DOCUMENT_RELEASED appended."],
             "Production Phase", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 5: TWO-TIER JENKINS ARCHITECTURE
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Two-Tier Jenkins Architecture: Continuous Integration vs Delivery")

    add_card(slide5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1),
             "Job 1: Document-Approval-CI (Continuous Integration)",
             ["Job Type: Freestyle Project with automated polling trigger (H/15 * * * *).",
              "DevOps Purpose: Rapid developer feedback on every code commit.",
              "Execution Time: Fast (~10 to 18 seconds).",
              "Automated Pre-Build Hook: Terminates conflicting host processes on port 8080 to prevent Windows JAR locking.",
              "Lifecycle: mvn clean test-compile surefire:test package -Dtest=DocumentApprovalApplicationTests.",
              "Artifact Archiving: Stores target/*.jar with cryptographic fingerprinting.",
              "Failure Handling: Rejects commits immediately if any unit test fails."],
             "Fast Feedback CI Loop", ACCENT_CYAN)

    add_card(slide5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1),
             "Job 2: Document-Approval-Pipeline (Continuous Delivery)",
             ["Job Type: Declarative Pipeline codified in versioned Jenkinsfile.",
              "DevOps Purpose: Comprehensive end-to-end containerized release gate.",
              "Execution Time: Thorough (~2 min 50 seconds).",
              "7 Automated Stages: From Git sync to Docker publishing and browser acceptance testing.",
              "Infrastructure as Code: Environment, tools (JDK-17, Maven-3.9.9), and deployment ports defined in code.",
              "Acceptance Quality Gate: Runs headless Selenium Chrome journeys and archives screenshots.",
              "Enterprise Distribution: Pushes verified images to private registry localhost:5000."],
             "Full Delivery Release Pipeline", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 6: DETAILED 7-STAGE CI/CD PIPELINE
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "The 7-Stage End-to-End CI/CD Pipeline Workflow")

    stages = [
        ("Stage 1", "Checkout", "Git baseline synchronization; pulls verified source commits and verifies tree integrity."),
        ("Stage 2", "Build & Tests", "Compiles Java 17 bytecode and runs JUnit 5 unit test suite via Maven Surefire plugin."),
        ("Stage 3", "Package Artefact", "Packages fat executable JAR (automated-document-approval-1.0.0.jar) and records fingerprint."),
        ("Stage 4", "Docker Build", "Builds multi-tagged Docker image (v2, latest, registry tag) using Alpine JRE 17 base."),
        ("Stage 5", "Registry Push", "Publishes versioned images to private local registry localhost:5000 for secure distribution."),
        ("Stage 6", "Continuous Deploy", "Safely cleans old containers, frees port 8080, and launches new container in detached mode."),
        ("Stage 7", "Selenium E2E Gate", "Runs live HTTP health probe and executes 5 headless Chrome browser journeys with screenshots.")
    ]

    for idx, (st_num, st_name, st_desc) in enumerate(stages):
        col_w = Inches(1.58)
        left = Inches(0.8 + idx * 1.7)
        top = Inches(1.8)
        height = Inches(4.8)

        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, col_w, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = ACCENT_CYAN if idx < 3 else (ACCENT_AMBER if idx < 6 else ACCENT_GREEN)
        card.line.width = Pt(1.5)

        tbox = slide6.shapes.add_textbox(left + Inches(0.08), top + Inches(0.12), col_w - Inches(0.16), height - Inches(0.24))
        tf = tbox.text_frame
        tf.word_wrap = True

        p_num = tf.paragraphs[0]
        p_num.text = st_num.upper()
        p_num.font.size = Pt(10)
        p_num.font.bold = True
        p_num.font.color.rgb = ACCENT_CYAN if idx < 3 else (ACCENT_AMBER if idx < 6 else ACCENT_GREEN)
        p_num.space_after = Pt(4)

        p_nm = tf.add_paragraph()
        p_nm.text = st_name
        p_nm.font.size = Pt(13)
        p_nm.font.bold = True
        p_nm.font.color.rgb = TEXT_MAIN
        p_nm.space_after = Pt(12)

        p_desc = tf.add_paragraph()
        p_desc.text = st_desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 7: DOCKER CONTAINERIZATION & PRIVATE REGISTRY
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Docker Containerization & Private Registry Architecture")

    add_card(slide7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1),
             "Hardened Production Dockerfile Architecture",
             ["Base Image: eclipse-temurin:17-jre-alpine (lightweight, minimal attack surface, ~345MB).",
              "Security Hardening: Creates and enforces non-root execution via appuser:appgroup.",
              "Port Exposure: Exposes standardized internal application port 8080.",
              "Integrated Healthcheck: Built-in wget spider probe pinging /api/health every 15 seconds.",
              "JVM Optimization: -Djava.security.egd=file:/dev/./urandom enables instantaneous entropy generation on Linux kernels, reducing Tomcat startup to <2 seconds."],
             "Container Hardening", ACCENT_CYAN)

    add_card(slide7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1),
             "Local Private Registry & Image Versioning",
             ["Registry Service: Dedicated devops-registry container running official registry:2 image on port 5000.",
              "Security & Compliance: Proprietary enterprise artifacts remain inside internal firewall, never exposed to public Docker Hub.",
              "Multi-Tagging Strategy:\n  • :v2 — Build-specific immutable artifact tied to Git commit.\n  • :latest — Operational pointer for active deployment.\n  • localhost:5000/... — Target registry publication tag.",
              "Storage Efficiency: Layer caching allows multiple tags to share identical underlying layers with zero storage duplication."],
             "Enterprise Registry", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 8: QUALITY GATES & SELENIUM ACCEPTANCE TESTING
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Automated Quality Gates: Selenium WebDriver E2E Testing")

    add_card(slide8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1),
             "Why Unit Tests Are Not Enough",
             ["Unit tests verify Java methods in isolation; they cannot test DOM rendering, CSS, or browser session handling.",
              "Selenium WebDriver launches a real headless Google Chrome instance inside Jenkins.",
              "Executes complete user actions against the live containerized deployment on port 8080.",
              "If any button fails, API response hangs, or modal fails to appear, the pipeline halts immediately, preventing flawed releases from reaching users."],
             "Acceptance Quality Gate", ACCENT_AMBER)

    add_card(slide8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1),
             "The 5 Automated User Journey Tests & Artifact Proofs",
             ["Journey 1: Initial Dashboard Load & Health Status Verification (Checks server status UP and memory metrics).",
              "Journey 2: Create New Controlled Document Draft (Fills form, submits SOP/Policy, verifies DRAFT table entry).",
              "Journey 3: Submit DRAFT Document for Review (Transitions state to PENDING_APPROVAL and verifies author lock).",
              "Journey 4: Formal Review & Approval Decision Gate (Approver verifies document, applies sign-off comments, reaches RELEASED).",
              "Journey 5: Search Filtering & Category Tab Navigation (Validates live instant search across SOP, Policy, Spec tabs).",
              "Audit Artifacts: Jenkins permanently archives all 5 visual screenshot proofs (Journey_1 to Journey_5.png)."],
             "Audited User Journeys", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 9: DEVOPS RELIABILITY, RESILIENCE & FIXES
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "DevOps Engineering: Troubleshooting, Self-Healing & Reliability")

    add_card(slide9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1),
             "The Windows File-Locking Challenge & Resolution",
             ["Problem: Windows locks any JAR file actively executed by a running Java process on port 8080.",
              "Symptom: Jenkins CI builds failed with 'Failed to delete target/automated-document-approval-1.0.0.jar'.",
              "Engineered Solution: Implemented an automated pre-build process cleanup hook directly into the Jenkins configuration:",
              "Script: for /f \"tokens=5\" %%a in ('netstat -aon | findstr :8080 | findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1",
              "Result: Scheduled 15-minute builds now execute cleanly without manual intervention or process collisions."],
             "Self-Healing CI Fix", ACCENT_CYAN)

    add_card(slide9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1),
             "Continuous Health Probing & Zero-Downtime Deployment",
             ["Liveness Verification: Pipeline executes automated HTTP polling against /api/health before triggering E2E tests.",
              "Safe Container Transition: Existing container is stopped and removed; new image is deployed seamlessly in <3 seconds.",
              "Audit Integrity: Every build records cryptographic hashes and fingerprints for full forensic traceability.",
              "Environment Isolation: Jenkins agent workspace, host OS, and Docker runtime operate in separate security boundaries."],
             "Operational Stability", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 10: CONCLUSION, METRICS & FUTURE ROADMAP
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Project Conclusion, Value Delivered & Future Roadmap")

    add_card(slide10, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.1),
             "1. Deliverables & Results",
             ["Fully operational Spring Boot controlled document approval microservice.",
              "Two-tier Jenkins automation: fast CI loop (15s) and full CD delivery (2.8m).",
              "Dockerized deployment with Alpine JRE 17 and private registry on port 5000.",
              "100% automated test coverage combining JUnit 5 and Selenium WebDriver UI tests.",
              "Passed Jenkins Build #61 with all status indicators green."],
             "Key Achievements", ACCENT_GREEN)

    add_card(slide10, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.1),
             "2. Business Impact",
             ["Eliminated 100% of manual deployment friction and configuration errors.",
              "Guaranteed tamper-evident compliance for GxP / FDA 21 CFR Part 11 audits.",
              "Accelerated document release cycles from days to under 3 minutes.",
              "Instant rollback capability through immutable versioned Docker images."],
             "Business Value", ACCENT_CYAN)

    add_card(slide10, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.1),
             "3. Future Roadmap",
             ["Kubernetes (K8s) Cluster Deployment: Multi-replica deployment with Helm charts and rolling updates.",
              "Observability: Integration with Prometheus and Grafana for real-time latency and throughput dashboards.",
              "Static Code Analysis: SonarQube quality gate integration for security vulnerability scanning.",
              "Open for Questions & Live Demonstration."],
             "Next Steps", ACCENT_PURPLE)

    output_path = os.path.abspath("DevOps_Project_Presentation.pptx")
    prs.save(output_path)
    print(f"PowerPoint Presentation successfully created at: {output_path}")

create_deck()
