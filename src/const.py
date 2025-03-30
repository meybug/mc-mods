HELP_MESSAGE = """mcli - A command-line tool for searching and downloading mods.

USAGE:
  python3 src/main.py <COMMAND> [OPTIONS]

COMMANDS:
  help                              Show this help page.
  search <query>                    Search for mods matching a query.
  show <mod ID>                     Show information and files of a specific mod.
  download <directory> <mod ID>     Download a mod by ID, including dependencies.

SEARCH OPTIONS:
  -v, --version <version> ...       Specify one or more game versions.
  -m, --modloader <modloader> ...   Specify one or more modloaders.
  -s, --source <source>             Choose the mod source (CurseForge or Modrinth).
  -c, --category <category> ...     Filter results by one ore more categories.
  -l, --limit <number>              Limit search results. (default: 5)

SHOW/DOWNLOAD OPTIONS:
  -v, --version <version> ...       Specify one or more game versions.
  -m, --modloader <modloader> ...   Specify one or more modloaders.

REFERENCE:
  Versions:   Any release, snapshot or preview version (e.g. 1.21.1, 21w14a, 1.17-pre1).
  Modloaders: %s
  Categories: %s

EXAMPLES:
  python3 src/main.py search "Sodium" -m Fabric -v 1.20 1.20.1 20w23a -v 1.20.2 -l 10
  python3 src/main.py search "" --source CurseForge --category "World Generation" Adventure
  python3 src/main.py show AANobbMI --version 1.21.5
  python3 src/main.py download ./mods 394468 --version 1.21 --modloader Fabric
"""

SOURCES = (
    "CurseForge",
    "Modrinth",
)

MODLOADERS = (
    "Cauldron",
    "Fabric",
    "Forge",
    "LiteLoader",
    "NeoForge",
    "Quilt",
    "Rift",
)

CATEGORIES = (
    "Adventure",
    "Cursed",
    "Decoration",
    "Economy",
    "Equipment",
    "Food",
    "Game Mechanics",
    "Library",
    "Magic",
    "Management",
    "Mobs",
    "Optimization",
    "Social",
    "Storage",
    "Technology",
    "Transportation",
    "Utility",
    "World Generation",
)

CURSEFORGE_API_KEY = ""
CURSEFORGE_FILE_URL = "https://edge.forgecdn.net/files"
CURSEFORGE_SEARCH_URL = "https://api.curseforge.com/v1/mods/search"
CURSEFORGE_PROJECT_URL = "https://api.curseforge.com/v1/mods"

CURSEFORGE_ID_MODS = 6
CURSEFORGE_ID_MINECRAFT = 432

CURSEFORGE_RESULT_LIMIT = 50
CURSEFORGE_VERSION_LIMIT = 4
CURSEFORGE_CATEGORY_LIMIT = 10
CURSEFORGE_MODLOADER_LIMIT = 5
CURSEFORGE_REQUIRED_DEPENDENCY = 3

MODRINTH_SEARCH_URL = "https://api.modrinth.com/v2/search"
MODRINTH_PROJECT_URL = "https://api.modrinth.com/v2/project"
MODRINTH_RESULT_LIMIT = 100
