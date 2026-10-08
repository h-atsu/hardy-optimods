variable "project_id" {
  description = "GCE を作成する Google Cloud プロジェクト ID"
  type        = string
}

variable "region" {
  description = "サブネットを作成するリージョン"
  type        = string
  default     = "asia-northeast1"
}

variable "zone" {
  description = "GCE インスタンスを作成するゾーン"
  type        = string
  default     = "asia-northeast1-b"
}

variable "instance_name" {
  description = "GCE インスタンス名"
  type        = string
  default     = "hardy-optimods-sandbox"

  validation {
    condition     = can(regex("^[a-z]([-a-z0-9]{0,47}[a-z0-9])?$", var.instance_name))
    error_message = "instance_name は小文字、数字、ハイフンを使った 1〜49 文字の名前にしてください。"
  }
}

variable "machine_type" {
  description = "GCE マシンタイプ"
  type        = string
  default     = "e2-medium"
}

variable "boot_disk_size_gb" {
  description = "ブートディスク容量 (GB)"
  type        = number
  default     = 20

  validation {
    condition     = var.boot_disk_size_gb >= 10
    error_message = "boot_disk_size_gb は 10 以上にしてください。"
  }
}

variable "subnet_cidr" {
  description = "検証用サブネットの IPv4 CIDR"
  type        = string
  default     = "10.10.0.0/24"

  validation {
    condition     = can(cidrhost(var.subnet_cidr, 0))
    error_message = "subnet_cidr には有効な IPv4 CIDR を指定してください。"
  }
}

variable "assign_external_ip" {
  description = "VM にエフェメラル外部 IP を付与するか。false の場合は別途 Cloud NAT 等がなければインターネットへ出られません"
  type        = bool
  default     = true
}

variable "labels" {
  description = "GCE インスタンスへ追加するラベル"
  type        = map(string)
  default     = {}
}
