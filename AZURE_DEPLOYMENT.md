# Azure Deployment Guide - TechRob Action360 Agent

Deploy your API to Azure App Service for production use with M365 Copilot integration.

## Prerequisites

- ✅ Azure subscription
- ✅ Azure CLI installed (`az` command)
- ✅ Logged into Azure: `az login`
- ✅ Azure AI Foundry project with GPT-4o deployment
- ✅ Azure DevOps organization (for MCP integration)

## Step 1: Prepare Deployment Parameters

Edit `infra/deploy.bicepparam` and fill in your Azure details:

```bicepparam
param location = 'eastus'  # Or your preferred Azure region
param foundryProjectEndpoint = 'https://<your-region>.api.azureml.ms'
param foundryProjectName = '<your-project-name>'
param foundryResourceGroup = '<your-rg-name>'
param foundrySubscriptionId = '<your-subscription-id>'
```

**To find your values:**

```bash
# Get your subscription ID
az account show --query id -o tsv

# Get your resource group name
az group list --query "[].name" -o tsv

# Find your Foundry project endpoint and name in Azure Portal
# Navigate to: Your Foundry Project > Project settings
```

## Step 2: Create Azure Resource Group

```bash
# Set your variables
$resourceGroup = "rg-techrob-action360"
$location = "eastus"

# Create resource group
az group create --name $resourceGroup --location $location
```

## Step 3: Deploy Infrastructure

Deploy the Bicep template to create the App Service:

```bash
# Set your variables
$resourceGroup = "rg-techrob-action360"
$templateFile = "infra/deploy.bicep"
$parametersFile = "infra/deploy.bicepparam"

# Deploy
az deployment group create `
  --resource-group $resourceGroup `
  --template-file $templateFile `
  --parameters $parametersFile
```

**Example output:**
```
deploymentId: /subscriptions/xxx/resourceGroups/rg-techrob-action360/deployments/deploy
deploymentName: deploy
deploymentState: Succeeded
outputs:
  webAppUrl:
    type: String
    value: https://techrob-action360-prod-xxxxx.azurewebsites.net
  webAppId:
    type: String
    value: /subscriptions/xxx/resourceGroups/rg-techrob-action360/providers/Microsoft.Web/sites/techrob-action360-prod-xxxxx
```

**Save the `webAppUrl`** - this is your API endpoint for M365 integration.

## Step 4: Deploy Code to App Service

### Option A: Deploy from GitHub (Recommended)

```bash
# Set your variables
$resourceGroup = "rg-techrob-action360"
$appName = "techrob-action360-prod-xxxxx"  # From deployment output
$gitHubRepo = "https://github.com/ChrisKoenig/techrob-action360-agent.git"
$branch = "main"

# Get your GitHub Personal Access Token
# (Create at: https://github.com/settings/tokens)

# Configure GitHub deployment
az webapp deployment github-actions add `
  --resource-group $resourceGroup `
  --name $appName `
  --repo $gitHubRepo `
  --branch $branch `
  --runtime "python|3.11"
```

This creates a GitHub Actions workflow that automatically deploys on push to `main`.

### Option B: Deploy Manually (Quick Test)

```bash
# Set your variables
$resourceGroup = "rg-techrob-action360"
$appName = "techrob-action360-prod-xxxxx"  # From deployment output

# Deploy from local directory
az webapp up `
  --resource-group $resourceGroup `
  --name $appName `
  --runtime "PYTHON:3.11" `
  --sku B2
```

## Step 5: Verify Deployment

Check that your API is running:

```bash
# Get the web app URL
$webAppUrl = az deployment group show `
  --resource-group "rg-techrob-action360" `
  --name "deploy" `
  --query "properties.outputs.webAppUrl.value" -o tsv

# Test health endpoint
Invoke-WebRequest -Uri "$webAppUrl/api/health"

# Should return: {"status":"ok","agent_initialized":false}
```

## Step 6: View Logs

Monitor your app in real-time:

```bash
# Stream application logs
az webapp log tail `
  --resource-group "rg-techrob-action360" `
  --name "techrob-action360-prod-xxxxx"
```

View logs in Azure Portal:
1. Navigate to your App Service
2. Select "Log stream" or "App Service logs"
3. Configure log levels in "Diagnostic settings"

## Step 7: Configure Custom Domain (Optional)

For production M365 Copilot integration, use a custom domain:

```bash
# Add custom domain
az webapp config hostname add `
  --resource-group "rg-techrob-action360" `
  --webapp-name "techrob-action360-prod-xxxxx" `
  --hostname "api.yourdomain.com"

# Create SSL certificate (optional, recommended)
# Use Azure Portal: App Service > TLS/SSL settings > Private Certificates
```

## Step 8: Set Up CORS for M365 Copilot (Next Step)

After verifying the API is running, configure CORS in your App Service:

```bash
az webapp cors add `
  --resource-group "rg-techrob-action360" `
  --name "techrob-action360-prod-xxxxx" `
  --allowed-origins "https://teams.microsoft.com" "https://*.teams.microsoft.com"
```

## Testing the API

### Test Query Endpoint

```bash
# Non-streaming query
$response = Invoke-WebRequest -Uri "$webAppUrl/api/query" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query": "Show action 676893", "instruction_type": "summary"}'

$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Test Streaming Endpoint

```bash
# Streaming query
$sse = Invoke-WebRequest -Uri "$webAppUrl/api/query/stream" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query": "Show action 676893", "instruction_type": "summary"}'

# Process Server-Sent Events
Write-Host $sse.Content
```

### List Available Tools

```bash
# Get available MCP tools
$tools = Invoke-WebRequest -Uri "$webAppUrl/api/tools" -Method GET
$tools.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

## Monitoring & Troubleshooting

### Scale the App Service

```bash
# If experiencing high load, scale up
az appservice plan update `
  --name "plan-techrob-action360-xxxxxx" `
  --resource-group "rg-techrob-action360" `
  --sku "B3"
```

### Check Application Insights

Your deployment includes Application Insights for monitoring:

```bash
# Get Application Insights resource
$appInsightsName = az deployment group show `
  --resource-group "rg-techrob-action360" `
  --name "deploy" `
  --query "properties.outputs" -o json | ConvertFrom-Json

# View in Azure Portal:
# 1. Search for "Application Insights"
# 2. Find "appinsights-techrob-action360-xxxxx"
# 3. Monitor performance, failures, logs
```

### Common Issues

#### "Module not found" errors
- Check `requirements.txt` is in root directory
- Ensure `startup.sh` has execution permissions
- Review App Service logs in Azure Portal

#### "Authentication failed"
- Verify Azure identity has access to Azure AI Foundry
- Check `FOUNDRY_PROJECT_ENDPOINT` is correct
- Run `az login` to refresh credentials

#### Slow startup
- First request initializes the agent (may take 30-60 seconds)
- Subsequent requests are faster
- Consider increasing `appServiceSkuName` to `B3` or `S1`

## Next: M365 Copilot Integration

Once verified:
1. Note your `webAppUrl` from deployment output
2. Proceed to Teams app manifest creation
3. Configure message extensions to call your API

**Your API is now production-ready!** 🚀

---

**Need help?** Check logs with:
```bash
az webapp log tail --resource-group "rg-techrob-action360" --name "techrob-action360-prod-xxxxx"
```
