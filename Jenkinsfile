// Declarative Jenkinsfile Pipeline for Automated Controlled Document Version Approval System
pipeline {
    agent any

    tools {
        maven 'Maven-3.9.9'
        jdk 'JDK-17'
    }

    environment {
        APP_NAME = 'automated-document-approval'
        IMAGE_TAG = "v${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = 'docker.io/myorg'
        DEPLOY_PORT = '8080'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source baseline from Git...'
                checkout scm
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
                echo "Building Docker container image: ${APP_NAME}:${IMAGE_TAG}..."
                bat "docker build -t ${APP_NAME}:${IMAGE_TAG} -t ${APP_NAME}:latest ."
            }
        }

        stage('Continuous Deployment (Tomcat/Docker)') {
            steps {
                echo "Deploying containerized application to port ${DEPLOY_PORT}..."
                bat """
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                    docker run -d --name ${APP_NAME} -p ${DEPLOY_PORT}:8080 ${APP_NAME}:latest
                """
            }
        }

        stage('Health & Reliability Check') {
            steps {
                echo 'Executing liveness and health verification...'
                bat "curl -f http://localhost:${DEPLOY_PORT}/api/health || exit 1"
            }
        }
    }

    post {
        success {
            echo 'Pipeline successfully executed! Application is live on Tomcat.'
        }
        failure {
            echo 'Pipeline failed. Automated deployment blocked.'
        }
    }
}
