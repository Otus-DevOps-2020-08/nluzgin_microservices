# nluzgin_microservices
nluzgin microservices repository 3000 pro

ДЗ №14

Проблемы: команда из дз не отработала:
"docker-machine create --driver google \
 --google-machine-image https://www.googleapis.com/compute/v1/projects/ubuntuos-cloud/global/images/family/ubuntu-1604-lts \
 --google-machine-type n1-standard-1 \
 --google-zone europe-west1-b \
 docker-host"

 Заменил на
 "docker-machine create --driver google --google-machine-image https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/ubuntu-1604-xenial-v20200807 --google-machine-type n1-standard-1 --google-zone europe-west1-b  docker-host"


Сравнить вывод команд.

docker run --rm -ti tehbilly/htop
Видим только саму команду htop в списке процессов. При этом видно все cpu/ram.

docker run --rm --pid host -ti tehbilly/htop
Видим список всех процессов хостовой машины.


ДЗ с *
Всё описано в docker-1.log

ДЗ с **

Создал ансибл плейбуки
Создал образ пакером (при этом использовал плейбуки)
Создал АЖТРИ инстанса с приложением в докере в GCE

.
├── ansible
│   ├── ansible.cfg
│   ├── inventory.json
│   ├── inventory.py
│   ├── playbooks
│   │   └── docker_app.yml
│   └── roles
│       └── docker_full
│           ├── defaults
│           │   └── main.yml
│           ├── files
│           ├── handlers
│           │   └── main.yml
│           ├── meta
│           │   └── main.yml
│           ├── README.md
│           ├── tasks
│           │   └── main.yml
│           ├── templates
│           ├── tests
│           │   ├── inventory
│           │   └── test.yml
│           └── vars
│               └── main.yml
├── packer
│   ├── docker_app.json
│   └── variables.json
└── terraform
    ├── main.tf
    ├── outputs.tf
    ├── terraform.tfstate
    ├── terraform.tfstate.backup
    ├── terraform.tfvars
    └── variables.tf

Всё проверил, всё пашет.
