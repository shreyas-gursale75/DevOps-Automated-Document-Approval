@echo off
set "JAVA_HOME=C:\Users\Shreyas Gursale\.tools\jdk17\jdk17.0.20_12"
set "M2_HOME=C:\Users\Shreyas Gursale\.tools\maven\apache-maven-3.9.9"
set "PATH=%JAVA_HOME%\bin;%M2_HOME%\bin;%PATH%"
echo Java version:
java -version
echo.
echo Maven version:
mvn -version
