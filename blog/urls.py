from django.urls import path
from . import views
#from .views import AddPostView
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    # ALTERNATIVE path('post/new/', AddPostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish', views.post_publish, name='post_publish'),
    path('post/<pk>/remove', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('category/add/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<str:category>', views.category_view, name='category'),
    path('not_allowed!/', TemplateView.as_view(template_name='blog/not_allowed.html'), name='not_allowed'),
    path('post/<int:pk>/invalid_author', views.post_invalid_author, name='invalid_author')
]