# Azure Container Instances Deployment Guide

**Fastest way to deploy your API to Azure** - fully automated with GitHub Actions.

## Prerequisites

✅ GitHub repository (already have: ChrisKoenig/techrob-action360-agent)  
✅ Docker Hub account (free: https://hub.docker.com/signup)  
✅ Azure subscription (already set up)

## Step 1: Create Docker Hub Account

1. Go to https://hub.docker.com/signup
2. Create free account
3. Save your username and token

## Step 2: Create Azure Service Principal

For GitHub Actions to deploy to Azure:

```bash
# Create service principal
$subscription = "f23858ca-331b-4f31-89c1-e2ffa9e5c17c"
$sp = az ad sp create-for-rbac --name techrob-action360-github --role Contributor --scopes /subscriptions/$subscription

# Output will look like:
# {
#   "appId": "...",
#   "displayName": "techrob-action360-github",
#   "password": "...",
#   "tenant": "..."
# }

# Convert to JSON format GitHub expects
$spJson = @{
    clientId = $sp.appId
    clientSecret = $sp.password
    subscriptionId = $subscription
    tenantId = $sp.tenant
} | ConvertTo-Json

Write-Host $spJson
```

Copy the entire JSON output.

## Step 3: Add GitHub Secrets

1. Go to your repository: https://github.com/ChrisKoenig/techrob-action360-agent
2. Settings > Secrets and variables > Actions
3. Create these secrets:

| Secret Name | Value |
|---|---|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub token/password |
| `AZURE_CREDENTIALS` | The JSON from Step 2 |
| `FOUNDRY_PROJECT_ENDPOINT` | `https://action360-agent-resource.services.ai.azure.com/api/projects/action360-agent` |
| `FOUNDRY_PROJECT_NAME` | `action360-agent` |
| `FOUNDRY_RESOURCE_GROUP` | `action360-agent-resource` |
| `FOUNDRY_SUBSCRIPTION_ID` | `f23858ca-331b-4f31-89c1-e2ffa9e5c17c` |

## Step 4: Trigger Deployment

### Automatic (on push):
```bash
git add .
git commit -m "feat: add Azure Container Instances deployment"
git push origin main
```

This automatically triggers the GitHub Actions workflow.

### Manual Trigger:
1. Go to: https://github.com/ChrisKoenig/techrob-action360-agent/actions
2. Select: "Deploy to Azure Container Instances"
3. Click: "Run workflow" > "Run workflow"

## Step 5: Monitor Deployment

1. Go to https://github.com/ChrisKoenig/techrob-action360-agent/actions
2. Click the running workflow
3. Watch the logs in real-time

Expected steps:
- ✅ Checkout code
- ✅ Set up Docker Buildx
- ✅ Login to Docker Hub
- ✅ Build and push image (~2-3 minutes)
- ✅ Azure Login
- ✅ Deploy to ACI (~1 minute)
- ✅ Test API Health

## Step 6: Get Your API URL

After successful deployment:

```bash
# Get the FQDN
az container show \
  --resource-group rg-techrob-action360 \
  --name techrob-action360-api \
  --query ipAddress.fqdn -o tsv

# URL will be: http://techrob-action360-api.<region>.azurecontainers.io:8000
```

Or check GitHub Actions output for: `API_URL`

## Step 7: Test Your API

```bash
# Test health endpoint
$url = "http://techrob-action360-api.<your-region>.azurecontainers.io:8000"

Invoke-WebRequest -Uri "$url/api/health"

# Should return:
# {"status":"ok","agent_initialized":false}
```

## Step 8: Use in M365 Copilot

Your API endpoint is now ready for Teams/M365 integration:

```
https://techrob-action360-api.<region>.azurecontainers.io:8000
```

Use this in Teams app manifest.

## Monitoring & Logs

```bash
# View container logs
az container logs \
  --resource-group rg-techrob-action360 \
  --name techrob-action360-api

# View container status
az container show \
  --resource-group rg-techrob-action360 \
  --name techrob-action360-api \
  --query ipAddress
```

## Scaling & Costs

**Cost**: ~$0.015/hour (~$11/month for 24/7 usage)

**To scale up**:
Edit `.github/workflows/deploy-aci.yml` and increase:
- `--cpu 1` → `--cpu 2`
- `--memory 1.5` → `--memory 3.5`

## Redeploy on Code Changes

Any push to `main` branch automatically redeploys:

```bash
git commit -am "fix: update agent logic"
git push origin main
# Workflow runs automatically
```

## Troubleshooting

### "Docker login failed"
- Verify `DOCKER_PASSWORD` is a token, not your password
- Generate token at: https://hub.docker.com/settings/security

### "Azure credentials invalid"
- Recreate service principal from Step 2
- Verify JSON format in `AZURE_CREDENTIALS` secret

### "Container stuck in Creating state"
- Check logs: `az container logs ...`
- Container may be pulling large image first time
- Takes 1-2 minutes on first deploy

### "API returns 500 errors"
- Check logs: `az container logs ...`
- Verify environment variables are set correctly
- Ensure `FOUNDRY_PROJECT_ENDPOINT` is reachable

## Next Steps

1. ✅ Deployment complete
2. 🔄 Test the API
3. 📱 Move to Teams integration (see [TEAMS_INTEGRATION.md](../TEAMS_INTEGRATION.md))

---

**Questions?** Check GitHub Actions logs or run:
```bash
az container show --resource-group rg-techrob-action360 --name techrob-action360-api
```
