from utils import pprint
from const import *
import requests
import json

# Docs:
# https://docs.modrinth.com/api/operations/searchprojects/

# Manual usage:
# curl -X GET https://api.modrinth.com/v2/search?query=sodium
# curl -X GET https://api.modrinth.com/v2/project/AANobbMI/version?loaders=%5B%22fabric%22%5D


def request(url, params):
    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"WARNING: {e}")
        return None

    return response.json()


def search_parse_mod(mod: dict):
    return {
        "id": mod["project_id"],
        "name": mod["title"],
        "description": mod["description"],
    }


def search(
    query="",
    limit=5,
    versions=[],
    modloaders=[],
    categories=[],
    client_side=None,
    server_side=None,
):
    assert isinstance(query, str), "Query should be string."
    assert isinstance(limit, int), "Limit should be integer."
    assert isinstance(versions, list), "Versions should be list."
    assert isinstance(modloaders, list), "Modloaders should be list."
    assert isinstance(categories, list), "Categories should be list."

    facets = [["project_type:mod"]]

    if versions:
        facets.append([f"versions:{version}" for version in versions])

    # Modloaders are part of the categories.
    if modloaders:
        facets.append([f"categories:{modloader}" for modloader in modloaders])

    if categories:
        facets.append([f"categories:{category}" for category in categories])

    if client_side is not None:
        facets.append(["client_side:true"])

    if server_side is not None:
        facets.append(["server_side:true"])

    params = {
        "offset": 0,
        "query": query,
        "limit": min(limit, MODRINTH_RESULT_LIMIT),
        "facets": json.dumps(facets),
    }

    mods = []

    while params["limit"] > 0:
        response_data = request(MODRINTH_SEARCH_URL, params)
        if response_data is None:
            response_data = {"hits": [], "total_hits": 0}

        mods.extend(response_data["hits"])

        limit -= params["limit"]
        params["offset"] += params["limit"]
        params["limit"] = min(
            limit,
            response_data["total_hits"] - params["offset"],
            MODRINTH_RESULT_LIMIT,
        )

    return list(map(search_parse_mod, mods))


def show(
    mod_id="",
    versions=[],
    modloaders=[],
):
    params = {}

    if versions:
        params["game_versions"] = json.dumps(versions)

    if modloaders:
        params["loaders"] = json.dumps(modloaders)

    response_data = request(f"{MODRINTH_PROJECT_URL}/{mod_id}/version", params)
    if response_data is None:
        print("ERROR: Could not resolve modId.")
        raise SystemExit

    files = []
    for item in response_data:
        dependencies = []
        for dependency in item["dependencies"]:
            dependencies.append(dependency["project_id"])

        files.append(
            {
                "id": item["id"],
                "name": item["name"],
                "versions": item["game_versions"],
                "modloaders": item["loaders"],
                "url": item["files"][0]["url"],
                "file": item["files"][0]["filename"],
                "dependencies": dependencies,
            }
        )

    return files
