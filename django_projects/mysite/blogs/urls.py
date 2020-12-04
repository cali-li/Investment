from django.urls import path, reverse_lazy
from . import views

app_name='blogs'
urlpatterns = [
    path('', views.BlogListView.as_view()),
    path('blogs', views.BlogListView.as_view(), name='all'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/create',
        views.BlogCreateView.as_view(success_url=reverse_lazy('blogs:all')), name='blog_create'),
    path('blog/<int:pk>/update',
        views.BlogUpdateView.as_view(success_url=reverse_lazy('blogs:all')), name='blog_update'),
    path('blog/<int:pk>/delete',
        views.BlogDeleteView.as_view(success_url=reverse_lazy('blogs:all')), name='blog_delete'),
    path('blog_picture/<int:pk>', views.stream_file, name='blog_picture'),
    path('blog/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='blog_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('blogs:all')), name='blog_comment_delete'),
    path('blog/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='blog_favorite'),
    path('blog/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='blog_unfavorite'),


]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined
