from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProtectedView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    def get(self, request: Request) -> Response:
        """Test API for jwt token (delete this later)."""
        return Response(data={"user_id": request.user.user_id})
