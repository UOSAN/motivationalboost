from motivationalboost import create_app


def test_config():
    assert create_app({'TESTING': True}).testing
    assert len(create_app({'TESTING': True}).blueprints) == 1
