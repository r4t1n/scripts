#!/usr/bin/env python3

import json
import requests
import sys
import time

def get_uuid(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        trimmed_uuid = data["id"] # UUID is under the key "id"
        if trimmed_uuid is None:
            print(f"Got UUID: None for '{username}', trying again...")
            return get_uuid(username)
        uuid = "-".join([trimmed_uuid[:8], trimmed_uuid[8:12], trimmed_uuid[12:16], trimmed_uuid[16:20], trimmed_uuid[20:]]) # The Minecraft API gives back the UUID without dashes
        return uuid
    elif response.status_code == 404:
        print(f"Got status code '404' when trying to get the UUID for '{username}' (the user does not exist), skipping user")
        return None
    elif response.status_code == 429:
        print(f"Got status code '429' when trying to get the UUID for '{username}' (we have been rate limited), trying again...")
        time.sleep(1)
        return get_uuid(username)
    else:
        print(f"error: unable to get the UUID for '{username}', HTTP status code: '{response.status_code}'")
        return None

def main():
    if len(sys.argv) != 2:
        print("usage: generate-minecraft-whitelist.py <filename>")
        return

    username_filepath = sys.argv[1]
    whitelist_entries = []
    iterated = 0

    try:
        with open(username_filepath, "r") as username_file:
            print("Getting UUIDs for usernames in file:")
            usernames = [line.strip() for line in username_file]

        usernames_set = set(usernames)

        for username in sorted(usernames_set, key=str.lower):
            uuid = get_uuid(username)
            iterated += 1
            if uuid:    
                print(f"[{iterated}/{len(usernames_set)}] Username: {username}, UUID: {uuid}")
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
