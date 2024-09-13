from . import views
from django.urls import path
app_name = 'page'
urlpatterns = [
    path('page-list/',                           views.PostListAdmin,                name='PostListAdmin'),
    # path('',                                  views.public_page_list,                    name='public_page_list'),
    path('page-detail-delete/<str:page_id>/',           views.PostDelete,                   name='page_delete'),
    path('create-page/',                                views.create_page_twfl,             name='create_page'),
    # path('change-status-is-active/<str:page_id>/',      views.change_status_is_active_twfl, name='change_status_is_active_twfl'),
    # path('change_status_publish_twfl/<str:page_id>/',   views.change_status_publish_twfl,   name='change_status_publish_twfl'),
    path('<str:slug>/',                       views.PostDetail,                   name='PostDetail'),
    path('edit-page-detail/<str:pk>/',             views.edit_page,          name='page_detail_edit'),
    # path('add-title-slug/',             views.add_title_slug,          name='add_title_slug'),

]

