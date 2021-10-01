from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from priorities.models import PrioritiesModel, PrioritiesNameModel
from priorities.permissions import IsAuthorOrReadOnly
from priorities.serializers import PrioritiesSerializer, PrioritiesNameSerializer, PrioritiesCompatibilitySerializer
from priorities.utils import method_conformance


class PrioritiesViewSet(viewsets.ModelViewSet):
    serializer_class = PrioritiesSerializer
    permission_classes = [IsAuthenticated]#[IsAuthorOrReadOnly]

    def get_queryset(self):
        return PrioritiesModel.objects.filter(account=self.request.user)

    @extend_schema(request=PrioritiesCompatibilitySerializer, responses={200: None})
    @action(detail=False, methods=['get'], name='Compatibility list',
            permission_classes=[IsAuthenticated])
    def compatibility_list(self, request):
        user_account = request.user
        data = method_conformance(user_account)
        return Response(status=status.HTTP_200_OK, data=data)


class PrioritiesNameViewSet(viewsets.ModelViewSet):
    serializer_class = PrioritiesNameSerializer
    queryset = PrioritiesNameModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
