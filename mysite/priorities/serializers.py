from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from priorities.models import PrioritiesModel, PrioritiesNameModel


class PrioritiesNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrioritiesNameModel
        fields = '__all__'


class PrioritiesSerializer(serializers.ModelSerializer):
    account = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = PrioritiesModel
        fields = '__all__'


class PrioritiesCompatibilitySerializer(serializers.Serializer):
    name = serializers.ReadOnlyField(source='account.name')
    conformance = serializers.ReadOnlyField()
