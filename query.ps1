#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Query the TechRob Action360 Agent via REST API

.DESCRIPTION
    Sends a query to the TechRob Action360 Agent running on localhost:8000
    and returns the response.

.PARAMETER Query
    The query string to send to the agent

.EXAMPLE
    .\query.ps1 "What work items do I have?"
    .\query.ps1 "Show me recent Actions in state Active"
    .\query.ps1 "List all pull requests"

.NOTES
    Requires the API server to be running on http://localhost:8000
    Start the server with: python run_api.py
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Query
)

$ApiUrl = "http://localhost:8000/api/query"

try {
    # Check if API is reachable
    $healthUrl = "http://localhost:8000/api/health"
    $healthCheck = Invoke-RestMethod -Uri $healthUrl -ErrorAction SilentlyContinue
    
    if (-not $healthCheck) {
        Write-Host "❌ Error: API server is not responding at $healthUrl" -ForegroundColor Red
        Write-Host "Start the server with: python run_api.py" -ForegroundColor Yellow
        exit 1
    }
    
    # Build request body
    $body = @{
        query = $Query
    } | ConvertTo-Json
    
    Write-Verbose "📤 Sending query to $ApiUrl"
    Write-Verbose "Query: $Query"
    
    # Send query
    $response = Invoke-RestMethod -Uri $ApiUrl -Method Post -ContentType "application/json" -Body $body -ErrorAction Stop
    
    # Display response
    if ($response.response) {
        Write-Host "✅ Response:" -ForegroundColor Green
        Write-Host $response.response
    }
    else {
        Write-Host "❌ No response from agent" -ForegroundColor Red
        Write-Verbose "Full response: $($response | ConvertTo-Json)"
        exit 1
    }
}
catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    Write-Verbose $_.Exception.StackTrace
    exit 1
}
