from django.shortcuts import render
from django.http import HttpResponse


def add_to_basket(request, pk):
    return HttpResponse(f"Product {pk} added to basket (placeholder).")
