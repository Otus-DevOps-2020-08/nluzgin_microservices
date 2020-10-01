#!/usr/bin/env python
# coding: utf-8

import re
import os
import json
import argparse

import googleapiclient.discovery

appname = 'gitlab-tmp'
# dbname = 'reddit-db'
project = 'docker-286318'
zone = 'us-central1-a'


vars_tmpl = r'''---
host_ip: {IP}'''


def get_instances_info(compute_engines):
    """
    Получение списка инстансов в гугле и информацию по ним
    :return:
    """
    result = compute_engines.instances().list(project=project, zone=zone).execute() or {}
    return result.get('items')


def get_instance_ip_by_name(name, instances):
    """
    Поиск всех ip инстанса по имени
    :param name:
    :param instances:
    :return:
    """
    ip_list = [access_config.get('natIP') for instance in instances
               if instance.get('name') == name
               for network_interface in instance.get('networkInterfaces', [])
               for access_config in network_interface.get('accessConfigs', [])
               if access_config.get('natIP')]
    return ip_list


def get_args():
    """
    Получение входных параметров
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', required=False, action='store_true')
    args = parser.parse_args()
    return args


def renew_ip_in_vars(new_host_ip):
    """
    Обновим db_host: в group_vars/app актуальным значением
    :return:
    """
    # /home/user/OTUS/nluzgin_microservices/gitlab-ci/infra/ansible/group_vars/app

    env_var_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vars.yml')
    # with open(env_var_path, mode='r', encoding='utf-8') as file:
    #     # Читаем старьё
    #     new_content = file.read()
    #     # Ищем старый ip
    #     old_db_host = [line for line in new_content.splitlines() if 'db_host: ' in line][0]
    #     # Меняем старый ip на свеженький
    #     new_content = new_content.replace(old_db_host, 'db_host: ' + new_db_host)

    # Перезаписываем файл
    with open(env_var_path, mode='w', encoding='utf-8') as file:
        file.write(vars_tmpl.format(IP=new_host_ip))


def main():
    """
    Получаем ip и струячим в файлы
    :return:
    """
    args = get_args()
    if args.list:

        compute_engines = googleapiclient.discovery.build('compute', 'v1')
        instances_info = get_instances_info(compute_engines)
        reddit_app_ip_list = get_instance_ip_by_name(name=appname, instances=instances_info)

        inventory = {
            'app': {
                'hosts': [
                    appname
                ]
            },
            '_meta': {
                'hostvars': {
                    appname: {
                        'ansible_host': reddit_app_ip_list[0]  # костыль, ноооо
                    },
                }
            }
        }

        inventory_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'inventory.json')
        with open(inventory_path, mode='w', encoding='utf-8') as inventory_file:
            inventory_string = json.dumps(inventory)
            # именно этого ждёт ansible
            print(inventory_string)
            # Для потомков
            json.dump(inventory, inventory_file, sort_keys=True, indent=3)
            # включаем лень на максималку
            renew_ip_in_vars(reddit_app_ip_list[0])


if __name__ == '__main__':
    main()
