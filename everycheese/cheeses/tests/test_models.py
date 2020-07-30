import pytest

from ..models import Cheese
from .factories import CheeseFactory

# Connect to database
pytestmark = pytest.mark.django_db


def test___str__():
    # cheese = Cheese.objects.create(
    #     name="Stracchino", description="Semi-sweet cheese that goes well with starches.", firmness=Cheese.Firmness.SOFT)
    cheese = CheeseFactory()
    assert cheese.__str__() == cheese.name
    assert str(cheese) == cheese.name
