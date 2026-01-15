using './deploy-aci.bicep'

param location = 'eastus'
param containerName = 'techrob-action360-api'
param containerPort = 8000

// Azure AI Foundry Configuration - SET THESE VALUES
param foundryProjectEndpoint = 'https://action360-agent-resource.services.ai.azure.com/api/projects/action360-agent'
param foundryProjectName = 'action360-agent'
param foundryResourceGroup = 'action360-agent-resource'
param foundrySubscriptionId = 'f23858ca-331b-4f31-89c1-e2ffa9e5c17c'

// Model Configuration
param modelDeployment = 'gpt-4o'

// Azure DevOps Configuration
param adoOrgName = 'UnifiedActionTracker'
param adoProjectName = 'Unified Action Tracker'

// API Configuration
param logLevel = 'INFO'
