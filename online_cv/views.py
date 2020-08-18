from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CVForm
from .models import CV

# Create your views here.
@login_required
def cv(request):
    form = CVForm()
    return render(request, 'online_cv/cv.html', {'form': form})