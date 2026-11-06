# Infrastructure shell only: no application ZIP, SQL grants or runtime activation.
resource "azurerm_service_plan" "processor" {
  count               = var.provision_processor_shell ? 1 : 0
  name                = "asp-example-document-processor"
  resource_group_name = azurerm_resource_group.lab.name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "FC1"
  tags                = var.tags
}
resource "azurerm_function_app_flex_consumption" "processor" {
  count                                          = var.provision_processor_shell ? 1 : 0
  name                                           = var.function_name
  resource_group_name                            = azurerm_resource_group.lab.name
  location                                       = var.location
  service_plan_id                                = azurerm_service_plan.processor[0].id
  storage_container_type                         = "blobContainer"
  storage_container_endpoint                     = "${azurerm_storage_account.data.primary_blob_endpoint}processor-deployments"
  storage_authentication_type                    = "SystemAssignedIdentity"
  runtime_name                                   = "node"
  runtime_version                                = "22"
  maximum_instance_count                         = 2
  instance_memory_in_mb                          = 2048
  enabled                                        = false
  https_only                                     = true
  public_network_access_enabled                  = false
  webdeploy_publish_basic_authentication_enabled = false
  virtual_network_subnet_id                      = var.integration_subnet_id
  identity { type = "SystemAssigned" }
  site_config {
    minimum_tls_version     = "1.2"
    scm_minimum_tls_version = "1.2"
    http2_enabled           = true
    vnet_route_all_enabled  = true
  }
  app_settings = {
    AzureWebJobsStorage              = ""
    AzureWebJobsStorage__accountName = var.storage_account_name
    AzureWebJobsStorage__credential  = "managedidentity"
    SCAN_PROCESSOR_ENABLED           = "false"
  }
  lifecycle {
    precondition {
      condition     = length(trimspace(var.integration_subnet_id)) > 0
      error_message = "Provide an existing delegated integration subnet and prove the private storage route before provisioning the shell."
    }
  }
  depends_on = [azapi_resource.containers]
  tags       = var.tags
}
