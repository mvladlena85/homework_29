from rest_framework import serializers
from rest_framework.fields import empty

from users.models import User, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name']


class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        extra_kwargs = {'name': {'required': True, 'allow_blank': False}}


class UserSerializer(serializers.ModelSerializer):
    # locations = LocationSerializer(many=True)
    locations = serializers.SlugRelatedField(many=True,
                                             read_only=True,
                                             slug_field='name')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'age', 'locations']


class UserCreateSerializer(serializers.ModelSerializer):
    # locations = LocationSerializer(many=True)
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(required=False,
                                             many=True,
                                             queryset=Location.objects.all(),
                                             slug_field='name')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'age', 'locations']

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.locations.add(location_obj)

        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(required=False,
                                             many=True,
                                             queryset=Location.objects.all(),
                                             slug_field='name')
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations')
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        user.locations.all().delete()

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.locations.add(location_obj)

        user.save()
        return user


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
