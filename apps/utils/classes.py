# Vendor
from datetime import datetime
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# Local
from apps.utils.permissions import MixedPermission
from apps.utils.exceptions import CustomException


class Pagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_param = 'page'

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request)
        page_count = self.page.paginator.count // page_size
        if self.page.paginator.count % page_size != 0:
            page_count += 1

        return Response({
            'next': True if self.get_next_link() else False,
            'previous': True if self.get_previous_link() else False,
            'count': self.page.paginator.count,
            'pageCount': page_count,
            'results': data
        })


class MixedSerializer:
    """ Serializer action's mixin
    """
    def get_serializer(self, *args, **kwargs):
        try:
            serializer_class = self.serializer_classes_by_action[self.action]
        except KeyError:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class ListModelMixinOrdered(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListModelMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        # request.data._mutable = True
        request.data["created_by_user"] = request.user.id
        # request.data._mutable = False
        return super().create(request, *args, **kwargs)


class UpdateModelMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        # request.data._mutable = True
        request.data['updated_by_user'] = request.user.id
        # request.data._mutable = False
        return super().update(request, *args, **kwargs)


class DestroyModelMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.deleted_by_user = request.user
            instance.deleted_at = datetime.now()
            instance.save()
            return Response({"Объект удален"}, status=status.HTTP_200_OK)
        except:
            raise CustomException(
                translate_code="object_not_found", code=status.HTTP_404_NOT_FOUND)


class CreateListRetrieveNoPermissions(CreateModelMixin,
                                      ListModelMixinOrdered,
                                      mixins.RetrieveModelMixin,
                                      viewsets.GenericViewSet):
    pass


class CreateListRetrieve(MixedPermission,
                         CreateModelMixin,
                         ListModelMixinOrdered,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    pass


class CreateListRetrieveDestroy(MixedPermission,
                                CreateModelMixin,
                                ListModelMixinOrdered,
                                DestroyModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


class CreateRetrieveDestroy(MixedPermission,
                            CreateModelMixin,
                            DestroyModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    pass


class CreateUpdateListRetrieve(MixedPermission,
                               CreateModelMixin,
                               ListModelMixinOrdered,
                               UpdateModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    pass


class CreateUpdateListRetrieveDestroy(MixedPermission,
                                      CreateModelMixin,
                                      ListModelMixinOrdered,
                                      DestroyModelMixin,
                                      UpdateModelMixin,
                                      mixins.RetrieveModelMixin,
                                      viewsets.GenericViewSet):
    pass


class RetrieveViewSet(MixedPermission,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):

    pass

class ListRetrieve(MixedPermission,
                   ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    pass