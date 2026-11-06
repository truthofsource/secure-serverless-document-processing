variable "subscription_id" { type = string }
variable "location" {
  type    = string
  default = "eastus2"
}
variable "resource_group_name" { type = string }
variable "tags" {
  type    = map(string)
  default = { environment = "lab", owner = "engineering", cost_center = "training", managed_by = "terraform" }
}

variable "storage_account_name" {
  type = string
  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.storage_account_name))
    error_message = "Choose a globally unique 3-24-character lowercase storage account name."
  }
}

variable "enable_malware_scanning" {
  type    = bool
  default = false
}
variable "enable_event_delivery" {
  type    = bool
  default = false
}
variable "provision_processor_shell" {
  type    = bool
  default = false
}
variable "function_name" {
  type    = string
  default = "func-example-document-processor"
}
variable "integration_subnet_id" {
  type    = string
  default = ""
}
variable "malware_scan_cap_gb_per_month" {
  type    = number
  default = 10
}
