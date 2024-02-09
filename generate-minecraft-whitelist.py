#!/usr/bin/env python3

import json
import requests
import sys
import time

def read_whitelist():
    try:
        with open("whitelist.json", "r") as whitelist_file:
            whitelist = json.load(whitelist_file)
            username_uuid_map = {entry["name"]: entry["uuid"] for entry in whitelist}
            return username_uuid_map
    except FileNotFoundError:
        return {}

def get_uuid(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        trimmed_uuid = data["id"] # UUID is under the key "id"
        if trimmed_uuid is None:
            print(f"Got UUID 'None' for '{username}', trying again...")
            return get_uuid(username)
        uuid = "-".join([trimmed_uuid[:8], trimmed_uuid[8:12], trimmed_uuid[12:16], trimmed_uuid[16:20], trimmed_uuid[20:]]) # The Minecraft API gives back the UUID without dashes
        return uuid, None
    else:
        return None, response.status_code

def main():
    if len(sys.argv) != 2:
        print("usage: generate-minecraft-whitelist.py <filename>")
        return

    iterated = 0
    username_filepath = sys.argv[1]
    whitelist_entries = []

    try:
        with open(username_filepath, "r") as username_file:
            print("Getting UUIDs for usernames in file:")
            usernames = [line.strip() for line in username_file]

        username_uuid_map = read_whitelist()
        usernames_set = set(usernames)

        for username in sorted(usernames_set, key=str.lower):
            iterated += 1
            uuid = username_uuid_map.get(username)
            uuid_from = "whitelist"
            if not uuid:
                uuid, status_code = get_uuid(username)
                if status_code:
                     if status_code == 404:
                         print(f"[{iterated}/{len(usernames_set)}] (from API) Username: '{username}' does not exist, HTTP status code: 404")
                     elif status_code == 429:
                         print(f"[{iterated}/{len(usernames_set)}] (from API) Rate limited for '{username}', trying again..., HTTP status code: 429")
                         time.sleep(1)
                         uuid, _ = get_uuid(username)
                     else:
                         print(f"[{iterated}/{len(usernames_set)}] (from API) Failed to get UUID for '{username}', HTTP status code: {status_code}")
                uuid_from = "API"
            if uuid:
                print(f"[{iterated}/{len(usernames_set)}] (from {uuid_from}) Username: {username}, UUID: {uuid}")
                whitelist_entry = { # https://minecraft.fandom.com/wiki/Whitelist.json
                    "uuid": uuid,
                    "name": username
                }
                whitelist_entries.append(whitelist_entry)

        with open("whitelist.json", "w") as whitelist_file:
            print("Generating whitelist.json...")
            json.dump(whitelist_entries, whitelist_file, indent=2)

    except FileNotFoundError:
        print(f"error: file '{username_filepath}' does not exist")

if __name__ == "__main__":
    main()
