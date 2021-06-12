from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from .custom_response import CustomResponse


class CustomViewSet(ModelViewSet):
    """  ViewSetMixin resolve url path tip always """
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return CustomResponse(data=response.data, code=200,
                              msg='ok', success=True)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return CustomResponse(data=response.data, code=200,
                              msg='ok', success=True)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return CustomResponse(data=response.data, code=200,
                              msg='ok', success=True)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return CustomResponse(data=response.data, code=200,
                              msg='ok', success=True)

    def destroy(self, request, *args, **kwargs):
        response=super().destroy(request, *args, **kwargs)

        return CustomResponse(data=response.data, code=200,
                               msg='ok', success=True)
