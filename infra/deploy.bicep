metadata description = 'Deploy TechRob Action360 Agent to Azure App Service'
metadata author = 'TechRob Team'

param location string = resourceGroup().location
param environment string = 'prod'
param appName string = 'techrob-action360'

param uniqueSuffix string = substring(uniqueString(resourceGroup().id), 0, 6)

param pythonVersion string = '3.11'
param appServiceSkuName string = 'B2'
param appServiceSkuTier string = 'Basic'

@secure()
param foundryProjectEndpoint string
@secure()
param foundryProjectName string
@secure()
param foundryResourceGroup string
@secure()
param foundrySubscriptionId string

param modelDeployment string = 'gpt-4o'
param adoOrgName string = 'UnifiedActionTracker'
param adoProjectName string = 'Unified Action Tracker'
param apiPort string = '8000'
param logLevel string = 'INFO'

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: 'plan-${appName}-${uniqueSuffix}'
  location: location
  sku: {
    name: appServiceSkuName
    tier: appServiceSkuTier
  }
  properties: {
    reserved: true
  }
}

// App Service
resource webApp 'Microsoft.Web/sites@2024-04-01' = {
  name: '${appName}-${environment}-${uniqueSuffix}'
  location: location
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|${pythonVersion}'
      alwaysOn: true
      http20Enabled: true
      minTlsVersion: '1.2'
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        {
          name: 'FOUNDRY_PROJECT_ENDPOINT'
          value: foundryProjectEndpoint
        }
        {
          name: 'FOUNDRY_PROJECT_NAME'
          value: foundryProjectName
        }
        {
          name: 'FOUNDRY_RESOURCE_GROUP'
          value: foundryResourceGroup
        }
        {
          name: 'FOUNDRY_SUBSCRIPTION_ID'
          value: foundrySubscriptionId
        }
        {
          name: 'MODEL_DEPLOYMENT'
          value: modelDeployment
        }
        {
          name: 'ADO_ORG_NAME'
          value: adoOrgName
        }
        {
          name: 'ADO_PROJECT_NAME'
          value: adoProjectName
        }
        {
          name: 'API_PORT'
          value: apiPort
        }
        {
          name: 'LOG_LEVEL'
          value: logLevel
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'ENABLE_ORYX_BUILD'
          value: 'true'
        }
      ]
      connectionStrings: []
    }
    httpsOnly: true
  }
}

// Configure deployment to use local git
resource webAppSourceControl 'Microsoft.Web/sites/basicPublishingCredentialsPolicies@2024-04-01' = {
  parent: webApp
  name: 'ftp'
  properties: {
    allow: false
  }
}

resource webAppScmSourceControl 'Microsoft.Web/sites/basicPublishingCredentialsPolicies@2024-04-01' = {
  parent: webApp
  name: 'scm'
  properties: {
    allow: false
  }
}

// Configure web app to allow deployment from local git or GitHub
resource webAppGitConfig 'Microsoft.Web/sites/sourcecontrols@2024-04-01' = {
  parent: webApp
  name: 'web'
  properties: {
    repoUrl: ''
    branch: ''
    isManualIntegration: false
  }
}

// Application Insights for monitoring
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appinsights-${appName}-${uniqueSuffix}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    RetentionInDays: 30
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Add Application Insights extension to App Service
resource webAppDiagnostics 'Microsoft.Web/sites/config@2024-04-01' = {
  parent: webApp
  name: 'logs'
  properties: {
    applicationLogs: {
      fileSystem: {
        level: 'Verbose'
      }
    }
    httpLogs: {
      fileSystem: {
        enabled: true
        retentionInDays: 7
      }
    }
    failedRequestsTracing: {
      enabled: true
    }
    detailedErrorMessages: {
      enabled: true
    }
  }
}

@description('The URL of the deployed web app')
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'

@description('The app service plan resource ID')
output appServicePlanId string = appServicePlan.id

@description('The web app resource ID')
output webAppId string = webApp.id

@description('The system-assigned managed identity principal ID')
output managedIdentityPrincipalId string = webApp.identity.principalId
