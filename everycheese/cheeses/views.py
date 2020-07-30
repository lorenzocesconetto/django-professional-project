from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from autoslug import fields

from .models import Cheese


class CheeseListView(ListView):
    model = Cheese


class CheeseDetailView(DetailView):
    model = Cheese


class CheeseCreateView(LoginRequiredMixin, CreateView):
    model = Cheese
    fields = ['name', 'description', 'firmness', 'country_of_origin']
