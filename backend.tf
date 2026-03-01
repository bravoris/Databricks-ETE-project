terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "sttfstatecustmed"
    container_name       = "tfstate"
    key                  = "custmed-dev.terraform.tfstate"
  }
}