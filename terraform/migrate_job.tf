resource "google_cloud_run_v2_job" "migrate" {
  name                = "photo-album-migrate"
  location            = var.region
  deletion_protection = true

  template {
    template {
      service_account = google_service_account.cloud_run_sa.email

      volumes {
        name = "cloudsql"
        cloud_sql_instance {
          instances = [google_sql_database_instance.postgres.connection_name]
        }
      }

      containers {
        image = var.container_image

        command = ["python"]
        args    = ["manage.py", "migrate", "--noinput"]

        env {
          name  = "DB_NAME"
          value = google_sql_database.app_db.name
        }

        env {
          name  = "DB_USER"
          value = google_sql_user.app_user.name
        }

        env {
          name  = "DB_PASSWORD"
          value = random_password.db_password.result
        }

        env {
          name  = "DB_HOST"
          value = "/cloudsql/${google_sql_database_instance.postgres.connection_name}"
        }

        env {
          name  = "DB_PORT"
          value = "5432"
        }

        env {
          name  = "DJANGO_SECRET_KEY"
          value = var.django_secret_key
        }

        env {
          name  = "MEDIA_BUCKET_NAME"
          value = google_storage_bucket.media.name
        }

        env {
          name  = "USE_GCS"
          value = "true"
        }
      }
    }
  }

  depends_on = [
    google_project_iam_member.run_cloudsql_client,
    google_storage_bucket_iam_member.cloud_run_media_admin
  ]
}