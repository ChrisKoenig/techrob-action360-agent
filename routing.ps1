#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Query the TechRob Action360 Agent for routing recommendations via REST API

.DESCRIPTION
    Sends a routing analysis query to the TechRob Action360 Agent running on localhost:8000
    and returns routing recommendations for an Action.

.PARAMETER ActionId
    The Action ID to analyze for routing

.PARAMETER Query
    (Optional) Custom query string for routing analysis. If not provided, will use:
    "Analyze action {ActionId} and provide routing recommendation"

.EXAMPLE
    .\routing.ps1 12345
    .\routing.ps1 12345 "Analyze action 12345 and provide detailed routing recommendation with escalation path"
    .\routing.ps1 ABC-123

.NOTES
    Requires the API server to be running on http://localhost:8000
    Start the server with: python run_api.py
    
    The API must be configured with routing instructions. See DYNAMIC_INSTRUCTIONS.md
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$ActionId,
    
    [Parameter(Mandatory = $false, Position = 1)]
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
    
    # Use provided query or build default query
    if ([string]::IsNullOrWhiteSpace($Query)) {
        $Query = "Analyze action $ActionId and provide routing recommendation"
    }
    
    # Build request body with routing instruction type
    $body = @{
        query            = $Query
        instruction_type = "routing"
    } | ConvertTo-Json
    
    Write-Host "🔍 Analyzing Action: $ActionId" -ForegroundColor Cyan
    Write-Verbose "📤 Sending routing query to $ApiUrl"
    Write-Verbose "Query: $Query"
    Write-Verbose "Instruction Type: routing"
    
    # Send query
    $response = Invoke-RestMethod -Uri $ApiUrl -Method Post -ContentType "application/json" -Body $body -ErrorAction Stop
    
    # Display response
    if ($response.response) {
        Write-Host "`n✅ Routing Recommendation:" -ForegroundColor Green
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        Write-Host $response.response
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Show instruction type used
        Write-Verbose "Instruction Type Used: $($response.instruction_type)"
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
