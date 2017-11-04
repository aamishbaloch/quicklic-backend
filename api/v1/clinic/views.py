from rest_framework.generics import RetrieveAPIView
from entities.clinic.models import Clinic
from libs.authentication import UserAuthentication
from api.v1.serializers import ClinicSerializer


class ClinicView(RetrieveAPIView):
    """
    View for getting Clinic.

    **Example requests**:

        GET /clinic/{id}
    """

    authentication_classes = (UserAuthentication,)
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
