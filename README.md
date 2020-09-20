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
ДЗ №16


1) Сравните вывод команды "docker run -ti --rm --network host joffotron/docker-net-tools -c ifconfig" с "docker-machine ssh docker-host ifconfig":

Вывоз одинаковый, за исключение наличия каких-то стрёмных символов %32544 в ответе от ssh


2) Запустите несколько раз (2-4) команду "docker run --network host -d nginx". Каков результат? Что выдал docker ps? Как думаете почему?


docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
82dfa0b194e7        nginx               "/docker-entrypoint.…"   19 seconds ago      Up 15 seconds                           charming_clarke


Первый вариант ответа - таков путь.

Второй - Занят порт 80, процесс не стартует и завершается с кодом 1 или типа того, умирает pid1, умирает контейнер.
docker logs --tail 100 e6c84e477e46a37afe8afdc519642c3848b414e198e85ea83232f37fe30682fa
...
2020/09/09 17:51:39 [emerg] 1#1: bind() to [::]:80 failed (98: Address already in use)
nginx: [emerg] bind() to [::]:80 failed (98: Address already in use)
2020/09/09 17:51:39 [emerg] 1#1: still could not bind()
nginx: [emerg] still could not bind()


3) Повторите запуски контейнеров с использованием драйверов
none и host и посмотрите, как меняется список namespace-ов.


docker-machine ssh docker-host sudo ip netns
edb196f23d2a
5264ce0e624b
61a2790a0274
4503526581dd
default

В none сетке можно запустить nginx (но зачем? :D) поэтому кроме дефолтовой сетки подвезли ещё + 4 (т.к. 4 раза зпаустил docker run --network none -d nginx).
docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
f6e5c36085bd        nginx               "/docker-entrypoint.…"   2 minutes ago       Up 2 minutes                            modest_golick
426d1314c25c        nginx               "/docker-entrypoint.…"   2 minutes ago       Up 2 minutes                            nostalgic_goldwasser
77cc84d687d7        nginx               "/docker-entrypoint.…"   2 minutes ago       Up 2 minutes                            affectionate_ishizaka
6f9961c427f9        nginx               "/docker-entrypoint.…"   2 minutes ago       Up 2 minutes                            jolly_yalow
28f85913de03        nginx               "/docker-entrypoint.…"   2 minutes ago       Up 2 minutes                            confident_ellis

Всё, что запускалось с host вылилось в один контейнер



   docker run --network host -d nginx
   network_nginx_N.txt

   user@ubuntu:~/OTUS/nluzgin_microservices$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
70eb4ee08fd9        nginx               "/docker-entrypoint.…"   11 seconds ago      Up 10 seconds                           pedantic_borg



 sudo ip netns
 1)
 default

 2) после запуска
RTNETLINK answers: Invalid argument
RTNETLINK answers: Invalid argument
RTNETLINK answers: Invalid argument
bbfdf78a843a
RTNETLINK answers: Invalid argument
netns
default


Узнайте как образуется базовое имя проекта. Можно ли его задать? Если можно то как?

Судя по всему базовое имя проекта зависит от имени папки в которой находится docker-compose.yml.
Изменить можно переименовав папку (что тупо) или задав COMPOSE_PROJECT_NAME
