from rest_framework.generics import ListAPIView, RetrieveAPIView

from entities.clinic.models import Clinic
from entities.test_menu.models import Test
from libs.authentication import UserAuthentication
from libs.permission import PatientDoctorPermission
from api.v1.serializers import TestSerializer, ClinicSerializer


class TestLabView(ListAPIView):
    """
    View for listing test labs.

    **Example requests**:
        GET /test/lab/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientDoctorPermission,)
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.filter(is_active=True, is_lab=True).order_by('id')


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
