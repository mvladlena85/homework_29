from django.urls import path

from ads.views import ad

urlpatterns = [

    path("", ad.AdsView.as_view(), name="ads"),
    path("create/", ad.AdsCreateView.as_view(), name="create_ad"),
    path("<int:pk>/", ad.AdsEntityView.as_view(), name="full_ad"),
    path("<int:pk>/update/", ad.AdsUpdateView.as_view(), name="update_ad"),
    path("<int:pk>/delete/", ad.delete_ad, name="delete_ad"),
    path('<int:pk>/upload_image/', ad.AdsImageView.as_view(), name="upload_image"),
    ]
