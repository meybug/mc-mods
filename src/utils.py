def read_file(path):
    with open(path, "r") as f:
        data = f.read()
    return data


def pretty_json(data, indent=0, depth=-1):
    if isinstance(data, (list, tuple)):
        brackets = "[", "]"
    elif isinstance(data, dict):
        brackets = "{", "}"
    elif isinstance(data, str):
        return '"' + data + '"'
    else:
        return str(data)

    if len(data) == 0 or depth == 0:
        return " ".join(brackets)

    items = []
    if isinstance(data, dict):
        for key, value in data.items():
            items.append(
                " " * (indent + 2)
                + key
                + " = "
                + pretty_json(value, indent + 2, depth - 1)
            )
    else:
        for value in data:
            items.append(" " * (indent + 2) + pretty_json(value, indent + 2, depth - 1))

    return brackets[0] + "\n" + ",\n".join(items) + "\n" + " " * indent + brackets[1]


def pprint(data, depth=-1):
    print(pretty_json(data, depth=depth))


def info(message, hint=True, severity=0):
    prefix = ("INFO", "WARNING", "ERROR")[severity]

    if hint is False:
        print(f"{prefix}: {message}")
    elif hint is True:
        print(f"{prefix}: {message} Try running passing 'help' instead.")
    else:
        print(f"{prefix}: {message} Try running 'python {hint} help' instead.")

    if severity == 2:
        raise SystemExit
