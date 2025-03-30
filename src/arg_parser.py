from utils import info
from const import *


def print_help():
    index = 0
    substitutions = []
    for collection in MODLOADERS, CATEGORIES:
        index = HELP_MESSAGE.find("%s", index + 1)
        indent = HELP_MESSAGE[index::-1].find("\n") - 1
        line_length = indent

        substitution = ""
        for item in collection:
            if line_length != indent and line_length + len(item) > 70:
                line_length = indent
                substitution += "\n" + " " * indent

            substitution += item + ","
            line_length += len(item)

        substitutions.append(substitution.rstrip(",").replace(",", ", "))

    print(HELP_MESSAGE % (*substitutions,))

    raise SystemExit


def get_value_flags(i, flags, iterator):
    values = []

    i += 1
    while i < len(flags) and not flags[i].startswith("-"):
        _, value = next(iterator)
        values.append(value.lower())
        i += 1

    return values


def parse_search_flags(flags):
    params = {"versions": [], "modloaders": [], "categories": []}

    iterator = iter(enumerate(flags))

    # Skip query, if first argument seems to be a flag.
    if flags[0].startswith("--") or flags[0].startswith("-") and len(flags[0]) == 2:
        params["query"] = ""
    else:
        params["query"] = next(iterator)[1]

    for i, flag in iterator:
        if not flag.startswith("-"):
            info(f"Unexpected argument '{flag}' (ignoring).", True, 1)
            continue

        values = get_value_flags(i, flags, iterator)

        match flag:
            case "-v" | "--version":
                params["versions"].extend(values)
            case "-m" | "--modloader":
                for modloader in values:
                    if modloader not in map(str.lower, MODLOADERS):
                        info(f"Unknown modloader '{modloader}'.", True, 2)

                params["modloaders"].extend(values)
            case "-c" | "--category":
                for category in values:
                    if category not in map(str.lower, CATEGORIES):
                        info(f"Unknown category '{category}'.", True, 2)

                params["categories"].extend(values)
            case "-s" | "--source":
                if len(values) < 1:
                    info("Expected argument for source.", True, 2)
                if len(values) > 1:
                    info("Too many values for source.", True, 2)

                source = values[0]
                if source not in map(str.lower, SOURCES):
                    info(f"Unknown source '{source}'.", True, 2)

                params["source"] = source
            case "-l" | "--limit":
                if len(values) < 1:
                    info("Expected number for search limit.", True, 2)
                if len(values) > 1:
                    info("Too many values for search limit.", True, 2)

                value = values[0]
                if not value.isdecimal():
                    info("Expected integer for search limit.", True, 2)

                params["limit"] = int(value)
            case _:
                info(f"Unknown search option '{flag}' (ignoring).", True, 1)
                continue

    return params


def parse_show_flags(flags):
    params = {"versions": [], "modloaders": []}

    iterator = iter(enumerate(flags))
    params["mod_id"] = next(iterator)[1]
    if params["mod_id"].isdecimal():
        params["source"] = "curseforge"
    else:
        params["source"] = "modrinth"

    for i, flag in iterator:
        if not flag.startswith("-"):
            info(f"Unexpected argument '{flag}' (ignoring).", True, 1)
            continue

        values = get_value_flags(i, flags, iterator)
        if len(values) != 1:
            info(f"Expected one value after '{flag}'.", True, 2)

        match flag:
            case "-v" | "--version":
                params["versions"].extend(values)
            case "-m" | "--modloader":
                for modloader in values:
                    if modloader not in map(str.lower, MODLOADERS):
                        info(f"Unknown modloader '{modloader}'.", True, 2)

                params["modloaders"].extend(values)

    return params


def parse_download_flags(flags):
    if len(flags) < 2:
        info("Missing argument modId.", True, 2)

    params = {"versions": [], "modloaders": []}

    iterator = iter(enumerate(flags))
    params["directory"] = next(iterator)[1]
    params["mod_id"] = next(iterator)[1]
    if params["mod_id"].isdecimal():
        params["source"] = "curseforge"
    else:
        params["source"] = "modrinth"

    for i, flag in iterator:
        if not flag.startswith("-"):
            info(f"Unexpected argument '{flag}' (ignoring).", True, 1)
            continue

        values = get_value_flags(i, flags, iterator)
        if len(values) != 1:
            info(f"Expected one value after '{flag}'.", True, 2)

        match flag:
            case "-v" | "--version":
                params["versions"].extend(values)
            case "-m" | "--modloader":
                for modloader in values:
                    if modloader not in map(str.lower, MODLOADERS):
                        info(f"Unknown modloader '{modloader}'.", True, 2)

                params["modloaders"].extend(values)

    return params


def parse_action_args(parser, program, args):
    action = args[0]

    if len(args) < 2:
        info(f"Expected one or more arguments after '{action}'.", program, 2)

    return action, parser(args[1:])


def parse(program_args):
    if len(program_args) < 2:
        info("Expected one or more arguments.", True, 2)

    program, *args = program_args

    match args[0]:
        case "help":
            print_help()
        case "search":
            return parse_action_args(parse_search_flags, program, args)
        case "show":
            return parse_action_args(parse_show_flags, program, args)
        case "download":
            return parse_action_args(parse_download_flags, program, args)
        case _:
            info(f"Unknown argument '{args[0]}'.", program, 2)
