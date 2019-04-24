from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from app.views import *
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.views import obtain_jwt_token
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet


class FCMViewWrap(FCMDeviceAuthorizedViewSet):
    permission_classes = (IsAuthenticated,)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth', obtain_jwt_token),
    path('api/v1/devices', FCMViewWrap.as_view({'post': 'create'}), name='create_fcm_device'),
    path('api/v1/authorize', UserAuthViewSet.as_view()),

    path('api/v1/series', SeriesListViewSet.as_view()),
    path('api/v1/series/<int:pk>', SeriesSingleViewSet.as_view()),
    path('api/v1/series/<int:pk>/answer', UserAnswerViewSet.as_view()),

    ]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
