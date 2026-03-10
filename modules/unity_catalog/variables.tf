variable "metastore_name" {
  description = "Unity Catalog metastore name"
  type        = string
}

variable "region" {
  description = "Region for Unity Catalog metastore"
  type        = string
}

variable "storage_root" {
  description = "Storage location for Unity Catalog metastore"
  type        = string
}

variable "workspace_id" {
  description = "Databricks workspace id"
  type        = string
}