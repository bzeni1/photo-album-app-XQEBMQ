variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "europe-west1"
}

variable "service_name" {
  type    = string
  default = "photo-album-app"
}

variable "db_instance_name" {
  type    = string
  default = "photo-album-db"
}

variable "db_name" {
  type    = string
  default = "photoalbum"
}

variable "db_user" {
  type    = string
  default = "photoapp"
}

variable "container_image" {
  type    = string
  default = "europe-west1-docker.pkg.dev/photo-paas/photo-album-repo/photo-album:latest"
}

variable "django_secret_key" {
  type      = string
  sensitive = true
  default   = "temporary-secret"
}

variable "media_bucket_name" {
  type    = string
  default = "photo-paas-photo-album-media"
}