# ACI Deployment Setup Checklist

Complete these steps in order to deploy your API to Azure Container Instances.

## ✅ STEP 1: Create Docker Hub Account (5 min)

- [ ] Go to https://hub.docker.com/signup
- [ ] Create a free account
- [ ] Save your username

**Generate Docker Hub Personal Access Token:**
- [ ] Go to https://hub.docker.com/settings/security
- [ ] Click "New Access Token"
- [ ] Name it: `techrob-action360-github`
- [ ] Permissions: Read, Write
- [ ] Click "Generate"
- [ ] Copy the token (won't show again!)

---

## ✅ STEP 2: Create Azure Service Principal (5 min)

Run this command in PowerShell:

```powershell
$subscription = "f23858ca-331b-4f31-89c1-e2ffa9e5c17c"

$sp = az ad sp create-for-rbac `
  --name techrob-action360-github `
  --role Contributor `
  --scopes /subscriptions/$subscription

# Display as JSON (what GitHub needs)
$spJson = @{
    clientId = $sp.appId
    clientSecret = $sp.password
    subscriptionId = $subscription
    tenantId = $sp.tenant
} | ConvertTo-Json

Write-Host $spJson
```

**What to do with the output:**
- [ ] Copy the entire JSON output
- [ ] Don't share it with anyone
- [ ] You'll paste it in GitHub in the next step

---

## ✅ STEP 3: Add GitHub Secrets (5 min)

1. [ ] Go to your repo: https://github.com/ChrisKoenig/techrob-action360-agent
2. [ ] Click **Settings**
3. [ ] Click **Secrets and variables** (left sidebar)
4. [ ] Click **Actions**
5. [ ] Click **New repository secret**

**Add these 6 secrets:**

### Secret 1: DOCKER_USERNAME
- **Name:** `DOCKER_USERNAME`
- **Value:** Your Docker Hub username
- Click **Add secret**

### Secret 2: DOCKER_PASSWORD
- **Name:** `DOCKER_PASSWORD`
- **Value:** The token you generated (NOT your password)
- Click **Add secret**

### Secret 3: AZURE_CREDENTIALS
- **Name:** `AZURE_CREDENTIALS`
- **Value:** The entire JSON from Step 2
- Click **Add secret**

### Secret 4: FOUNDRY_PROJECT_ENDPOINT
- **Name:** `FOUNDRY_PROJECT_ENDPOINT`
- **Value:** `https://action360-agent-resource.services.ai.azure.com/api/projects/action360-agent`
- Click **Add secret**

### Secret 5: FOUNDRY_PROJECT_NAME
- **Name:** `FOUNDRY_PROJECT_NAME`
- **Value:** `action360-agent`
- Click **Add secret**

### Secret 6: FOUNDRY_RESOURCE_GROUP
- **Name:** `FOUNDRY_RESOURCE_GROUP`
- **Value:** `action360-agent-resource`
- Click **Add secret**

### Secret 7: FOUNDRY_SUBSCRIPTION_ID
- **Name:** `FOUNDRY_SUBSCRIPTION_ID`
- **Value:** `f23858ca-331b-4f31-89c1-e2ffa9e5c17c`
- Click **Add secret**

✅ **Verify all 7 secrets are added:**

Go to **Settings > Secrets and variables > Actions** and confirm you see:
- DOCKER_USERNAME
- DOCKER_PASSWORD
- AZURE_CREDENTIALS
- FOUNDRY_PROJECT_ENDPOINT
- FOUNDRY_PROJECT_NAME
- FOUNDRY_RESOURCE_GROUP
- FOUNDRY_SUBSCRIPTION_ID

---

## ✅ STEP 4: Push Code to GitHub (1 min)

```bash
cd c:\src\techrob_action360_agent

# Add new files
git add .

# Commit
git commit -m "feat: add Azure Container Instances deployment"

# Push to GitHub
git push origin main
```

---

## ✅ STEP 5: Watch Deployment (5 min)

1. [ ] Go to: https://github.com/ChrisKoenig/techrob-action360-agent/actions
2. [ ] Click **Deploy to Azure Container Instances** workflow
3. [ ] You should see a running workflow with status ⏳
4. [ ] Watch these steps complete:
   - ✅ Checkout code
   - ✅ Set up Docker Buildx
   - ✅ Log in to Docker Hub
   - ✅ Build and push image (~3-5 min)
   - ✅ Azure Login
   - ✅ Deploy to Azure Container Instances (~2-3 min)
   - ✅ Get Container URL
   - ✅ Test API Health

**First deployment takes 5-10 minutes.** Subsequent deployments are faster due to Docker layer caching.

---

## ✅ STEP 6: Get Your API URL

After the workflow completes successfully:

1. [ ] Go to the workflow logs
2. [ ] Look for the step: **Get Container URL**
3. [ ] Find the line: `✅ API deployed at: http://techrob-action360-api.<region>.azurecontainers.io:8000`
4. [ ] Copy this URL

Or run this command:

```bash
az container show \
  --resource-group rg-techrob-action360 \
  --name techrob-action360-api \
  --query ipAddress.fqdn -o tsv
```

Then add `:8000` to the output.

---

## ✅ STEP 7: Test Your API

```bash
# Replace with your actual URL from Step 6
$apiUrl = "http://techrob-action360-api.<your-region>.azurecontainers.io:8000"

# Test health endpoint
Invoke-WebRequest -Uri "$apiUrl/api/health"

# Should return:
# {"status":"ok","agent_initialized":false}
```

✅ **If you get a 200 response - Deployment is successful!**

---

## 🎉 Next Steps

Your API is now **live and accessible** from anywhere on the internet.

### For M365 Copilot Integration:

1. Save your API URL
2. Go to [TEAMS_INTEGRATION.md](../TEAMS_INTEGRATION.md)
3. Use your URL in the Teams app manifest

### To monitor your container:

```bash
# View logs
az container logs \
  --resource-group rg-techrob-action360 \
  --name techrob-action360-api

# Check status
az container show \
  --resource-group rg-techrob-action360 \
  --name techrob-action360-api
```

### To redeploy (after code changes):

```bash
git add .
git commit -m "fix: update agent logic"
git push origin main
# Workflow runs automatically
```

---

## ❌ Troubleshooting

### "Workflow failed at Docker login"
- Check `DOCKER_PASSWORD` is your **token**, not your password
- Regenerate token at: https://hub.docker.com/settings/security

### "Azure Login failed"
- Verify `AZURE_CREDENTIALS` JSON is correct (no extra whitespace)
- Check subscription ID is correct: `f23858ca-331b-4f31-89c1-e2ffa9e5c17c`

### "Container stuck in Creating state"
- First deployment downloads image (~500MB)
- Takes 1-2 minutes
- Check logs: `az container logs ...`

### "API returns 500 errors"
```bash
az container logs \
  --resource-group rg-techrob-action360 \
  --name techrob-action360-api
```

Check if `FOUNDRY_PROJECT_ENDPOINT` and credentials are correct.

### "API not responding"
- Container may still be starting (check logs)
- HTTPS redirect issue? Try accessing with `http://` not `https://`

---

## 💰 Cost & Resources

**Estimated Monthly Cost:**
- Container Instance: ~$11 (1 CPU, 1.5GB RAM, 24/7)
- Storage: ~$1
- Data transfer: Minimal (<$1)
- **Total: ~$12/month**

To stop charges:
```bash
az container delete \
  --resource-group rg-techrob-action360 \
  --name techrob-action360-api \
  --yes
```

---

**Mark completed steps above as you go! 🚀**
