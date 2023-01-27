import json
import sys

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ads.models import Ads, Categories
from ads.permissions import IsAdOwnerOrStaff
from ads.serializers import AdSerializer, AdUpdateSerializer
from homework_27 import settings
from users.models import User


def get_base_url(request):
    return JsonResponse({"status": "ok"})


class AdsView(ListView):
    model = Ads
    queryset = Ads.objects.order_by('-price')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        categories = request.GET.getlist("cat", None)
        text = request.GET.get("text", None)
        location = request.GET.get("location", None)
        price_from = request.GET.get("price_from", None)
        price_to = request.GET.get("price_to", None)

        if categories:
            self.object_list = self.object_list.filter(category_id__in=categories)
        if text:
            self.object_list = self.object_list.filter(name__icontains=text)
        if location:
            self.object_list = self.object_list.filter(author__locations__name__icontains=location)
        if price_from != 0 or price_to != sys.maxsize:
            self.object_list = self.object_list.filter(price__range=[price_from, price_to])

        paginator = Paginator(self.object_list, per_page=settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        response = {
            "items": [{"id": ad.pk,
                       "name": ad.name,
                       "author": ad.author.first_name,
                       "price": ad.price} for ad in page_object],
            "total": paginator.count,
            "num_pages": paginator.num_pages}

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ads.objects.create(name=ad_data['name'],
                                author=get_object_or_404(User, pk=ad_data['author_id']),
                                price=ad_data['price'],
                                description=ad_data['description'],
                                is_published=ad_data['is_published'],
                                category=get_object_or_404(Categories, pk=ad_data['category_id']),
                                )

        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author_id": ad.author.pk,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "category_id": ad.category.pk,
            "is_published": ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdOwnerOrStaff]

    # @permission_classes([IsAdOwnerOrStaff])
    # def post(self, request):
    #     ad_data = json.loads(request.body)
    #
    #     self.object.name = ad_data['name']
    #     self.object.author = ad_data['author_id']
    #     self.object.price = ad_data['price']
    #     self.object.description = ad_data['description']
    #     self.object.category = ad_data['category_id']
    #
    #     try:
    #         self.object.full_clean()
    #     except ValidationError as e:
    #         return JsonResponse(e.message_dict, status=422)
    #
    #     self.object.save()
    #
    #     return JsonResponse({
    #         "id": self.object.pk,
    #         "name": self.object.name,
    #         "author_id": self.object.author.pk,
    #         "author": self.object.author.first_name,
    #         "price": self.object.price,
    #         "description": self.object.description,
    #         "category_id": self.object.category.pk,
    #         "image": self.object.image.url if self.object.image else None,
    #         "is_published": self.object.is_published
    #     })


class AdsEntityView(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]
    #
    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #
    #     return JsonResponse({
    #         "id": self.object.pk,
    #         "name": self.object.name,
    #         "author": self.object.author.first_name,
    #         "price": self.object.price,
    #         "description": self.object.description,
    #         "category": self.object.category.name,
    #         "image": self.object.image.url if self.object.image else None,
    #         "is_published": self.object.is_published
    #     })


# @method_decorator(csrf_exempt, name='dispatch')
# class AdsDeleteView(DeleteView):
#     model = Ads
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({"status": "ok"}, status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdOwnerOrStaff])
def delete_ad(request, pk):
    ad = Ads.objects.get(pk=pk)
    ad.delete()

    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsImageView(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category', 'image']

    def post(self, request, *args, **kwargs):
        self.object = super().get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "category": self.object.category.name,
            "image": self.object.image.url if self.object.image else None,
            "is_published": self.object.is_published
        })


