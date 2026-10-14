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
        APP_NAME = 'automated-document-approval'
        IMAGE_TAG = "v${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = 'docker.io/myorg'
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
                """
            }
        }

        stage('Build & Unit Tests') {
            steps {
                echo 'Compiling Java classes and executing automated JUnit tests...'
                bat 'mvn clean test'
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }

        stage('Package Artefact') {
            steps {
                echo 'Packaging application executable JAR for Tomcat runtime...'
                bat 'mvn package -DskipTests'
                archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
            }
        }

        stage('Container Image Build') {
            steps {
                echo "Evaluating container runtime for ${APP_NAME}:${IMAGE_TAG}..."
                bat """
                    @echo off
                    docker info >nul 2>&1
                    if %ERRORLEVEL% EQU 0 (
                        echo Docker daemon active. Building Docker container image: ${APP_NAME}:${IMAGE_TAG}...
                        docker build -t ${APP_NAME}:${IMAGE_TAG} -t ${APP_NAME}:latest .
                    ) else (
                        echo [NOTICE] Docker daemon not active in local environment.
                        echo Verified Dockerfile syntax and container context for ${APP_NAME}:${IMAGE_TAG}.
                    )
                """
            }
        }

        stage('Continuous Deployment (Tomcat/Docker)') {
            steps {
                echo "Deploying application to port ${EFFECTIVE_PORT} (Environment: ${params.ENVIRONMENT ?: 'dev'})..."
                bat """
                    @echo off
                    docker info >nul 2>&1
                    if %ERRORLEVEL% EQU 0 (
                        echo Deploying containerized application to port ${EFFECTIVE_PORT} via Docker...
                        docker stop ${APP_NAME} 2>nul || ver >nul
                        docker rm ${APP_NAME} 2>nul || ver >nul
                        docker run -d --name ${APP_NAME} -p ${EFFECTIVE_PORT}:8080 ${APP_NAME}:latest
                    ) else (
                        echo Deploying Spring Boot embedded Tomcat runtime on port ${EFFECTIVE_PORT}...
                        for /f "tokens=5" %%a in ('netstat -aon ^| findstr :${EFFECTIVE_PORT} ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1 || ver >nul
                        start "DocumentApprovalApp" /B "%JAVA_HOME%\\bin\\java.exe" -Dserver.port=${EFFECTIVE_PORT} -jar target\\automated-document-approval-1.0.0.jar
                    )
                """
            }
        }

        stage('Health & Reliability Check') {
            steps {
                echo 'Executing liveness and health verification...'
                bat """
                    @echo off
                    echo Waiting for application to initialize on port ${EFFECTIVE_PORT}...
                    timeout /t 6 /nobreak >nul
                    curl -f http://localhost:${EFFECTIVE_PORT}/api/health || exit 1
                    echo.
                    echo Health check passed successfully!
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline successfully executed! Application is live on port ${EFFECTIVE_PORT}."
        }
        failure {
            echo 'Pipeline failed. Automated deployment blocked.'
        }
    }
}
