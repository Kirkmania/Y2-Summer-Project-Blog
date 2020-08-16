from django.shortcuts import render
from .forms import CVForm
from .models import CV

# Create your views here.

def cv(request):
    form = CVForm()
    return render(request, 'blog/cv.html', {'form': form})