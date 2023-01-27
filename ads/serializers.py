from rest_framework import serializers

from ads.models import Ads, Selection
from users.models import User


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'


class AdUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ads
        fields = '__all__'


class AdDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ['id']


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(queryset=User.objects.all(),
                                         slug_field='username')
    items = AdSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # owner = serializers.SlugRelatedField(queryset=User.objects.all(),
    #                                      slug_field='username')
    # items = AdSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id']