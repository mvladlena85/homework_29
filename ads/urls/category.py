from django.urls import path

from ads import views
from ads.views import category

urlpatterns = [
    path("", category.CategoriesView.as_view(), name="categories"),
    path("create/", category.CategoryCreateView.as_view(), name="create_category"),
    path("<int:pk>/", category.CategoriesEntityView.as_view(), name="category"),
    path("<int:pk>/update/", category.CategoryUpdateView.as_view(), name="update_category"),
    path("<int:pk>/delete/", category.CategoryDeleteView.as_view(), name="delete_category"),
    ]
