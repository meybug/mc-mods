#!/usr/bin/env python3

from utils import pprint, info
import arg_parser
import curseforge
import modrinth
import requests
import sys
import os


def print_search_results(results):
    for result in results:
        print(f"{result["id"]:<10}{result["name"]}\n{" " * 10}{result["description"]}")
    print("")


def search(params):
    if "source" in params:
        source = [params["source"]]
        del params["source"]
    else:
        source = "curseforge", "modrinth"

    if "curseforge" in source:
        results = curseforge.search(**params)

        print("CurseForge:")
        print_search_results(results)

    if "modrinth" in source:
        results = modrinth.search(**params)

        print("Modrinth:")
        print_search_results(results)


def print_show_results(results):
    for result in results:
        versions = ", ".join(result["modloaders"] + result["versions"])
        dependencies = ", ".join(map(str, result["dependencies"]))

        print(f"{result["id"]:<10}{result["name"]} ({versions})")
        print(f"{" " * 10}{result["url"]}")
        if dependencies:
            print(f"{" " * 10}Dependencies: {dependencies}")
    print("")


def show(params):
    source = params["source"]
    del params["source"]

    if source == "curseforge":
        results = curseforge.show(**params)
    else:
        results = modrinth.show(**params)

    print_show_results(results)


def download(params, downloaded=[]):
    source = params["source"]
    directory = params["directory"]
    if not os.path.exists(directory):
        os.makedirs(directory)

    stripped_params = {
        "mod_id": params["mod_id"],
        "versions": params["versions"],
        "modloaders": params["modloaders"],
    }

    if source == "curseforge":
        results = curseforge.show(**stripped_params)
    else:
        results = modrinth.show(**stripped_params)

    if len(results) == 0:
        info(f"Could not find any matching versions for {params["mod_id"]}", False, 1)
        return

    result = results[0]

    url = result["url"]
    file = result["file"]

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(os.path.join(directory, file), "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"INFO: Downloaded {result["name"]} ({params["mod_id"]})")

    downloaded.append(params["mod_id"])
    for mod_id in result["dependencies"]:
        if mod_id in downloaded:
            info(f"Found circular dependency on {mod_id}", False, 1)
            continue

        params["mod_id"] = mod_id
        download(params, downloaded)


def main():
    args = sys.argv
    action, params = arg_parser.parse(args)

    curseforge.load_api_key()

    if action == "search":
        search(params)
    elif action == "show":
        show(params)
    elif action == "download":
        download(params)


if __name__ == "__main__":
    main()
