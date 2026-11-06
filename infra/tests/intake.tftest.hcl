mock_provider "azurerm" {}
mock_provider "azapi" {}
variables {
  subscription_id      = "00000000-0000-0000-0000-000000000001"
  resource_group_name  = "rg-example-documents"
  storage_account_name = "stexampledocuments001"
}
run "paid_scan_delivery_and_runtime_stay_off" {
  command = plan
  assert {
    condition     = length(azurerm_security_center_storage_defender.intake) == 0 && length(azapi_resource.queue_subscription) == 0 && length(azurerm_function_app_flex_consumption.processor) == 0
    error_message = "Paid scans, delivery and worker provisioning must remain opt-in."
  }
  assert {
    condition     = !azurerm_storage_account.data.public_network_access_enabled && !azurerm_eventgrid_topic.scan_results.local_auth_enabled
    error_message = "Keep file ingress private and topic shared keys disabled."
  }
}
run "worker_shell_is_always_disabled" {
  command = plan
  variables {
    provision_processor_shell = true
    integration_subnet_id     = "/subscriptions/00000000-0000-0000-0000-000000000001/resourceGroups/rg-example-network/providers/Microsoft.Network/virtualNetworks/vnet-example/subnets/application"
  }
  assert {
    condition     = !azurerm_function_app_flex_consumption.processor[0].enabled && azurerm_function_app_flex_consumption.processor[0].app_settings["SCAN_PROCESSOR_ENABLED"] == "false"
    error_message = "Do not activate an unpackaged processor."
  }
}
