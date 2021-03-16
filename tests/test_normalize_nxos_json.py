"""Contains unit tests for functions in the normalize_nxos_json module."""

import pytest
from normalize_nxos_json import normalize_output


@pytest.mark.parametrize(
    "input, output",
    [
        pytest.param(
            {"test": "one"},
            {"test": "one"},
            id="Test simple dictionary is not modified",
        ),
        pytest.param(
            {"test": ["one"]},
            {"test": ["one"]},
            id="Test dictionary with list as value is not modified",
        ),
        pytest.param(
            {"ROW_example": {"test": "one"}},
            {"ROW_example": [{"test": "one"}]},
            id="Test dictionary with ROW_ in key and dictionary as value is modified",
        ),
        pytest.param(
            {
                "ROW_vrf": {
                    "TABLE_peer": {"ROW_peer": {"test": "one"}},
                }
            },
            {
                "ROW_vrf": [
                    {
                        "TABLE_peer": {"ROW_peer": [{"test": "one"}]},
                    }
                ]
            },
            id="Test simplified NX-OS routing protocol data structured with nested ROW_ keys",
        ),
        pytest.param(
            {
                "TABLE_asn": {
                    "ROW_asn": {
                        "asn": "1",
                        "TABLE_vrf": {
                            "ROW_vrf": {
                                "vrf": "default",
                                "TABLE_peer": {
                                    "ROW_peer": {
                                        "peer_ipaddr": "10.1.0.1",
                                        "peer_ifname": "Eth1/1",
                                    }
                                },
                            }
                        },
                    },
                }
            },
            {
                "TABLE_asn": {
                    "ROW_asn": [
                        {
                            "asn": "1",
                            "TABLE_vrf": {
                                "ROW_vrf": [
                                    {
                                        "vrf": "default",
                                        "TABLE_peer": {
                                            "ROW_peer": [
                                                {
                                                    "peer_ipaddr": "10.1.0.1",
                                                    "peer_ifname": "Eth1/1",
                                                }
                                            ]
                                        },
                                    }
                                ]
                            },
                        }
                    ],
                }
            },
            id="Test complex NX-OS routing protocol data with multiple processes/VRFs",
        ),
    ],
)
def test_normalize_output(input, output):
    """Tests whether `normalize_output` function works as expected."""
    assert normalize_output(input) == output
