from utils import pretty_json, read_file, pprint
from const import *
import requests
import json

# Docs:
# https://docs.curseforge.com/rest-api/#search-mods


def translate_categories(category):
    match category.lower():
        case "adventure":
            return "adventure and rpg"
        case "cursed":
            return "blood magic"
        case "decoration":
            return "cosmetic"
        case "economy":
            return "farming"
        case "equipment":
            return "armor, tools, and weapons"
        case "food":
            return "food"
        case "game mechanics":
            return "addons"
        case "library":
            return "api and library"
        case "magic":
            return "magic"
        case "management":
            return "server utility"
        case "mobs":
            return "mobs"
        case "optimization":
            return "performance"
        case "social":
            return "education"
        case "storage":
            return "storage"
        case "technology":
            return "technology"
        case "transportation":
            return "player transport"
        case "utility":
            return "utility & qol"
        case "world generation":
            return "world gen"
        case _:
            raise Exception(f"Unexpected category {category}.")


def get_category_ids(categories):
    ids = []

    for category in categories:
        match category.lower():
            case "ores and resources":
                ids.append(408)
            case "food":
                ids.append(436)
            case "miscellaneous":
                ids.append(425)
            case "thermal expansion":
                ids.append(427)
            case "cosmetic":
                ids.append(424)
            case "education":
                ids.append(5299)
            case "buildcraft":
                ids.append(432)
            case "processing":
                ids.append(413)
            case "map and information":
                ids.append(423)
            case "tinker's construct":
                ids.append(428)
            case "technology":
                ids.append(412)
            case "industrial craft":
                ids.append(429)
            case "structures":
                ids.append(409)
            case "farming":
                ids.append(416)
            case "genetics":
                ids.append(418)
            case "magic":
                ids.append(419)
            case "addons":
                ids.append(426)
            case "armor, tools, and weapons":
                ids.append(434)
            case "dimensions":
                ids.append(410)
            case "energy, fluid, and item transport":
                ids.append(415)
            case "server utility":
                ids.append(435)
            case "mobs":
                ids.append(411)
            case "world gen":
                ids.append(406)
            case "player transport":
                ids.append(414)
            case "applied energistics 2":
                ids.append(4545)
            case "energy":
                ids.append(417)
            case "adventure and rpg":
                ids.append(422)
            case "forestry":
                ids.append(433)
            case "storage":
                ids.append(420)
            case "redstone":
                ids.append(4558)
            case "thaumcraft":
                ids.append(430)
            case "blood magic":
                ids.append(4485)
            case "biomes":
                ids.append(407)
            case "api and library":
                ids.append(421)
            case "twitch integration":
                ids.append(4671)
            case "automation":
                ids.append(4843)
            case "crafttweaker":
                ids.append(4773)
            case "mcreator":
                ids.append(4906)
            case "kubejs":
                ids.append(5314)
            case "utility & qol":
                ids.append(5191)
            case "galacticraft":
                ids.append(5232)
            case "skyblock":
                ids.append(6145)
            case "create":
                ids.append(6484)
            case "integrated dynamics":
                ids.append(6954)
            case "performance":
                ids.append(6814)
            case "bug fixes":
                ids.append(6821)
            case "twilight forest":
                ids.append(7669)
            case _:
                raise Exception(f"Unexpected category {category}.")

    return ids


def load_api_key():
    global CURSEFORGE_API_KEY

    try:
        CURSEFORGE_API_KEY = read_file(".env").strip()
    except FileNotFoundError:
        print("WARNING: Expected Curseforge API Key in file .env")
        print("         Curseforge API will not be used.\n")


def request(url, params):
    assert CURSEFORGE_API_KEY, "No Curseforge API Key provided."

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": CURSEFORGE_API_KEY,
    }

    response = requests.get(url, headers=headers, params=params)

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"WARNING: {e}")
        return None

    return response.json()


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

    if not CURSEFORGE_API_KEY:
        return []

    params = {
        "index": 0,
        "searchFilter": query,
        "pageSize": min(limit, CURSEFORGE_RESULT_LIMIT),
        "sortOrder": "desc",
        "gameId": CURSEFORGE_ID_MINECRAFT,
        "classId": CURSEFORGE_ID_MODS,
    }

    # NOTE: Not yet implemented.
    # Curseforge only supports inclusion but not exclusion of client and server side.
    if client_side is True:
        versions = ["Client", *versions]
    if server_side is True:
        versions = ["Server", *versions]

    # Curseforge can filter at most 4 version.
    if versions:
        params["gameVersions"] = json.dumps(versions[:CURSEFORGE_VERSION_LIMIT])

    # Curseforge can filter at most 5 modloaders.
    # If more modloaders are provided, none should be filtered.
    if 1 <= len(modloaders) <= CURSEFORGE_MODLOADER_LIMIT:
        params["modLoaderTypes"] = json.dumps(modloaders)

    # Curseforge can filter at most 10 categories.
    # Curseforge filters categories conjunctively.
    if categories:
        categories = list(map(translate_categories, categories))
        category_ids = get_category_ids(categories[:CURSEFORGE_CATEGORY_LIMIT])
        params["categoryIds"] = json.dumps(category_ids)

    mods = []
    while params["pageSize"] > 0:
        response_data = request(CURSEFORGE_SEARCH_URL, params)
        if response_data is None:
            response_data = {"data": [], "pagination": {"totalCount": 0}}

        mods.extend(response_data["data"])

        limit -= params["pageSize"]
        params["index"] += params["pageSize"]
        params["pageSize"] = min(
            limit,
            response_data["pagination"]["totalCount"] - params["index"],
            CURSEFORGE_RESULT_LIMIT,
        )

    return list(map(parse_mod, mods))


def parse_mod(mod: dict):
    return {
        "id": mod["id"],
        "name": mod["name"],
        "description": mod["summary"],
    }


def show(
    mod_id="",
    versions=[],
    modloaders=[],
):
    params = {}

    if versions:
        params["gameVersion"] = versions[0]

    if modloaders:
        params["modLoaderType"] = modloaders[0]

    response_data = request(f"{CURSEFORGE_PROJECT_URL}/{mod_id}/files", params)
    if response_data is None:
        print("ERROR: Could not resolve modId.")
        raise SystemExit

    files = []
    for item in response_data["data"]:
        dependencies = []
        for dependency in item["dependencies"]:
            # Curseforge also suggests optional dependencies, which can
            # sometimes result in circular and unmatched dependencies.
            if dependency["relationType"] == CURSEFORGE_REQUIRED_DEPENDENCY:
                dependencies.append(dependency["modId"])

        mixed_versions = item["gameVersions"]
        modloaders = []
        versions = []
        for version in mixed_versions:
            if version in MODLOADERS:
                modloaders.append(version)
            else:
                versions.append(version)

        files.append(
            {
                "id": item["id"],
                "name": item["displayName"],
                "versions": versions,
                "modloaders": modloaders,
                "file": item["fileName"],
                "url": item["downloadUrl"],
                "dependencies": dependencies,
            }
        )

    return files
