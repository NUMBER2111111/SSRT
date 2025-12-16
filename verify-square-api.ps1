Write-Host "Testing Square Payment API..." -ForegroundColor Cyan
Write-Host ""

$uri = "https://ssrt-opal.vercel.app/api/payment/create-link"
$body = '{"amount":500,"currency":"USD","name":"SSRT"}'

try {
  $response = Invoke-WebRequest `
    -Uri $uri `
    -Method POST `
    -Headers @{
      "Content-Type"="application/json"
      "Cache-Control"="no-cache"
    } `
    -Body $body `
    -ErrorAction Stop

  Write-Host "Status Code: $($response.StatusCode)" -ForegroundColor Green
  Write-Host ""
  Write-Host "Response Body:" -ForegroundColor Yellow
  $json = $response.Content | ConvertFrom-Json
  $json | ConvertTo-Json -Depth 10

  if ($json.url -and $json.url -like "*square.link*") {
    Write-Host ""
    Write-Host "SUCCESS: Square link generated" -ForegroundColor Green
    Write-Host "URL: $($json.url)" -ForegroundColor Cyan
  } else {
    Write-Host ""
    Write-Host "ERROR: Missing Square URL field" -ForegroundColor Red
  }

} catch {
  Write-Host "ERROR: Request failed" -ForegroundColor Red
  if ($_.Exception.Response) {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $errBody = $reader.ReadToEnd()
    Write-Host "HTTP Error Body:" -ForegroundColor Yellow
    Write-Host $errBody
  } else {
    Write-Host $_.Exception.Message
  }
}

