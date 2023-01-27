import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from rest_framework.exceptions import ValidationError

from ads.models import Categories


class CategoriesView(ListView):
    model = Categories
    queryset = Categories.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('name')

        response = [{"id": cat.pk,
                     "name": cat.name} for cat in self.object_list]
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Categories
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)

        cat = Categories.objects.create(name=cat_data['name'])
        return JsonResponse({
            "id": cat.pk,
            "name": cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Categories
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)
        super().post(request, *args, **kwargs)

        self.object.name = cat_data['name']

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name
        })


class CategoriesEntityView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        cat = get_object_or_404(Categories, *args, **kwargs)

        return JsonResponse({
            "id": cat.pk,
            "name": cat.name
        })


class CategoryDeleteView(DeleteView):
    model = Categories
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)
