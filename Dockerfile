# Production Dockerfile for Automated Controlled Document Version Approval System
# Based on Eclipse Temurin 17 JRE Alpine for minimal attack surface and fast startup
FROM eclipse-temurin:17-jre-alpine

LABEL maintainer="DevOps Team <devops@organization.com>"
LABEL version="1.0.0"
LABEL description="Automated Controlled Document Version Approval System"

WORKDIR /app

# Create non-privileged user and group for container security compliance
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy tested and packaged Spring Boot application artifact
ARG JAR_FILE=target/automated-document-approval-1.0.0.jar
COPY ${JAR_FILE} app.jar

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=5s --start-period=15s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/api/health || exit 1

ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-Dserver.port=8080", "-jar", "app.jar"]
