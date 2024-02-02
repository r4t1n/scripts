#!/usr/bin/env python3

import argparse, os, re, shutil

DOCKER_COMPOSE_FILE_NAMES = ['docker-compose.yml', 'docker-compose.yaml']

def main(args):
    apps_folder = args.path

    if not os.path.exists(apps_folder) or not os.path.isdir(apps_folder):
        print(f'error: The specified path "{apps_folder}" is not valid')
        return

    for app_folder in os.listdir(apps_folder):
        if args.restore:
            restore_docker_version(apps_folder, app_folder)
        else:
            convert_and_backup_docker_version(apps_folder, app_folder)

def restore_docker_version(apps_folder, app_folder):
    for docker_compose_file_name in DOCKER_COMPOSE_FILE_NAMES:
        docker_compose_file_path = os.path.join(apps_folder, app_folder, docker_compose_file_name)

        if os.path.exists(docker_compose_file_path) and os.path.exists(docker_compose_file_path + '.bak'):
            shutil.move(docker_compose_file_path + '.bak', docker_compose_file_path)
        
        print(f'Restored "{docker_compose_file_path}" for "{app_folder}"')

def convert_and_backup_docker_version(apps_folder, app_folder):
    for docker_compose_file_name in DOCKER_COMPOSE_FILE_NAMES:
        docker_compose_file_path = os.path.join(apps_folder, app_folder, docker_compose_file_name)

        if os.path.exists(docker_compose_file_path):
            backup_file_path = docker_compose_file_path + '.bak'
            shutil.copyfile(docker_compose_file_path, backup_file_path)

            with open(docker_compose_file_path, 'r') as docker_compose_file:
                file_content = docker_compose_file.read()
                latest_image_content = re.sub(r'(image: [^:\n]+:)[^ \n]+', r'\1latest', file_content)

            with open(docker_compose_file_path, 'w') as docker_compose_file:
                docker_compose_file.write(latest_image_content)

            print(f'Converted and backupped "{docker_compose_file_path}" for "{app_folder}"')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Script to convert installed CasaOS apps\' docker image version to "latest"')
    parser.add_argument('--path', action='store', default='/var/lib/casaos/apps', help='Path to the CasaOS apps folder (default: /var/lib/casaos/apps)')
    parser.add_argument('--restore', action='store_true', help='Restore the original docker image version')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
