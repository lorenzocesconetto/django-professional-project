from django.http import response
from django.http import request
import pytest
from pytest_django.asserts import assertContains, assertRedirects

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from everycheese.users.models import User
from ..models import Cheese
from ..views import CheeseCreateView, CheeseDetailView, CheeseListView, CheeseUpdateView
from .factories import CheeseFactory, cheese


pytestmark = pytest.mark.django_db


def test_good_cheese_list_view_expanded(rf):
    '''For reference only, this is redundant with funciton test_good_cheese_list_view()'''
    # Determine the URL
    url = reverse('cheeses:list')
    # rf is pytest shortcut to django.test.RequestFactory
    # We generate a request as if from a user accessing
    # the cheese list view
    request = rf.get(url)
    # Call as_view() to make a callable object
    # callable_obj is analogous to a function-based view
    callable_obj = CheeseListView.as_view()
    # Pass in the request into the callable_obj to get an # HTTP response served up by Django
    response = callable_obj(request)
    # Test that the HTTP response has 'Cheese List' in the
    # HTML and has a 200 response code
    assertContains(response, 'Cheese List')


def test_good_cheese_list_view(rf):
    # Get the request
    request = rf.get(reverse('cheeses:list'))
    # Use the request to get the response
    response = CheeseListView.as_view()(request)
    # Test that the response is valid
    assertContains(response, 'Cheese List')


def test_good_cheese_detail_view(rf, cheese):
    # Make a request for our new cheese
    url = reverse('cheeses:detail', kwargs={'slug': cheese.slug})
    request = rf.get(url)
    # Use the request to get the response
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # Test that the response is valid
    assertContains(response, cheese.name)


def test_good_cheese_create_view(rf, admin_user):
    # Make a request for our new cheese
    request = rf.get(reverse('cheeses:add'))
    # Add an authenticated user
    request.user = admin_user
    # Use the request to get the response
    response = CheeseCreateView.as_view()(request)  # Test that the response is valid
    assert response.status_code == 200


def test_cheese_list_contains_2_cheeses(rf):
    # Let's create a couple cheeses
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    # Create a request and then a response
    # for a list of cheeses
    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)
    # Assert that the response contains both cheese names # in the template.
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)


def test_detail_contains_cheese_data(rf, cheese):
    # Make a request for our new cheese
    url = reverse('cheeses:detail', kwargs={'slug': cheese.slug})
    request = rf.get(url)
    # Use the request to get the response
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # Let's test our Cheesy details!
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)


def test_cheese_create_form_valid(rf, admin_user):
    form_data = {
        'name': 'Paski Sir',
        'description': 'A salty hard cheese',
        'firmness': Cheese.Firmness.HARD
    }
    request = rf.post(reverse('cheeses:add'), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)

    cheese = Cheese.objects.get(name='Paski Sir')

    assert cheese.description == 'A salty hard cheese'
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == admin_user


def test_cheese_create_correct_title(rf, admin_user):
    request = rf.get(reverse('cheeses:add'))
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    assertContains(response, 'Add Cheese')


def test_good_cheese_update_view(rf, admin_user, cheese):
    url = reverse('cheeses:update', kwargs={'slug': cheese.slug})
    request = rf.get(url)
    request.user = admin_user
    response = CheeseUpdateView.as_view()(request, slug=cheese.slug)
    assertContains(response, 'Update Cheese')


def test_cheese_update(rf, admin_user, cheese):
    form_data = {'name': 'new name', 'description': 'new description', 'firmness': Cheese.Firmness.HARD}
    url = reverse('cheeses:update', kwargs={'slug': cheese.slug})
    request = rf.post(url, form_data)
    request.user = admin_user
    response = CheeseUpdateView.as_view()(request, slug=cheese.slug)
    cheese.refresh_from_db()
    assert cheese.name == 'new name'
    assert cheese.description == 'new description'
    assert cheese.firmness == Cheese.Firmness.HARD
