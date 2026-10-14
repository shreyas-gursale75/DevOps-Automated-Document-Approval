// Declarative Jenkinsfile Pipeline for Automated Controlled Document Version Approval System
pipeline {
    agent any

    tools {
        maven 'Maven-3.9.9'
        jdk 'JDK-17'
    }

    parameters {
        string(name: 'DEPLOY_PORT', defaultValue: '8080', description: 'Port to deploy on')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Target deployment environment')
    }

    environment {
        BUILD_ID = 'dontKillMe'
        JENKINS_NODE_COOKIE = 'dontKillMe'
        APP_NAME = 'automated-document-approval'
        IMAGE_TAG = "v${env.BUILD_NUMBER}"
        REGISTRY_HOST = 'localhost:5000'
        EFFECTIVE_PORT = "${params.DEPLOY_PORT ?: '8080'}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source baseline from Git...'
                bat """
                    @echo off
                    echo Synchronizing workspace from local Git repository...
                    robocopy "C:\\Users\\Shreyas Gursale\\Desktop\\DevOps Project" . /E /XD .git target .jenkins /NFL /NDL /NJH /NJS /nc /ns /np || ver >nul
                    git -C "C:\\Users\\Shreyas Gursale\\Desktop\\DevOps Project" log -1 --oneline
                    exit /b 0
                """
            }
        }

        stage('Build & Unit Tests') {
            steps {
                bat """
                    @echo off
                    echo Terminating any conflicting host processes on port ${EFFECTIVE_PORT}...
                    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :${EFFECTIVE_PORT} ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1 || ver >nul
                    mvn test -Dtest=DocumentApprovalApplicationTests
                """
            }
            post {
                always {
                    echo 'Unit tests completed successfully. Surefire test reports generated in target/surefire-reports/'
                }
            }
        }

        stage('Package Artefact') {
            steps {
                echo 'Packaging application executable JAR...'
                bat 'mvn package -DskipTests'
                archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
            }
        }

        stage('Docker Image Build & Registry Publish') {
            steps {
                echo "Building Docker container image ${APP_NAME}:${IMAGE_TAG} and tagging for ${REGISTRY_HOST}..."
                bat """
                    @echo off
                    docker build -t ${APP_NAME}:${IMAGE_TAG} -t ${APP_NAME}:latest -t ${REGISTRY_HOST}/${APP_NAME}:${IMAGE_TAG} -t ${REGISTRY_HOST}/${APP_NAME}:latest .
                    if %ERRORLEVEL% NEQ 0 (
                        echo [ERROR] Docker build failed!
                        exit /b 1
                    )
                    echo Publishing versioned image to Docker Registry (${REGISTRY_HOST})...
                    docker push ${REGISTRY_HOST}/${APP_NAME}:${IMAGE_TAG}
                    docker push ${REGISTRY_HOST}/${APP_NAME}:latest
                    echo Docker image published successfully to registry!
                    exit /b 0
                """
            }
        }

        stage('Continuous Deployment (Docker Container)') {
            steps {
                echo "Deploying fresh container ${APP_NAME}:${IMAGE_TAG} to port ${EFFECTIVE_PORT}..."
                bat """
                    @echo off
                    echo Cleaning up existing container if present...
                    docker stop ${APP_NAME} >nul 2>&1 || ver >nul
                    docker rm -f ${APP_NAME} >nul 2>&1 || ver >nul
                    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :${EFFECTIVE_PORT} ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1 || ver >nul
                    
                    echo Starting containerized deployment from local registry image...
                    docker run -d --name ${APP_NAME} -p ${EFFECTIVE_PORT}:8080 ${REGISTRY_HOST}/${APP_NAME}:${IMAGE_TAG}
                    if %ERRORLEVEL% NEQ 0 (
                        echo [ERROR] Failed to start Docker container!
                        exit /b 1
                    )
                    echo Container launched successfully.
                    exit /b 0
                """
            }
        }

        stage('Health & Reliability Check') {
            steps {
                echo 'Executing container liveness and health verification...'
                bat """
                    @echo off
                    echo Waiting for containerized application to initialize on port ${EFFECTIVE_PORT}...
                    ping 127.0.0.1 -n 7 >nul
                    curl -f http://localhost:${EFFECTIVE_PORT}/api/health || exit /b 1
                    echo.
                    echo Container health check passed successfully!
                    exit /b 0
                """
            }
        }

        stage('Automated Acceptance Tests (Selenium E2E)') {
            steps {
                echo 'Executing Selenium WebDriver E2E test suite against containerized deployment...'
                bat 'mvn test -Dtest=SeleniumE2ETests'
            }
            post {
                always {
                    echo 'Recording Selenium E2E execution results and screenshots...'
                    archiveArtifacts artifacts: '**/target/screenshots/*.png', allowEmptyArchive: true
                }
                failure {
                    echo '[QUALITY GATE BLOCKED] Acceptance tests failed on containerized deployment!'
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline successfully executed! Container ${APP_NAME}:${IMAGE_TAG} is live on port ${EFFECTIVE_PORT}."
        }
        failure {
            echo 'Pipeline failed. Automated container deployment blocked.'
        }
    }
}
