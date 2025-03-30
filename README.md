# mcli
A command-line tool for searching and downloading mods from CurseForge and Modrinth.

[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](/LICENSE)

## Usage
```
python3 src/main.py <COMMAND> [OPTIONS]
```

### Commands
- `help` - Show the help page.
- `search <query>` - Search for mods matching a query.
- `show <mod ID>` - Show information and files of a specific mod.
- `download <directory> <mod ID>` - Download a mod by ID, including dependencies.

### Search Options
- `-v, --version <version> ...` - Specify one or more game versions.
- `-m, --modloader <modloader> ...` - Specify one or more modloaders.
- `-s, --source <source>` - Choose the mod source (CurseForge or Modrinth).
- `-c, --category <category> ...` - Filter results by one ore more categories.
- `-l, --limit <number>` - Limit search results. (default: 5)

### Show/Download Options
- `-v, --version <version> ...` - Specify one or more game versions.
- `-m, --modloader <modloader> ...` - Specify one or more modloaders.

## Requirements

- Python 3.x
- Required packages:
  - requests

To install dependencies:
```
pip install requests
```
Alternatively, use the included requirements.txt:
```
pip install -r requirements.txt
```

## Modloaders and Categories
<details>
  <summary>Modloaders</summary>
  Cauldron, Fabric, Forge, LiteLoader, NeoForge, Quilt and Rift
</details>

<details>
  <summary>Categories</summary>
  Same categories as Modrinth uses.
  Use quotes for categories containing spaces.
  
  - Adventure
  - Cursed
  - Decoration
  - Economy
  - Equipment
  - Food
  - Game Mechanics
  - Library
  - Magic
  - Management
  - Mobs
  - Optimization
  - Social
  - Storage
  - Technology
  - Transportation
  - Utility
  - World Generation
</details>

## Examples
```
# Search for 10 Fabric mods with the query "Sodium" in 4 versions:
python3 src/main.py search "Sodium" -m Fabric -v 1.20 1.20.1 20w23a -v 1.20.2 -l 10

# Search for mods on CurseForge from the categories "World Generation" and "Adventure"
python3 src/main.py search "" --source CurseForge --category "World Generation" Adventure

# Show all files of AANobbMI (Sodium on Modrinth) with the version 1.21.5
python3 src/main.py show AANobbMI --version 1.21.5

# Try to download the Fabric mod 394468 (Sodium on CurseForge) with the version 1.21 into ./mods
python3 src/main.py download ./mods 394468 --version 1.21 --modloader Fabric
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Commit your changes (`git commit -m 'Add some amazing feature'`)
- Push to the branch (`git push origin feature/amazing-feature`)
- Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
