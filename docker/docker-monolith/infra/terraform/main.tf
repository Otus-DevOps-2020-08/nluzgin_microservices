terraform {
  # Версия terraform
  required_version = "0.12.29"
}

provider "google" {
  # Версия провайдера
  version = "2.15.0"
  project = var.project
  region  = var.region
}

resource "google_compute_instance" "app" {
  name         = "${var.app_name}-${count.index}"
  machine_type = "g1-small"
  zone         = var.zone
  tags         = ["docker-machine"]
  count = var.count_of_applications

  boot_disk {
    initialize_params {
      image = var.disk_image
    }
  }
  metadata = {
    # путь до публичного ключа
    ssh-keys = "nluzgin:${file(var.public_key_path)}"
  }

  network_interface {
    network = "default"
    access_config {}
  }

  provisioner "remote-exec" {
    inline = ["sudo docker run -d -p 9292:9292 --network=host funnyfatty/otus-reddit:1.0"]
  }

  connection {
    type  = "ssh"
    host  = self.network_interface[0].access_config[0].nat_ip
    user  = "nluzgin"
    agent = false
    # путь до приватного ключа
    private_key = file(var.private_key_path)
  }
}
