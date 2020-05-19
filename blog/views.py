from django.shortcuts import render

# Create your views here.
# NOTE: My first view creation :o
def post_list(request):
    return render(request, 'blog/post_list.html', {})

