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

ДЗ №15

Обратите внимание! Сборка ui началась не с первого шага. Подумайте - почему?

Судя по логу уже есть необходимый слой для контейнера, поэтому его берут из кеша:
Step 3/13 : ENV APP_HOME /app
 ---> Using cache
 ---> 4eb4fd23635e

 Using cache - указывает на наличие кеша.

Задание с *

Создаём енв файл runtime_containers_vars

Дописываем к именам сеток runtime:

COMMENT_DATABASE_HOST=comment_db_runtime
COMMENT_DATABASE=comments_runtime
POST_DATABASE_HOST=post_db_runtime
POST_DATABASE=posts_runtime
POST_SERVICE_HOST=post_runtime
POST_SERVICE_PORT=5000
COMMENT_SERVICE_HOST=comment_runtime
COMMENT_SERVICE_PORT=9292


Запускаем контейнеры с правленными алиасами (без пересборки)

docker run -d --network=reddit --network-alias=post_db_runtime --network-alias=comment_db_runtime --env-file=./runtime_containers_vars mongo:latest
docker run -d --network=reddit --network-alias=post_runtime --env-file=./runtime_containers_vars funnyfatty/post:1.0
docker run -d --network=reddit --network-alias=comment_runtime --env-file=./runtime_containers_vars funnyfatty/comment:1.0
docker run -d --network=reddit -p 9292:9292 --env-file=./runtime_containers_vars funnyfatty/ui:1.0

Задание с **
Придумайте еще способы уменьшить размер образа:
Собираем образы на специальных alpine образах и удаляем ненужные пакеты в конце

Дополнительные варианты решения уменьшения размера образов можете оформить в виде файла Dockerfile.<цифра> в папке сервиса:
Было бы интересно узнать что можно сделать сверх этого, я не додумался.
