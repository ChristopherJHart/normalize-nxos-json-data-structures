"""Contains the `normalize_output` utility function."""


def normalize_output(input: dict) -> dict:
    """Normalize structured output so that table rows are consistently lists.

    The back-end NX-OS uses for structuring data revolves around XML. When this
    XML data is converted to JSON, tables that have more than one row will be
    represented as a list, but tables that have a single row will be
    represented as a dictionary.

    For example, here's a table with a single row:

    {
        "TABLE_ctx": {
            "ROW_ctx": {
                "ptag": "1",
                "cname": "default",
                "nbrcount": "2",
                "TABLE_nbr": {
                    "ROW_nbr": {
                            "rid": "1.1.1.1",
                            "priority": "1",
                            "state": "EXSTART",
                            "drstate": "DR",
                            "uptime": "P14DT19H11M58S",
                            "addr": "192.168.10.10",
                            "intf": "Vlan10"
                    }
                }
            }
        }
    }

    Here's a table with multiple rows. Now that the ROW_nbr key now has a value
    that is a list of dictionaries, instead of a single dictionary:

    {
        "TABLE_ctx": {
            "ROW_ctx": {
                "ptag": "1",
                "cname": "default",
                "nbrcount": "2",
                "TABLE_nbr": {
                    "ROW_nbr": [
                        {
                            "rid": "1.1.1.1",
                            "priority": "1",
                            "state": "EXSTART",
                            "drstate": "DR",
                            "uptime": "P14DT19H11M58S",
                            "addr": "192.168.10.10",
                            "intf": "Vlan10"
                        },
                        {
                            "rid": "100.1.1.2",
                            "priority": "1",
                            "state": "EXCHANGE",
                            "drstate": "DROTHER",
                            "uptime": "P14DT19H11M47S",
                            "addr": "192.168.10.3",
                            "intf": "Vlan10"
                        }
                    ]
                }
            }
        }
    }

    This behavior is maddening to work around consistently.

    This function normalizes all structured output so that any key with the
    phrase "ROW_" in it is converted into a list of dictionaries - even if
    that list only has a single element in it.

    Parameters
    ----------
    input : dict
        JSON data structure returned by NX-OS that should be normalized.

    Returns
    -------
    dict
        Normalized JSON data structure.
    """
    for k, v in input.items():
        if "ROW_" in k and isinstance(v, dict):
            input[k] = [normalize_output(v)]
        elif isinstance(v, dict) and any("ROW_" in x for x in v.keys()):
            input[k] = normalize_output(v)
        # Taste to see if dictionary value is a list and if the list
        # contains dictionaries. This prevents us from needlessly normalizing
        # leaf nodes in the data structure.
        elif isinstance(v, list) and isinstance(v[0], dict):
            for index, item in enumerate(v):
                input[k][index] = normalize_output(item)
    return input
