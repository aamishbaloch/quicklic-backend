from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from entities.notification.models import Notification
from libs.authentication import UserAuthentication
from api.v1.serializers import NotificationSerializer
from libs.custom_exceptions import NotificationDoesNotExistsException
from libs.permission import PKNotificationOwnerPermission


class NotificationView(ListAPIView):
    """
    View for getting notifications.

    **Example requests**:

        GET /notifications/
    """

    authentication_classes = (UserAuthentication,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-id')


class NotificationUpdateView(APIView):
    """
    View for getting notifications.

    **Example requests**:

        GET /notifications/{id}/read
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PKNotificationOwnerPermission,)

    def get(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk)
            notification.is_read = True
            notification.save(update_fields=['is_read'])

            serializer = NotificationSerializer(notification)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            raise NotificationDoesNotExistsException()
