from . import views
from django.urls import path
app_name = 'blogs'
urlpatterns = [
    path('blogs-list/',                                  views.PostList,                    name='blogs_list'),
    path('',                                  views.public_blog_list,                    name='public_blog_list'),
    path('post-detail-delete/<str:post_id>/',           views.PostDelete,                   name='post_delete'),
    path('create-post/',                                views.create_post_twfl,             name='create_post'),
    path('change-status-is-active/<str:post_id>/',      views.change_status_is_active_twfl, name='change_status_is_active_twfl'),
    path('change_status_publish_twfl/<str:post_id>/',   views.change_status_publish_twfl,   name='change_status_publish_twfl'),
    path('mentor-blog-list/',                           views.PostListAdmin,                name='PostListAdmin'),
    path('medical-school-application/<str:slug>/',                       views.PostDetail,                   name='PostDetail'),
    path('edit-blog-detail/<str:pk>/<str:user_slug>/',             views.edit_post,          name='post_detail_edit'),
    path('add-title-slug/',             views.add_title_slug,          name='add_title_slug'),
]

