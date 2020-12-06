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


Задание с *
см. docker-compose.override.yml

ДЗ 16.

Развёрнут сервер gitlab-ci и его runner. Создание машин и настройка делалась руками ибо лень.

Для того, чтобы собрать докер на гитлаб пришлось перерегистрировать агента и поменять ему образ:

sudo docker exec -it gitlab-runner gitlab-runner register -n \
  --url http://35.198.142.9/ \
  --registration-token <TOKEN> \
  --executor docker \
  --description "My Docker Runner" \
  --docker-image "docker:19.03.12" \
  --docker-volumes /var/run/docker.sock:/var/run/docker.sock

ДЗ с *
1) В шаг build добавить сборку контейнера с приложением reddit.

Описание см в шагах build_job и test_unit_job.

2) Деплойте контейнер с reddit на созданный для ветки сервер.

- Предполагается, что тут сервер в гугле развёрнут руками (типа тестовый сервак, катить плейбуками тераформами и т.п. было лень)
- В папке gitlab-ci/reddit_server находится ансибл плейбук, который позволяет разворачивать свежесобранное приложение
- В шаге deploy_dev_job (.gitlab-ci.yml) мы делаем пуш в хаб, а потом запускаем плейбук, который его разворачивает на серваке

ДЗ с **
Продумайте автоматизацию развертывания и регистрации Gitlab CI Runner

1) В папке gitlab-ci/infra находятся ansible playbook'и и pakcer
2) Предполагается, что с помощью pakcer и ansible (плейбук с определёнными тегами) мы готовим образ для запуска gitlab. (скачиваем образы, ставим докеры и т.п.)
3) ИЗ образа пинаем создаём тачку (руками ибо было лень) и на ней раскатываем gitlab UIс помощью указания нужных тегов плейбука. (лапками)
4) В ручную конфигурим админку и тырим токен для ранеров (я почитал как это автоматизировать и чот как-то сложновато, если честно)
5) С помощью ansible и значения переменной runners_count (в дофолтах роли) раскатываем столько раннеров, сколько душе угодно. Скелинг осуществляется с помощью docker-compose, который умеет вместе с ансиблом в поднятие 1+ инстанса

Решение автоматизировано частично, но из соображений экономии времени на дз я позволил себе слегка полениться (и так отстаю)

ДЗ 16.

Добавьте ссылку на докер хаб с вашими образами в README.md и описание PR

https://hub.docker.com/r/funnyfatty/prometheus
https://hub.docker.com/r/funnyfatty/post
https://hub.docker.com/r/funnyfatty/comment
https://hub.docker.com/r/funnyfatty/ui

Задание со * #1
Добавьте в Prometheus мониторинг MongoDB с использованием необходимого экспортера. 

Добавлено блок mongo-exporter, в качестве экспортера образ forekshub/percona-mongodb-exporter:1.0.1
+ бонусом свой экспортер в monitoring/mondo_exporter/Dockerfile только он вышел в разы толще, но я тип потренился.


Задание со * #2
Боль, страдание, безумие.
Добавил
  - job_name: 'cloudprober'
    scrape_interval: 10s
    static_configs:
      - targets:
        - 'blackbox-exporter:9313'
Но не знаю по какой именно причине, но он так и не взлетел. Выдаёт ошибку подключения, хотя вроде бы внешне всё ок. Решил забить, т.к. сильно отстаю по курсу.

Задание со * #2
Makefile d src

ДЗ 17.

Пересобраны приложения с тегом logging.
Создан docker/docker-compose-logging.yml для EFK.
Создан Dockerfile, конфиг для fluentd, сбилжен и отправлен на dockerhub, а также добавлен в logging файл.
Проверен запуск на 2GB RAM, на старте Kiban-ы хост "наглухо" умер с потерей ssh :)
Добавлена настройка для post и ui  для отправки логов в fluentd
Kibana: созданы index-pattern для индекса из потока fluentd, изучены логи приложения.
Добавлен фильтр по json, добавлен фильтр с парсером по явной регулярке в fluentd.
Изучены и добавлены описанные grok шаблоны в конфиг fluentd(распарсены часть полей логов сервиса ui).
Добавлен в docker-compose-logging zipkin - изучены возможности трассировки запросов.

Задание с *
Разбор ещё одного формата логов
Добавил:
grok_pattern service=%{WORD:service} \| event=%{WORD:event} \| path=%{URIPATH:path} \| request_id=%{GREEDYDATA:request_id} \| remote_addr=%{IPORHOST:remote_addr} \| method=%{GREEDYDATA:method} \| response_status=%{NUMBER:response_status}


Задание с *
Траблшутинг UI-экспириенса
Не делал, т.к. сильно отстаю, но подглядел ответы коллег=)


ДЗ 18.

Зи харт вей

Проблемы:
1) В гайде создаётся 3 контроллера и 3 воркера, хотя дефолтная квота - 4 машины
2) sudo systemctl start etcd - для этого и правда нужен паралельный запуск (что показалось мне странным). Ну, всё же пришлось освоить tmux =)

На самом деле всё оказалось довольно просто, т.к. гайд == пошаговая инструкция где весьма сложно налажать. К сожалению особого осознания магии, что там происходила у меня не пришло, но было круто)

Задание с *
Не успеваю

ДЗ 19.

Проблемы при прохождении шагов до ДЗ:
- в гайдах допущены опечатки (kubeclt)
- в гайдах указана устаревшая версия API (apps/v1beta2) нужная и рабочая версия apps/v1
- в гайдах некорректная команда "minikube services list", корректная "minikube service list"
- В моёс миникубе не был включен нужный аддон:
dashboard                   | minikube | disabled     |
Ни слова о том, как его включать в описании дз нет. Соответсвенно иди гугли. Само поисание дз очередной раз показывает отставание от реалей: dashboard не вклчён по дефолту.
- Комнада "kubectl get all -n kube-system --selector k8s-app=kubernetes-dashboard" выводит ничего вообще. Найти аналог того, что указано в ДЗ можно с помощю "kubectl get all -n kube-system"
- в дашборд невозожно попасть с помощью "minikube service kubernetes-dashboard -n kube-system", нужно написать "minikube dashboard"
- команда "kubectl describe service ui -n dev | grep default" не выдаёт ничего. Токен нашел следующим образом: "kubectl -n kube-system describe secret | grep default" -> "kubectl -n kube-system describe secret default-token-2snlk | grep token"


1) Deployment компонента post сконфигурируйте подобным же образом самостоятельно и проверьте его работу. Не забудьте, что post слушает по-умолчанию на порту 5000
см. post-deployment.yml
2) По аналогии создайте объект Service в файле post-service.yml для компонента post (не забудьте про label-ы и правильные tcp-порты).
см. post-service.ymle

ДЗ 20.


1) Обновите mongo-network-policy.yml так, чтобы post-сервис дошел до базы данных.\
см mongo-network-policy.yml

2)Задание:
Создайте пост в приложении
Удалите deployment для mongo
Создайте его заново

Результат: данные в труху

ДЗ 21.

Проблемы при прохождении шагов до ДЗ:
- helm 3й версии релизнулся 15 дней назад. Там нет tiller'a, оказалось надо ставить вторую версию
- Команда "helm install --name test-ui-2 ui/" выдавала ошибку:
Error: render error in "ui/templates/service.yaml": template: ui/templates/service.yaml:13:20: executing "ui/templates/service.yaml" at <.Values.service.externalPort>: nil pointer evaluating interface {}.externalPort

Проблема крылась в том, что values.yaml я закинул в папку templates :D
- Из мануала копируется команда "helm plugin install https://github.com/rimusz/helmtiller" такой репы нет, по факту - пропущен "-" (только при копировании)
- requirements.yaml в ДЗ указан не корректно, пришлось добавлять папку Charts в пути.
- Команда "helm tiller run -- helm upgrade --install --wait --namespace=reddit-ns reddit ./" завершается с ошибкой:
Error: validation failed: unable to recognize "": no matches for kind "Deployment" in version "extensions/v1beta1"

На сколько я понял проблема в ingress.yaml и "apiVersion: extensions/v1beta1"

Замена на apps/v1 приводит к ошибке:
Error: validation failed: [unable to recognize "": no matches for kind "Deployment" in version "extensions/v1beta1", unable to recognize "": no matches for kind "Ingress" in version "apps/v1"]

Замена на networking.k8s.io/v1 приводит к ошибке:
Error: validation failed: [unable to recognize "": no matches for kind "Deployment" in version "extensions/v1beta1", unable to recognize "": no matches for kind "Ingress" in version "networking.k8s.io/v1"]

Для определения какая апи используется в кластере можно запустить команду "kubectl explain ingress" (вместо ingress можно писать deployment или т.п.)
Выровняв все версии с версиями апи кластера ошибки остались прежними.

Вылечелось всё ВНЕЗАПНО и БЕСПОЩАДНО переустановкой самого k8s кластера на версию 15.хх

Client Version: version.Info{Major:"1", Minor:"19", GitVersion:"v1.19.3", GitCommit:"1e11e4a2108024935ecfcb2912226cedeafd99df", GitTreeState:"clean", BuildDate:"2020-10-14T12:50:19Z", GoVersion:"go1.15.2", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"16+", GitVersion:"v1.16.15-gke.4300", GitCommit:"7ed5ddc0e67cb68296994f0b754cec45450d6a64", GitTreeState:"clean", BuildDate:"2020-10-28T09:23:22Z", GoVersion:"go1.13.15b4", Compiler:"gc", Platform:"linux/amd64"}


После этого починилась и команда "helm install --name test-ui-2 ui/"

- Следущая мина была близко:
"Установим наше приложение:
/Charts] $ helm install reddit --name reddit-test"

Первая проблема заключалась в том, что практически полностью отсутсвует контекст и не понятно запускаться надо было из папки nluzgin_microservices/kubernetes/reddit

Вторая заключалась в том, что даже зная где запускаться, всё равно выдавалась ошибка:
$ helm install reddit --name reddit-test
Error: failed to download "reddit" (hint: running `helm repo update` may help)

helm repo update - разумеется не помогал.

Преподователь подсказал выполнить команду:
$ helm install reddit --name reddit-test .
Но, естественно:
Error: This command needs 1 argument: chart name


- Проблемы с установкой gitlab:
helm install --name gitlab . -f values.yaml
WARNING: This chart is deprecated
Error: release gitlab failed: DaemonSet.apps "nginx" is invalid: spec.template.metadata.labels: Invalid value: map[string]string{"app":"nginx"}: `selector` does not match template `labels`

Всё решилось переустановкой кластера (второй раз) на версию 1.15.12-gke.4000

- После поднятия gitlab - не мог зайти в вебморду.

Оказывается Марс в опозиции и месяц красной луны. Ничего не делал - заработало само спустя сутки...

