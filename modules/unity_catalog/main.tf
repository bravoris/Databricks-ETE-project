terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
  }
}

resource "databricks_metastore" "this" {
  name         = var.metastore_name
  storage_root = var.storage_root
  region       = var.region
}

resource "databricks_metastore_assignment" "workspace_assignment" {
  workspace_id = var.workspace_id
  metastore_id = databricks_metastore.this.id
}

resource "databricks_catalog" "lakehouse" {
  name = "lakehouse"

  depends_on = [
    databricks_metastore_assignment.workspace_assignment
  ]
}

resource "databricks_schema" "raw" {
  name         = "raw"
  catalog_name = databricks_catalog.lakehouse.name

  depends_on = [databricks_catalog.lakehouse]
}

resource "databricks_schema" "bronze" {
  name         = "bronze"
  catalog_name = databricks_catalog.lakehouse.name

  depends_on = [databricks_catalog.lakehouse]
}

resource "databricks_schema" "silver" {
  name         = "silver"
  catalog_name = databricks_catalog.lakehouse.name

  depends_on = [databricks_catalog.lakehouse]
}

resource "databricks_schema" "gold" {
  name         = "gold"
  catalog_name = databricks_catalog.lakehouse.name

  depends_on = [databricks_catalog.lakehouse]
}