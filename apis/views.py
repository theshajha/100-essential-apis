# from rest_framework.parsers import MultiPartParser
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.viewsets import ModelViewSet
#
# from odyssey.utils.base_functions import CookieJWTAuthentication
# from odyssey.utils.base_functions import MultiSerializerViewSetMixin
# from .models import *
#
# from django.db.models import Q
#
#
# # Cache
#
#
# # from odyssey.mixpanel_util import mp
#
#
# class ApiListViewSet(MultiSerializerViewSetMixin, ModelViewSet):
#     authentication_classes = [CookieJWTAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = ApiListSerializer
#     parser_classes = (NoUnderscoreBeforeNumberCamelCaseJSONParser, MultiPartParser)
#     serializer_action_classes = {
#         'retrieve': ApiRetrieveSerializer,
#     }
#
#     def get_queryset(self, *args, **kwargs):
#         keyword = self.request.query_params.get('keyword', None)
#         category = self.request.query_params.get('category', None)
#
#         queryset = ApiList.objects.filter(is_active=True, status__in=['LIVE', 'BETA', 'COMING_SOON', 'DEPRECATED'])
#         if keyword:
#             queryset = queryset.filter(Q(name__icontains=keyword) |
#                                        Q(description__icontains=keyword))
#
#         if category:
#             queryset = queryset.filter(category_id=category)
#
#         return queryset