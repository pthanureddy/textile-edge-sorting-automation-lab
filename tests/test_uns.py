import pytest

from textile_edge_sorting.uns import UnsAddress, lab_uns_address


def test_lab_uns_address_builds_asset_state_topic() -> None:
    address = lab_uns_address("line-1")

    assert address.topic("state", "classification") == (
        "portfolio/lab/textile-sorting/line-1/edge-cell/sorter-01/state/classification"
    )


def test_uns_address_rejects_mqtt_wildcards() -> None:
    with pytest.raises(ValueError, match="MQTT wildcards"):
        UnsAddress(
            enterprise="portfolio",
            site="lab",
            area="textile-sorting",
            line="line/+",
            cell="edge-cell",
            asset="sorter-01",
        )


def test_uns_address_requires_information_path() -> None:
    with pytest.raises(ValueError, match="information path"):
        lab_uns_address("line-1").topic()
