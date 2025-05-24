# authentification/views.py
from django.shortcuts import render

def index(request):
    """
    Rend le fichier HTML principal de l'application frontend.
    """
    return render(request, 'index.html')
def first(request):
    """
    Rend le fichier HTML principal de l'application frontend.
    """
    return render(request, 'first.html')
