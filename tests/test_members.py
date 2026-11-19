import members


def setup_function():
    members.members.clear()


def test_register_unique_member():
    assert members.register_member(4, "Ari")
    assert not members.register_member(4, "Another Ari")
    assert members.members == [{"id": 4, "name": "Ari"}]
