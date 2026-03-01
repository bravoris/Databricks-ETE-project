resource "azurerm_role_assignment" "db_storage_access" {
  scope                = var.storage_account_id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = var.databricks_principal_id
}