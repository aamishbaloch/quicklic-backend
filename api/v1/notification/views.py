from rest_framework.generics import ListAPIView
from libs.authentication import UserAuthentication
from api.v1.serializers import NotificationSerializer


class NotificationView(ListAPIView):
    """
    View for getting notifications.

    **Example requests**:

        GET /notifications/
    """

    authentication_classes = (UserAuthentication,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('id')
