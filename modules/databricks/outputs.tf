# output "managed_identity_principal_id" {
#   value = azurerm_databricks_workspace.dbw.identity[0].principal_id
# }

output "databricks_workspace_url" {
  value = azurerm_databricks_workspace.dbw.workspace_url
}

output "workspace_id" {
  value = azurerm_databricks_workspace.dbw.workspace_id
}