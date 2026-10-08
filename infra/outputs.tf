output "instance_name" {
  description = "作成した GCE インスタンス名"
  value       = google_compute_instance.sandbox.name
}

output "internal_ip" {
  description = "GCE インスタンスの内部 IP"
  value       = google_compute_instance.sandbox.network_interface[0].network_ip
}

output "external_ip" {
  description = "GCE インスタンスの外部 IP。assign_external_ip=false の場合は null"
  value       = try(google_compute_instance.sandbox.network_interface[0].access_config[0].nat_ip, null)
}

output "iap_ssh_command" {
  description = "IAP 経由で SSH 接続するコマンド"
  value       = "gcloud compute ssh ${google_compute_instance.sandbox.name} --project=${var.project_id} --zone=${var.zone} --tunnel-through-iap"
}
