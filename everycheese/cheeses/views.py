from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from autoslug import fields

from .models import Cheese


class CheeseListView(ListView):
    model = Cheese


class CheeseDetailView(DetailView):
    model = Cheese


class CheeseCreateView(LoginRequiredMixin, CreateView):
    model = Cheese
    fields = ['name', 'description', 'firmness', 'country_of_origin']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class CheeseUpdateView(LoginRequiredMixin, UpdateView):
    model = Cheese
    fields = ['name', 'description', 'firmness', 'country_of_origin']
    action = 'Update'
