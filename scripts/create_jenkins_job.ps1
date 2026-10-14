$baseUrl = "http://localhost:8085"
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

# 1. Fetch Crumb
try {
    $crumbRes = Invoke-RestMethod -Uri "$baseUrl/crumbIssuer/api/json" -WebSession $session
    $crumbField = $crumbRes.crumbRequestField
    $crumbValue = $crumbRes.crumb
    Write-Output "Obtained Crumb: $crumbField = $crumbValue"
} catch {
    Write-Output "Crumb issuer not required or error: $_"
    $crumbField = "Jenkins-Crumb"
    $crumbValue = ""
}

# 2. Post Job Config XML
$xmlContent = Get-Content -Path "jenkins_ci_job_config.xml" -Raw
$headers = @{
    "Content-Type" = "application/xml"
}
if ($crumbValue) {
    $headers[$crumbField] = $crumbValue
}

try {
    $createUrl = "$baseUrl/createItem?name=Document-Approval-CI"
    $response = Invoke-WebRequest -Uri $createUrl -Method POST -Headers $headers -Body $xmlContent -WebSession $session
    Write-Output "Job Creation Status: $($response.StatusCode)"
} catch {
    Write-Output "Creation response: $_"
}

# 3. Verify Job exists
try {
    $jobInfo = Invoke-RestMethod -Uri "$baseUrl/job/Document-Approval-CI/api/json" -WebSession $session
    Write-Output "Job Verified: $($jobInfo.name) | Buildable: $($jobInfo.buildable)"
} catch {
    Write-Output "Could not verify job: $_"
}
