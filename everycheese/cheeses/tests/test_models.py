import pytest

from .factories import cheese

# Connect to database
pytestmark = pytest.mark.django_db


def test___str__(cheese):
    assert cheese.__str__() == cheese.name
    assert str(cheese) == cheese.name


def test_get_absolute_url(cheese):
    url = cheese.get_absolute_url()
    assert url == f'/cheeses/{cheese.slug}/'
