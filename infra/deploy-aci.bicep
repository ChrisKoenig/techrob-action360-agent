metadata description = 'Deploy TechRob Action360 Agent to Azure Container Instances'
metadata author = 'TechRob Team'

param location string = resourceGroup().location
param containerName string = 'techrob-action360'
param containerImage string = 'python:3.11-slim'
param containerPort int = 8000

param foundryProjectEndpoint string
param foundryProjectName string
param foundryResourceGroup string
param foundrySubscriptionId string

param modelDeployment string = 'gpt-4o'
param adoOrgName string = 'UnifiedActionTracker'
param adoProjectName string = 'Unified Action Tracker'
param logLevel string = 'INFO'

// Storage Account for logs
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'sta${uniqueString(resourceGroup().id)}'
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    accessTier: 'Hot'
  }
}

// Container Group
resource containerGroup 'Microsoft.ContainerInstance/containerGroups@2023-05-01' = {
  name: containerName
  location: location
  properties: {
    containers: [
      {
        name: containerName
        properties: {
          image: containerImage
          resources: {
            requests: {
              cpu: 1
              memoryInGB: 1.5
            }
          }
          ports: [
            {
              port: containerPort
              protocol: 'TCP'
            }
          ]
          environmentVariables: [
            {
              name: 'FOUNDRY_PROJECT_ENDPOINT'
              secureValue: foundryProjectEndpoint
            }
            {
              name: 'FOUNDRY_PROJECT_NAME'
              secureValue: foundryProjectName
            }
            {
              name: 'FOUNDRY_RESOURCE_GROUP'
              secureValue: foundryResourceGroup
            }
            {
              name: 'FOUNDRY_SUBSCRIPTION_ID'
              secureValue: foundrySubscriptionId
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
              value: string(containerPort)
            }
            {
              name: 'LOG_LEVEL'
              value: logLevel
            }
          ]

        }
      }
    ]
    osType: 'Linux'
    ipAddress: {
      type: 'Public'
      ports: [
        {
          port: containerPort
          protocol: 'TCP'
        }
      ]
      dnsNameLabel: containerName
    }
    restartPolicy: 'OnFailure'
  }
}

@description('The FQDN of the container group')
output containerGroupFqdn string = containerGroup.properties.ipAddress.fqdn

@description('The public IP address')
output publicIpAddress string = containerGroup.properties.ipAddress.ip

@description('The API endpoint URL')
output apiEndpoint string = 'http://${containerGroup.properties.ipAddress.fqdn}:${containerPort}'
