$javaHome = 'C:\Users\Shreyas Gursale\.tools\jdk17\jdk17.0.20_12'
$mavenHome = 'C:\Users\Shreyas Gursale\.tools\maven\apache-maven-3.9.9'

[Environment]::SetEnvironmentVariable('JAVA_HOME', $javaHome, [EnvironmentVariableTarget]::User)
[Environment]::SetEnvironmentVariable('M2_HOME', $mavenHome, [EnvironmentVariableTarget]::User)

$userPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::User)
if ($userPath -notlike "*$javaHome*") {
    $newPath = "$javaHome\bin;$mavenHome\bin;$userPath"
    [Environment]::SetEnvironmentVariable('Path', $newPath, [EnvironmentVariableTarget]::User)
    Write-Output "User PATH updated successfully with Java and Maven."
} else {
    Write-Output "User PATH already contains Java."
}
