$baseUrl = "http://localhost:8085"
$jobName = "Document-Approval-Pipeline"
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

# 1. Fetch Crumb
try {
    $crumbRes = Invoke-RestMethod -Uri "$baseUrl/crumbIssuer/api/json" -WebSession $session
    $crumbField = $crumbRes.crumbRequestField
    $crumbValue = $crumbRes.crumb
    Write-Output "Obtained Crumb: $crumbField = $crumbValue"
} catch {
    $crumbField = "Jenkins-Crumb"
    $crumbValue = ""
}

# 2. Get current job config
$configXml = Invoke-RestMethod -Uri "$baseUrl/job/$jobName/config.xml" -WebSession $session

# 3. Read Jenkinsfile content and XML escape
$jenkinsfileContent = Get-Content -Path "Jenkinsfile" -Raw
$escapedScript = [System.Security.SecurityElement]::Escape($jenkinsfileContent)

# 4. Replace script inside configXml
$pattern = '(?s)<script>.*?</script>'
$newScriptTag = "<script>$escapedScript</script>"
$updatedXml = [System.Text.RegularExpressions.Regex]::Replace($configXml, $pattern, $newScriptTag)

# 5. POST updated configXml
$headers = @{
    "Content-Type" = "application/xml"
}
if ($crumbValue) {
    $headers[$crumbField] = $crumbValue
}

$updateUrl = "$baseUrl/job/$jobName/config.xml"
$response = Invoke-WebRequest -Uri $updateUrl -Method POST -Headers $headers -Body $updatedXml -WebSession $session
Write-Output "Pipeline Updated Status: $($response.StatusCode)"
