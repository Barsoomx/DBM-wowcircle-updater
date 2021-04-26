#!/usr/bin/env python3x
# -*- coding: utf-8 -*-

import re
import shutil
from datetime import datetime
from pathlib import Path

from dulwich import porcelain

def_repositories = {
    "DBM-wowcircle": {
        "github_user": "Barsoomx",
        "repo_name": "DBM-wowcircle",
        "branch": "master",
        "folder_glob": r"DBM-*"
    },

}


def fetch_repository(github_user, repo_name, branch='master'):
    repo_path = f"./repositories/{repo_name}"
    try:
        Path(f"./repositories").mkdir(exist_ok=True)
        print(f"GIT: Cloning {github_user}/{repo_name}")
        porcelain.clone(f"https://github.com/{github_user}/{repo_name}.git", repo_path, checkout=branch)
    except FileExistsError:
        print(f"GIT: already cloned, fetching updates {github_user}/{repo_name}")

        reset_repository_status(repo_path)
        porcelain.pull(repo_path)

    return Path(repo_path)


def reset_repository_status(repo_path):
    print(f"GIT: Resetting and cleaning {repo_path}")
    porcelain.reset(repo_path, "hard")
    porcelain.clean(repo=repo_path, target_dir=repo_path)


def map_directory(repo_name, folder_glob):
    p = Path("./")

    for _ in p.glob('Wow.exe'):
        print("UPDATER: directory correct, found Wow.exe")

        dt_now = datetime.now().replace(microsecond=0).isoformat().replace(":", "-")
        addons = Path("./Interface/AddOns/")

        backup_path = Path(f"./repositories/{repo_name}-backups/{dt_now}/")

        print(f"BACKUP: backing up current {folder_glob} directories")

        for child in filter_folders(addons, folder_glob):
            backup_path.mkdir(parents=True, exist_ok=True)
            shutil.move(child, backup_path)
            print(f"BACKUP: Backup {child} -> {backup_path}")

        print("BACKUP: Backup finished")

        backups_folder = Path(f"./repositories/{repo_name}-backups/")
        print("BACKUP: Cleaning older backups if they exist... Keeping only last 3")

        sorted_backups = [entry for entry in sorted(backups_folder.iterdir(), key=lambda x: x.name, reverse=True)]
        for path in sorted_backups[3:]:
            print(f"BACKUP: removing {path}")
            shutil.rmtree(path)

        print("BACKUP: Backup clean complete.")

        return addons

    print("UPDATER: directory incorrect, PLEASE place in folder with Wow.exe (WoW root folder)")
    exit(1)


def copy_repository_files(repo_path, addons_folder, folder_glob):
    for child in filter_folders(repo_path, folder_glob):
        shutil.move(child, addons_folder)
        print(f"Installing {child} -> {addons_folder}")

    reset_repository_status(repo_path)


def filter_folders(folder, folder_glob):
    folder_list = folder.glob("*")

    return [x for x in folder_list if x.is_dir() and re.fullmatch(folder_glob, x.name)]


def read_config_file():
    try:
        with open("./repo_config.conf", 'r') as conf:
            upd = dict()
            print(f"CONF: found config")
            for line in conf.readlines():
                if line.startswith("#"): continue  # skip commented lines
                github_user, repo_name, branch, folder_glob = [x.strip() for x in line.split(',')]
                print(f"CONF: found valid config entry: {repo_name}")
                upd.update({repo_name: {
                    "github_user": github_user,
                    "repo_name": repo_name,
                    "branch": branch,
                    "folder_glob": r'{folder_glob}'.format(folder_glob=folder_glob)
                }})

        return upd

    except FileNotFoundError:
        print(f"CONF: config not found, defaulting to DBM-wowcircle")
        return None


def main():
    print(f"UPDATER: SPIN UP")
    repositories = read_config_file() or def_repositories

    for name, repo_data in repositories.items():
        github_user, repo_name, branch, folder_glob = repo_data.values()

        addons_folder = map_directory(repo_name, folder_glob)
        repo_path = fetch_repository(github_user, repo_name, branch)

        copy_repository_files(repo_path, addons_folder, folder_glob)

    print(f"UPDATER: finished for {repositories}")


if __name__ == '__main__':
    main()
