import pytest


def test_init_on_import():
    from graph_builder.config.Config import Config

    # will throw exception, and fail, in the config files can't be found
    assert True
