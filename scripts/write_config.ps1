$src = "C:\Users\Shreyas Gursale\Desktop\DevOps Project\jenkins_ci_job_config.xml"
$destDir = "C:\Users\Shreyas Gursale\.jenkins\jobs\Document-Approval-CI"
if (!(Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
}
$dest = Join-Path $destDir "config.xml"
Copy-Item -Path $src -Destination $dest -Force
$len = (Get-Item $dest).Length
Write-Output "config.xml size: $len bytes"
