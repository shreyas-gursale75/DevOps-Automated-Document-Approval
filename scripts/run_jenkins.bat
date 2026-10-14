@echo off
set "JAVA_HOME=C:\Users\Shreyas Gursale\.tools\jdk21\jdk21.0.12_12"
set "M2_HOME=C:\Users\Shreyas Gursale\.tools\maven\apache-maven-3.9.9"
set "PATH=%JAVA_HOME%\bin;%M2_HOME%\bin;C:\Users\Shreyas Gursale\.tools\jdk17\jdk17.0.20_12\bin;%PATH%"
set "JENKINS_HOME=C:\Users\Shreyas Gursale\.jenkins"

echo Starting Jenkins LTS on port 8085 with CSRF disabled for local automation...
"%JAVA_HOME%\bin\java.exe" -Djenkins.install.runSetupWizard=false -Dhudson.security.csrf.GlobalCrumbIssuerConfiguration.DISABLE_CSRF_PROTECTION=true -jar "C:\Users\Shreyas Gursale\.tools\jenkins\jenkins.war" --httpPort=8085
