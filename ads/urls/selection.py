from django.urls import path

from ads import views
from ads.views import selection

urlpatterns = [
    path("", selection.SelectionListView.as_view(), name="categories"),
    path("create/", selection.SelectionCreateView.as_view(), name="create_category"),
    path("<int:pk>/", selection.SelectionEntityView.as_view(), name="category"),
    path("<int:pk>/update/", selection.SelectionUpdateView.as_view(), name="update_category"),
    path("<int:pk>/delete/", selection.SelectionDeleteView.as_view(), name="delete_category"),
    ]
