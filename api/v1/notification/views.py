from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from entities.notification.models import Notification
from libs.authentication import UserAuthentication
from api.v1.serializers import NotificationSerializer, BasicNotificationSerializer
from libs.custom_exceptions import NotificationDoesNotExistsException
from libs.permission import PKNotificationOwnerPermission, PatientDoctorPermission


class NotificationView(ListAPIView):
    """
    View for getting notifications.

    **Example requests**:

        GET /notification/
    """

    authentication_classes = (UserAuthentication,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-id')


class NotificationUpdateView(APIView):
    """
    View for getting notifications.

    **Example requests**:

        GET /notification/{id}/read
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PKNotificationOwnerPermission,)

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk)
            notification.is_read = True
            notification.save(update_fields=['is_read'])

            serializer = BasicNotificationSerializer(notification)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            raise NotificationDoesNotExistsException()


class NotificationAllReadView(APIView):
    """
    View for getting notifications.

    **Example requests**:

        GET /notification/{user_id}/read_all
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientDoctorPermission,)

    def post(self, request, user_id):
        Notification.objects.filter(user_id=user_id).update(is_read=True)
        return Response({}, status=status.HTTP_200_OK)
