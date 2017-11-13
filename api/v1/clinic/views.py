from rest_framework.generics import RetrieveAPIView, ListAPIView
from entities.clinic.models import Clinic
from entities.test_menu.models import Test
from libs.authentication import UserAuthentication
from api.v1.serializers import ClinicSerializer, TestSerializer
from libs.permission import PatientDoctorPermission


class ClinicView(RetrieveAPIView):
    """
    View for getting Clinic.

    **Example requests**:

        GET /clinic/{id}
    """

    authentication_classes = (UserAuthentication,)
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()


class TestView(ListAPIView):
    """
    View for listing clinic's tests.

    **Example requests**:
        GET /clinic/{id}/test/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientDoctorPermission,)
    serializer_class = TestSerializer

    def get_queryset(self):
        return Test.objects.filter(is_active=True, clinic_id=self.kwargs['pk']).order_by('id')
