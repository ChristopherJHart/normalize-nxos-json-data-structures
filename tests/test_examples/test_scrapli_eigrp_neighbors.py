"""Contains unit tests for functions in the scrapli_eigrp_neighbors module."""

import pytest
from examples.scrapli_eigrp_neighbors import get_number_of_eigrp_neighbors


@pytest.mark.parametrize(
    "input, neighbor_count",
    [
        pytest.param(
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
                    ]
                }
            },
            1,
            id="Single process, single VRF, single neighbor",
        ),
        pytest.param(
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
                                                },
                                                {
                                                    "peer_ipaddr": "10.1.0.2",
                                                    "peer_ifname": "Eth1/2",
                                                },
                                            ]
                                        },
                                    }
                                ]
                            },
                        }
                    ]
                }
            },
            2,
            id="Single process, single VRF, two neighbors",
        ),
        pytest.param(
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
                                    },
                                    {
                                        "vrf": "non-default",
                                        "TABLE_peer": {
                                            "ROW_peer": [
                                                {
                                                    "peer_ipaddr": "10.1.0.2",
                                                    "peer_ifname": "Eth1/2",
                                                }
                                            ]
                                        },
                                    },
                                ]
                            },
                        }
                    ]
                }
            },
            2,
            id="Single process, two VRFs, one neighbor each",
        ),
        pytest.param(
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
                                                },
                                                {
                                                    "peer_ipaddr": "10.1.0.2",
                                                    "peer_ifname": "Eth1/2",
                                                },
                                            ]
                                        },
                                    },
                                    {
                                        "vrf": "non-default",
                                        "TABLE_peer": {
                                            "ROW_peer": [
                                                {
                                                    "peer_ipaddr": "10.1.0.3",
                                                    "peer_ifname": "Eth1/3",
                                                },
                                                {
                                                    "peer_ipaddr": "10.1.0.4",
                                                    "peer_ifname": "Eth1/4",
                                                },
                                            ]
                                        },
                                    },
                                ]
                            },
                        }
                    ]
                }
            },
            4,
            id="Single process, two VRFs, two neighbors each",
        ),
        pytest.param(
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
                                                },
                                                {
                                                    "peer_ipaddr": "10.1.0.2",
                                                    "peer_ifname": "Eth1/2",
                                                },
                                            ]
                                        },
                                    },
                                    {
                                        "vrf": "non-default",
                                        "TABLE_peer": {
                                            "ROW_peer": [
                                                {
                                                    "peer_ipaddr": "10.1.0.3",
                                                    "peer_ifname": "Eth1/3",
                                                },
                                                {
                                                    "peer_ipaddr": "10.1.0.4",
                                                    "peer_ifname": "Eth1/4",
                                                },
                                            ]
                                        },
                                    },
                                ]
                            },
                        },
                        {
                            "asn": "2",
                            "TABLE_vrf": {
                                "ROW_vrf": [
                                    {
                                        "vrf": "default",
                                        "TABLE_peer": {
                                            "ROW_peer": [
                                                {
                                                    "peer_ipaddr": "10.1.0.5",
                                                    "peer_ifname": "Eth1/5",
                                                },
                                                {
                                                    "peer_ipaddr": "10.1.0.6",
                                                    "peer_ifname": "Eth1/6",
                                                },
                                            ]
                                        },
                                    },
                                    {
                                        "vrf": "non-default",
                                        "TABLE_peer": {
                                            "ROW_peer": [
                                                {
                                                    "peer_ipaddr": "10.1.0.7",
                                                    "peer_ifname": "Eth1/7",
                                                },
                                                {
                                                    "peer_ipaddr": "10.1.0.8",
                                                    "peer_ifname": "Eth1/8",
                                                },
                                            ]
                                        },
                                    },
                                ]
                            },
                        },
                    ]
                }
            },
            8,
            id="Two processes, two VRFs, two neighbors each",
        ),
    ],
)
def test_get_number_of_eigrp_neighbors(input: dict, neighbor_count: int) -> None:
    """Ensure the `get_number_of_eigrp_neighbors` function returns correct quantity of neighbors."""
    assert get_number_of_eigrp_neighbors(input) == neighbor_count
