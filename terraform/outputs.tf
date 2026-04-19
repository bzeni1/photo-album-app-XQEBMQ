output "db_instance_name" {
  value = google_sql_database_instance.postgres.name
}

output "db_connection_name" {
  value = google_sql_database_instance.postgres.connection_name
}

output "db_name" {
  value = google_sql_database.app_db.name
}

output "db_user" {
  value = google_sql_user.app_user.name
}

output "db_password" {
  value     = random_password.db_password.result
  sensitive = true
}

output "cloud_run_url" {
  value = google_cloud_run_v2_service.app.uri
}

output "media_bucket_name" {
  value = google_storage_bucket.media.name
}

output "media_bucket_url" {
  value = "gs://${google_storage_bucket.media.name}"
}