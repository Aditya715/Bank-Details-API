from django.urls import path
from .views import (
    GetAllData, 
    CreateNew, 
    UpdateExisting, 
    UserList
)


urlpatterns = [
    path('users/', UserList.as_view()),
    path('get', GetAllData.as_view(),name="get_all_data"),
    path('create', CreateNew.as_view(),name="create_new"),
    path('update', UpdateExisting.as_view(),name="update"),
]