# Malware scanner Terraform

Private intake/deployment containers, result and poison queues, a managed-identity Event Grid topic, optional Defender scan configuration and an optional disabled Functions Flex shell.

These configurations adapt the same resource boundaries used in the author's workforce/operations platform. Names and input examples are neutral; no environment state, backend, import block, secret or production identifier is included. Each folder is a standalone reference root, not a command to adopt an existing production resource into new state.

## Code map

| File | Purpose |
| --- | --- |
| [storage.tf](storage.tf) | Private OAuth-only intake storage, private ARM containers and version/deletion protection. |
| [events.tf](events.tf) | Queues, Event Grid identity and opt-in queue delivery/paid scan controls. |
| [processor.tf](processor.tf) | Opt-in Linux Node.js Functions Flex infrastructure shell, always Disabled with basic publishing authentication off. |
| [tests/intake.tftest.hcl](tests/intake.tftest.hcl) | Default-Off paid scanning/event delivery/runtime shell and disabled-worker assertions. |
| [versions.tf](versions.tf) | Exact provider versions; lock file records provider checksums. |
| [example inputs](example.tfvars.example) | Reviewable inputs with placeholders; never actual tenant values. |

## Validate locally without a cloud deployment

```bash
terraform init -backend=false
terraform fmt -check -recursive
terraform validate
terraform test
```

The `.tftest.hcl` files use mock providers and plan commands. They do not authenticate to Azure, create resources or mutate Entra. Provider initialization downloads provider packages; it is not an infrastructure deployment. No automatic Terraform apply is included in GitHub Actions. The existing workflow remains manual-only to avoid unnecessary Actions usage.

The `.tfvars.example` file is not loaded automatically. It contains placeholders and is not ready for a real plan. Leave real `.tfvars`, backend/state, saved plans and credentials outside Git. If you separately deploy a lab, review exact subscription/tenant, names, complete saved plan, permissions, network route, costs and cleanup first. Use a protected remote backend with Entra authentication; this public root deliberately supplies no organization backend.

## Integration boundaries

The actual Node.js processor package, SQL procedures, event journaling, per-container allowlist, private storage route/DNS, dedicated host-storage design and host/data RBAC are commissioning dependencies. The dashboard Python CLI is not an Azure Functions ZIP. Do not deploy it into the Node.js shell. This root deliberately does not claim a functioning scanner after apply.

## Security and activation

Paid Defender scanning, event delivery and shell provisioning are three separate default-Off choices. Before any scan pilot, verify the StorageDataScanner publisher identity/permission, managed-identity queue delivery and private-storage access. The subscription filters only the malware-result event type. Its queue grant does not authenticate an arbitrary JSON event. The processor shell remains Disabled even if provisioned. Before runtime activation, separate host/deployment storage from sensitive intake and grant only dedicated host roles plus exact data/container permissions.

## Cost, retention and cleanup

Storage, Event Grid and any provisioned plan/resources can incur charges. Enabling Defender scanning is a separate paid service decision; its data-volume cap is not an application spending cap. A Disabled worker is not evidence that pending files were scanned.

Mock-test cleanup is entirely local. A real destroy is a separate reviewed action against the correct lab state; never run it against copied production state or shared resources. Retire grants/trust and inventory retained recovery artifacts before removing a real lab.

## Strengths and tradeoffs

The foundation makes the event path reviewable without activating workers or paid scans. It intentionally stops short of an application deployment. Separate host storage and authenticated event handling add resources and operational work but reduce the range of systems a failure could affect.

## Resource inventory

| Terraform resource type | Local name | Definition |
| --- | --- | --- |
| `azurerm_eventgrid_topic` | `scan_results` | [events.tf](events.tf) |
| `azapi_resource` | `result_queue` | [events.tf](events.tf) |
| `azapi_resource` | `poison_queue` | [events.tf](events.tf) |
| `azurerm_role_assignment` | `event_sender` | [events.tf](events.tf) |
| `azapi_resource` | `queue_subscription` | [events.tf](events.tf) |
| `azurerm_security_center_storage_defender` | `intake` | [events.tf](events.tf) |
| `azurerm_resource_group` | `lab` | [main.tf](main.tf) |
| `azurerm_service_plan` | `processor` | [processor.tf](processor.tf) |
| `azurerm_function_app_flex_consumption` | `processor` | [processor.tf](processor.tf) |
| `azurerm_storage_account` | `data` | [storage.tf](storage.tf) |
| `azapi_resource` | `containers` | [storage.tf](storage.tf) |

## Official references

- [Terraform test command and mock providers](https://developer.hashicorp.com/terraform/cli/commands/test)
- [AzureRM provider documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Defender scan-result delivery](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-storage-configure-malware-scan)

See [project architecture](../docs/ARCHITECTURE.md) and [validation evidence](../docs/VALIDATION.md) for the separate application/reference boundaries.
