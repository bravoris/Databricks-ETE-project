output "managed_identity_principal_id" {
  value = azurerm_databricks_workspace.dbw.identity[0].principal_id
}