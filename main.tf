module "rg" {
  source = "./modules/resource_group"

  resource_group_name = var.resource_group_name
  location            = var.location
}

module "storage_account" {
  source = "./modules/storage_account"

  resource_group_name  = module.rg.resource_group_name
  location             = var.location
  storage_account_name = var.storage_account_name
}

module "databricks" {
  source = "./modules/databricks"

  resource_group_name       = module.rg.resource_group_name
  location                  = var.location
  databricks_workspace_name = var.databricks_workspace_name
}

# module "unity_catalog" {
#   source = "./modules/unity_catalog"

#   metastore_name = "custmed-metastore"
#   region         = var.location

#   storage_root = "abfss://unity-metastore@${var.storage_account_name}.dfs.core.windows.net/"

#   workspace_id = module.databricks.workspace_id
# }

# module "rbac" {
#   source = "./modules/rbac"

#   storage_account_id = module.storage_account.storage_account_id
#   databricks_principal_id = module.databricks.managed_identity_principal_id
# }