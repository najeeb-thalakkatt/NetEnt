__author__ = 'najeeb'

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from book_app.utils.messages import USER_ALREADY_EXISTS, ERROR_RESP, USER_CREATED


class CreateUserView(APIView):

    """
    The view will create User.
    """

    def post(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """
        username = request.data['username']
        password = request.data['password']
        email = request.data.get('email', None)
        if User.objects.filter(username=username).exists():
            ERROR_RESP['error']['message'] = USER_ALREADY_EXISTS
            return Response(status=status.HTTP_409_CONFLICT, data=ERROR_RESP)
        else:
            user = User.objects.create_user(username, email, password)

        # Building the response
        USER_CREATED['data']['username'] = username
        USER_CREATED['data']['email'] = email
        USER_CREATED['data']['id'] = user.id
        return Response(status=status.HTTP_201_CREATED, data=USER_CREATED)
