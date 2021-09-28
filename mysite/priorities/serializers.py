from rest_framework import serializers

from accounts.serializers import AccountSerializer
from priorities.models import PrioritiesModel, PrioritiesNameModel


class PrioritiesNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrioritiesNameModel
        fields = '__all__'


class PrioritiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrioritiesModel
        fields = '__all__'


# class PrioritiesCompatibilitySerializer(serializers.ModelSerializer):
class PrioritiesCompatibilitySerializer(serializers.Serializer):
    name = serializers.ReadOnlyField(source='account.name')
    conformance = serializers.ReadOnlyField()
    # priorities_name = PrioritiesNameSerializer(read_only=True)

    # class Meta:
    #     model = PrioritiesModel
    #     fields = '__all__'
    #     fields = ('name', 'conformance')
