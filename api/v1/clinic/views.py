from rest_framework.generics import RetrieveAPIView, ListAPIView
from entities.clinic.models import Clinic
from entities.test_menu.models import Test
from libs.authentication import UserAuthentication
from api.v1.serializers import ClinicSerializer, TestSerializer, ReviewSerializer
from libs.custom_exceptions import ClinicDoesNotExistsException
from libs.permission import PatientDoctorPermission
from libs.utils import get_start_datetime_from_date_string, get_end_datetime_from_date_string


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


class ClinicReviewView(ListAPIView):
    """
    View for getting clinic reviews

    **Example requests**:

        GET /clinic/{id}/review/

        **filters**
            doctor_id: Filter with clinic
            start_date: time filter
            end_date: time filter
    """

    authentication_classes = (UserAuthentication,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        try:
            clinic = Clinic.objects.get(pk=int(self.kwargs['pk']))
            reviews = clinic.reviews.all().order_by('created_at')

            if 'doctor_id' in self.request.query_params:
                reviews = reviews.filter(doctor=self.request.query_params.get('doctor_id'))

            if 'start_date' in self.request.query_params:
                start_datetime = get_start_datetime_from_date_string(self.request.query_params.get('start_date'))
                reviews = reviews.filter(created_at__gte=start_datetime)

            if 'end_date' in self.request.query_params:
                end_datetime = get_end_datetime_from_date_string(self.request.query_params.get('end_date'))
                reviews = reviews.filter(created_at__lte=end_datetime)

            return reviews
        except Clinic.DoesNotExist:
            raise ClinicDoesNotExistsException()




