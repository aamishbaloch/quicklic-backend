from rest_framework.generics import CreateAPIView

from libs.authentication import UserAuthentication
from libs.permission import PatientPermission
from api.v1.serializers import ReviewSerializer


class ReviewView(CreateAPIView):
    """
    View for creating review.

    **Example requests**:
        POST /review/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientPermission,)
    serializer_class = ReviewSerializer
