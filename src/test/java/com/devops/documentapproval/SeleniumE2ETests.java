package com.devops.documentapproval;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.time.Duration;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Phase 9: Automated End-to-End Selenium WebDriver Test Suite
 * Covers 5 Critical User Journeys across the Document Version Approval Lifecycle.
 */
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class SeleniumE2ETests {

    private static WebDriver driver;
    private static WebDriverWait wait;
    private static final String BASE_URL = "http://localhost:8080";

    @BeforeAll
    public static void setUpClass() {
        try {
            WebDriverManager.chromedriver().setup();
        } catch (Exception e) {
            System.out.println("[NOTE] WebDriverManager setup bypassed: " + e.getMessage());
        }

        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--disable-gpu");
        options.addArguments("--remote-allow-origins=*");
        options.addArguments("--window-size=1400,900");

        File chromeExe = new File("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe");
        if (chromeExe.exists()) {
            options.setBinary(chromeExe);
        }

        driver = new ChromeDriver(options);
        wait = new WebDriverWait(driver, Duration.ofSeconds(12));
    }

    @AfterAll
    public static void tearDownClass() {
        if (driver != null) {
            driver.quit();
        }
    }

    @BeforeEach
    public void navigateToDashboard() {
        driver.get(BASE_URL);
        wait.until(ExpectedConditions.presenceOfElementLocated(By.id("documentTableBody")));
    }

    @AfterEach
    public void captureScreenshotOnFailure(TestInfo testInfo) {
        try {
            File screenshotDir = new File("target/screenshots");
            if (!screenshotDir.exists()) {
                screenshotDir.mkdirs();
            }
            File srcFile = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            File destFile = new File(screenshotDir, testInfo.getDisplayName().replaceAll("[^a-zA-Z0-9_-]", "_") + ".png");
            Files.copy(srcFile.toPath(), destFile.toPath(), StandardCopyOption.REPLACE_EXISTING);
        } catch (Exception e) {
            System.err.println("Screenshot capture failed: " + e.getMessage());
        }
    }

    /**
     * Critical Journey 1: Verify Dashboard Initial Load & Seed Documents
     */
    @Test
    @Order(1)
    @DisplayName("Journey 1: Initial Dashboard Load & Health Status Verification")
    public void test01_dashboardInitialLoad() {
        // Verify Title and Header
        assertEquals("DocuControl | Automated Document Version Approval System", driver.getTitle());
        WebElement brandTitle = driver.findElement(By.className("brand-title"));
        assertEquals("DocuControl", brandTitle.getText());

        // Verify System Health Badge
        WebElement healthBadge = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("healthStatusText")));
        assertTrue(healthBadge.getText().contains("UP"), "Health status should indicate service is UP");

        // Verify Metric Cards are populated with numeric values
        wait.until(driver -> {
            String total = driver.findElement(By.id("metricTotalDocs")).getText();
            return !total.equals("-") && !total.isEmpty();
        });

        int totalDocs = Integer.parseInt(driver.findElement(By.id("metricTotalDocs")).getText().trim());
        assertTrue(totalDocs >= 3, "Initial dashboard should contain at least 3 seeded documents");

        // Verify document table rows rendered
        List<WebElement> rows = driver.findElements(By.cssSelector("#documentTableBody tr"));
        assertFalse(rows.isEmpty(), "Document table should not be empty");
    }

    /**
     * Critical Journey 2: Draft New Controlled Document Workflow
     */
    @Test
    @Order(2)
    @DisplayName("Journey 2: Create New Controlled Document Draft")
    public void test02_createNewDocumentDraft() {
        String testTitle = "DevOps Automated Release Gate Standard (Selenium Test " + System.currentTimeMillis() + ")";
        String testAuthor = "QA Automation Suite";
        String testSummary = "Automated test validating end-to-end document creation";
        String testContent = "This document establishes the formal compliance criteria for automated delivery pipelines.";

        // Open Modal
        WebElement btnOpenModal = wait.until(ExpectedConditions.elementToBeClickable(By.id("btnOpenNewDocModal")));
        btnOpenModal.click();

        // Verify Modal is visible
        WebElement modal = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("modalCreateDoc")));
        assertTrue(modal.isDisplayed(), "Create Document modal should be visible");

        // Fill Form
        WebElement titleInput = driver.findElement(By.id("docTitle"));
        titleInput.clear();
        titleInput.sendKeys(testTitle);

        Select categorySelect = new Select(driver.findElement(By.id("docCategory")));
        categorySelect.selectByValue("SOP");

        WebElement authorInput = driver.findElement(By.id("docAuthor"));
        authorInput.clear();
        authorInput.sendKeys(testAuthor);

        WebElement summaryInput = driver.findElement(By.id("docSummary"));
        summaryInput.clear();
        summaryInput.sendKeys(testSummary);

        WebElement contentInput = driver.findElement(By.id("docContent"));
        contentInput.clear();
        contentInput.sendKeys(testContent);

        // Submit Form
        WebElement btnSubmit = driver.findElement(By.id("btnSubmitNewDoc"));
        btnSubmit.click();

        // Wait for modal to close
        wait.until(ExpectedConditions.invisibilityOfElementLocated(By.id("modalCreateDoc")));

        // Verify document appears in table
        wait.until(ExpectedConditions.textToBePresentInElementLocated(By.id("documentTableBody"), testTitle));
        WebElement tableBody = driver.findElement(By.id("documentTableBody"));
        assertTrue(tableBody.getText().contains(testTitle), "Newly created document should appear in table");
        assertTrue(tableBody.getText().contains(testAuthor), "Author should be displayed in table");
    }

    private static WebElement clickWithRetry(By locator) {
        return wait.until(d -> {
            try {
                WebElement el = d.findElement(locator);
                if (el.isDisplayed() && el.isEnabled()) {
                    el.click();
                    return el;
                }
                return null;
            } catch (StaleElementReferenceException | ElementClickInterceptedException e) {
                return null;
            }
        });
    }

    /**
     * Critical Journey 3: Submit Draft for Review Workflow
     */
    @Test
    @Order(3)
    @DisplayName("Journey 3: Submit DRAFT Document for Review")
    public void test03_submitDraftForReview() throws InterruptedException {
        // Filter by DRAFT
        clickWithRetry(By.cssSelector(".filter-tab[data-status='DRAFT']"));
        Thread.sleep(800);

        // Click Submit for Review with retry
        By submitLocator = By.xpath("//tr[contains(., 'Draft')]//button[contains(text(), 'Submit for Review')]");
        clickWithRetry(submitLocator);

        // Verify toast confirmation specifically for submission
        WebElement toast = wait.until(ExpectedConditions.presenceOfElementLocated(
            By.xpath("//div[contains(@class,'toast') and (contains(text(), 'submitted') or contains(text(), 'queue'))]")));
        assertNotNull(toast, "Submission success toast should appear");
    }

    /**
     * Critical Journey 4: Review Decision Gate (Approval)
     */
    @Test
    @Order(4)
    @DisplayName("Journey 4: Formal Review & Approval Decision Gate")
    public void test04_approvePendingDocument() throws InterruptedException {
        // Switch filter to PENDING_APPROVAL
        clickWithRetry(By.cssSelector(".filter-tab[data-status='PENDING_APPROVAL']"));
        Thread.sleep(800);

        // Click Review Gate with retry
        By reviewGateLocator = By.xpath("//button[contains(text(), 'Review Gate')]");
        clickWithRetry(reviewGateLocator);

        // Review Modal Opens
        WebElement modal = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("modalReviewDoc")));
        assertTrue(modal.isDisplayed(), "Review decision modal should be visible");

        // Enter Reviewer Details
        WebElement reviewerInput = driver.findElement(By.id("reviewerName"));
        reviewerInput.clear();
        reviewerInput.sendKeys("Marcus Vance (Lead Auditor)");

        WebElement commentsInput = driver.findElement(By.id("reviewerComments"));
        commentsInput.clear();
        commentsInput.sendKeys("Automated compliance verification passed. Architecture and security controls approved.");

        // Click Approve
        WebElement btnApprove = driver.findElement(By.id("btnApproveDecision"));
        btnApprove.click();

        // Wait for modal to close and toast confirmation specifically for approval
        wait.until(ExpectedConditions.invisibilityOfElementLocated(By.id("modalReviewDoc")));
        WebElement toast = wait.until(ExpectedConditions.presenceOfElementLocated(
            By.xpath("//div[contains(@class,'toast') and (contains(text(), 'approved') or contains(text(), 'Approved'))]")));
        assertNotNull(toast, "Approval confirmation toast should appear");
    }

    /**
     * Critical Journey 5: Search and Filtering Operations
     */
    @Test
    @Order(5)
    @DisplayName("Journey 5: Search Filtering & Category Tab Navigation")
    public void test05_searchAndFilterNavigation() {
        // Test Search Bar
        WebElement searchInput = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("searchInput")));
        searchInput.clear();
        searchInput.sendKeys("Cloud Infrastructure");

        // Wait for debounce and verify filter
        wait.until(ExpectedConditions.textToBePresentInElementLocated(By.id("documentTableBody"), "Cloud Infrastructure"));
        WebElement tableBody = driver.findElement(By.id("documentTableBody"));
        assertTrue(tableBody.getText().contains("DOC-2026-1002"), "Search should locate DOC-2026-1002");

        // Clear Search
        searchInput.sendKeys(Keys.CONTROL + "a");
        searchInput.sendKeys(Keys.BACK_SPACE);

        // Click 'Released' filter tab
        WebElement releasedTab = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".filter-tab[data-status='RELEASED']")));
        releasedTab.click();

        wait.until(ExpectedConditions.textToBePresentInElementLocated(By.id("documentTableBody"), "DOC-2026-1001"));
        WebElement releasedTable = driver.findElement(By.id("documentTableBody"));
        assertTrue(releasedTable.getText().contains("DOC-2026-1001"), "Released filter tab should show DOC-2026-1001");

        // Reset to 'All'
        WebElement allTab = driver.findElement(By.cssSelector(".filter-tab[data-status='']"));
        allTab.click();
    }
}
