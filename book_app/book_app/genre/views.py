__author__ = 'najeeb'

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book_app.genre.model import Genre
from book_app.utils.messages import ERROR_RESP, NOT_SUPER_USER_ERROR


class GenreView(APIView):
    """
    This view will handle all genre related REST services.
    """
    # Basic Django authentication, you have to pass username nad password to access this api.
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """

        # Making a restriction that only admin user can access genre services
        if request.user.is_active and request.user.is_superuser:
            genres = request.data['genres']
            resp = {}
            genre_resp = []
            duplicates = []

            #  Avoid duplicates in genre
            for genre in genres:
                if not Genre.objects.filter(genre_str=genre):
                    new_genre = Genre(genre_str=genre)
                    new_genre.save()
                    genre_resp.append({"genre": new_genre.genre_str, "genre_id": new_genre.id})
                else:
                    duplicates.append(genre)
            resp['genre_details'] = genre_resp
            resp['genre_duplicates'] = duplicates
            return Response({'data': resp})
        else:
            ERROR_RESP['error']['message'] = NOT_SUPER_USER_ERROR
            return Response(status=status.HTTP_403_FORBIDDEN, data=ERROR_RESP)
