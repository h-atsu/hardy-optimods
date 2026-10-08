resource "google_project_service" "apis" {
  for_each = toset([
    "compute.googleapis.com",
    "iam.googleapis.com",
    "iap.googleapis.com",
    "oslogin.googleapis.com",
  ])

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_compute_network" "sandbox" {
  name                    = "${var.instance_name}-network"
  project                 = var.project_id
  auto_create_subnetworks = false

  depends_on = [google_project_service.apis]
}

resource "google_compute_subnetwork" "sandbox" {
  name                     = "${var.instance_name}-subnet"
  project                  = var.project_id
  region                   = var.region
  network                  = google_compute_network.sandbox.id
  ip_cidr_range            = var.subnet_cidr
  private_ip_google_access = true
}

# IAP TCP forwarding の送信元だけに SSH を許可する。
resource "google_compute_firewall" "iap_ssh" {
  name      = "${var.instance_name}-allow-iap-ssh"
  project   = var.project_id
  network   = google_compute_network.sandbox.name
  direction = "INGRESS"
  priority  = 1000

  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["iap-ssh"]

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}

resource "google_service_account" "instance" {
  account_id   = trim(substr("gce-${var.instance_name}-vm", 0, 30), "-")
  display_name = "${var.instance_name} VM"
  project      = var.project_id

  depends_on = [google_project_service.apis]
}

data "google_compute_image" "debian" {
  project = "debian-cloud"
  family  = "debian-12"

  depends_on = [google_project_service.apis]
}

resource "google_compute_instance" "sandbox" {
  name                      = var.instance_name
  project                   = var.project_id
  zone                      = var.zone
  machine_type              = var.machine_type
  allow_stopping_for_update = true
  deletion_protection       = false
  tags                      = ["iap-ssh"]

  labels = merge(
    {
      environment = "sandbox"
      managed-by  = "terraform"
    },
    var.labels,
  )

  boot_disk {
    auto_delete = true

    initialize_params {
      image = data.google_compute_image.debian.self_link
      size  = var.boot_disk_size_gb
      type  = "pd-balanced"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.sandbox.id

    dynamic "access_config" {
      for_each = var.assign_external_ip ? [1] : []
      content {}
    }
  }

  metadata = {
    enable-oslogin         = "TRUE"
    block-project-ssh-keys = "TRUE"
  }

  service_account {
    email  = google_service_account.instance.email
    scopes = ["cloud-platform"]
  }

  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    provisioning_model  = "STANDARD"
  }
}
