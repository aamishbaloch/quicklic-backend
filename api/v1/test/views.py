from rest_framework.generics import ListAPIView, RetrieveAPIView

from entities.test_menu.models import Test
from libs.authentication import UserAuthentication
from libs.permission import PatientDoctorPermission
from api.v1.serializers import TestSerializer


class TestView(ListAPIView):
    """
    View for listing featured tests.

    **Example requests**:
        GET /test/featured/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientDoctorPermission,)
    serializer_class = TestSerializer
    queryset = Test.objects.filter(is_active=True, is_featured=True).order_by('id')


class TestDetailView(RetrieveAPIView):
    """
    View for getting test details.

    **Example requests**:
        GET /test/{id}
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientDoctorPermission,)
    serializer_class = TestSerializer
    queryset = Test.objects.all()
