resource "azurerm_eventgrid_topic" "scan_results" {
  name                          = "evgt-example-scan-results"
  resource_group_name           = azurerm_resource_group.lab.name
  location                      = var.location
  input_schema                  = "EventGridSchema"
  public_network_access_enabled = true
  local_auth_enabled            = false
  identity { type = "SystemAssigned" }
  tags = var.tags
}
resource "azapi_resource" "result_queue" {
  type      = "Microsoft.Storage/storageAccounts/queueServices/queues@2023-05-01"
  name      = "scan-results"
  parent_id = "${azurerm_storage_account.data.id}/queueServices/default"
  body      = { properties = {} }
}
resource "azapi_resource" "poison_queue" {
  type      = "Microsoft.Storage/storageAccounts/queueServices/queues@2023-05-01"
  name      = "scan-results-poison"
  parent_id = "${azurerm_storage_account.data.id}/queueServices/default"
  body      = { properties = {} }
}
resource "azurerm_role_assignment" "event_sender" {
  count                = var.enable_event_delivery ? 1 : 0
  scope                = azapi_resource.result_queue.id
  principal_id         = azurerm_eventgrid_topic.scan_results.identity[0].principal_id
  principal_type       = "ServicePrincipal"
  role_definition_name = "Storage Queue Data Message Sender"
}
resource "azapi_resource" "queue_subscription" {
  count     = var.enable_event_delivery ? 1 : 0
  type      = "Microsoft.EventGrid/topics/eventSubscriptions@2022-06-15"
  name      = "scan-results-to-queue"
  parent_id = azurerm_eventgrid_topic.scan_results.id
  body = {
    properties = {
      deliveryWithResourceIdentity = {
        destination = {
          endpointType = "StorageQueue"
          properties = {
            queueMessageTimeToLiveInSeconds = 604800
            queueName                       = azapi_resource.result_queue.name
            resourceId                      = azurerm_storage_account.data.id
          }
        }
        identity = { type = "SystemAssigned" }
      }
      eventDeliverySchema = "EventGridSchema"
      filter              = { includedEventTypes = ["Microsoft.Security.MalwareScanningResult"] }
      retryPolicy         = { eventTimeToLiveInMinutes = 1440, maxDeliveryAttempts = 30 }
    }
  }
  depends_on = [azurerm_role_assignment.event_sender]
}
resource "azurerm_security_center_storage_defender" "intake" {
  count                                       = var.enable_malware_scanning ? 1 : 0
  storage_account_id                          = azurerm_storage_account.data.id
  override_subscription_settings_enabled      = true
  malware_scanning_on_upload_enabled          = true
  malware_scanning_on_upload_cap_gb_per_month = var.malware_scan_cap_gb_per_month
  scan_results_event_grid_topic_id            = azurerm_eventgrid_topic.scan_results.id
  sensitive_data_discovery_enabled            = false
}
