#!/isan/bin/nxpython3
"""Contains an example of JSON data structure normalization with EIGRP neighbors.

When executed, this script prints the quantity of EIGRP adjacencies configured across all EIGRP
processes and VRFs.

Tests for this script can be found in the ./tests/examples/test_eigrp_neighbors.py file.

This script was tested in CML2.1 with Nexus 9000v switches running NX-OS 9.3(7).
"""

from typing import Union
import sys
import json


def command(cmd: str, structured: bool = False) -> Union[str, dict]:
    """Execute a command through NX-OS CLI libraries.

    This function executes an NX-OS CLI command using NX-OS CLI Python
    libraries. NX-OS CLI Python libraries are purposefully abstracted so that
    they are imported in this function instead of at the module level so that
    unit testing outside of a Nexus switch is easier. This is inefficient, but
    stability is valued over speed.

    Parameters
    ----------
    cmd : str
        Command to execute through NX-OS CLI libraries.
    structured : bool, optional
        Indicates whether structured JSON output should be returned instead
        of plaintext. Defaults to False.

    Returns
    -------
    Union[str, dict]
        NX-OS CLI output. A string indicates raw CLI output. A dictionary
        indicates structured output through a JSON data structure.
    """
    if structured:
        from cli import clid

        return normalize_output(json.loads(clid(cmd)))
    from cli import cli

    return cli(cmd)


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


def get_number_of_eigrp_neighbors(data: dict) -> int:
    """Get quantity of EIGRP neighbors on switch.

    Parameters
    ----------
    data : dict

    Returns
    -------
    int
        Number of EIGRP neighbors on switch across all EIGRP processes and VRFs.
    """
    qty = 0
    try:
        asn_data = data["TABLE_asn"]["ROW_asn"]
    except KeyError:
        return qty
    else:
        for asn in asn_data:
            try:
                vrf_data = asn["TABLE_vrf"]["ROW_vrf"]
            except KeyError:
                continue
            else:
                for vrf in vrf_data:
                    try:
                        peer_data = vrf["TABLE_peer"]["ROW_peer"]
                    except KeyError:
                        continue
                    else:
                        qty += len(peer_data)
    return qty


def main():
    """Gather and report the quantity of EIGRP neighbors on the local switch."""
    eigrp_output = command("show ip eigrp neighbors", structured=True)
    number_of_neighbors = get_number_of_eigrp_neighbors(eigrp_output)
    print(f"This switch has {number_of_neighbors} EIGRP neighbors.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
