__author__ = 'najeeb'

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book_app.book.model import Book
from book_app.genre.model import Genre
from book_app.settings import FREE_BOOK_QUOTA
from book_app.utils.messages import ERROR_RESP, USER_QUOTA_EXCEEDED, USER_NOT_AUTHOR, BOOK_NOT_FOUND


class BooksView(APIView):
    """
    This view will handle all books related REST services.
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
        books = request.data['books']
        author = request.user.username

        # This will return the number of books by a author
        book_numbers = Book.objects.filter(author=author).count()
        response = {}
        resp = []
        duplicate_books = []

        # Free quota check
        if book_numbers < FREE_BOOK_QUOTA:
            for book in books:
                title = book['title']
                genres = book['genres']

                # Check for avoiding the duplicate entry of books
                if Book.objects.filter(book_title=title):
                    duplicate_books.append(book)
                    continue
                book_m = Book(book_title=title, author=author)
                book_m.save()

                # Check for avoiding the duplicate entry of Genres
                for genre in genres:
                    genre_m = Genre.objects.filter(genre_str=genre)
                    if not genre_m:
                        genre_model = Genre(genre_str=genre)
                        genre_model.save()
                        book_m.genres.add(genre_model)
                    else:
                        book_m.genres.add(genre_m[0])
                book['id'] = book_m.id
                resp.append(book)

            # Building the response
            response['duplicate_data'] = duplicate_books
            response['data'] = resp
            return Response(status=status.HTTP_201_CREATED, data=response)

        else:
            ERROR_RESP['error']['message'] = USER_QUOTA_EXCEEDED
            return Response(status=status.HTTP_403_FORBIDDEN, data=ERROR_RESP)

    def put(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """
        try:
            # Parsing the book data and checking for book entry
            book = request.data
            books = Book.objects.filter(id=book['id'])[0]
            if books:
                book_m = books[0]

                # Check if the logged in user and author is same
                if book_m.author != request.user.username:
                    ERROR_RESP['error']['message'] = USER_NOT_AUTHOR
                    return Response(status=status.HTTP_403_FORBIDDEN,
                                    data=ERROR_RESP)
                else:
                    genres = book.get('genres', None)

                    # Checks to avoid duplicate genres
                    if genres:
                        for genre in genres:
                            genre_m = Genre.objects.filter(genre_str=genre)
                            if not genre_m:
                                genre_model = Genre(genre_str=genre)
                                genre_model.save()
                                book_m.genres.add(genre_model)
                            else:
                                book_m.genres.add(genre_m[0])

                        del book['genres']  # genres are already updated so removing it.
                        Book.objects.filter(id=book['id']).update(**book)
            else:
                # Error response in case of no book found
                ERROR_RESP['error']['message'] = BOOK_NOT_FOUND
                return Response(status=status.HTTP_404_NOT_FOUND,
                                data=ERROR_RESP)
        except Exception as e:
            ERROR_RESP['error']['message'] = e.message
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=ERROR_RESP)
        return Response(status=status.HTTP_200_OK, data=book)

    def get(self, request, id, format=None):
        """
        :param request:
        :param id:
        :param format:
        :return:
        """
        try:
            # Fetching the book details
            books = Book.objects.filter(id=id)
            if books:
                book_m = books[0]

                #  Checking for the author
                if book_m.author != request.user.username:
                    ERROR_RESP['error']['message'] = USER_NOT_AUTHOR
                    return Response(status=status.HTTP_403_FORBIDDEN,
                                    data=ERROR_RESP)
                else:
                    # Building the response
                    book = dict()
                    book['id'] = book_m.id
                    book['author'] = book_m.author
                    book['title'] = book_m.book_title
                    book['genres'] = book_m.genres.values()
                    return Response(status=status.HTTP_200_OK, data=book)
            else:
                ERROR_RESP['error']['message'] = BOOK_NOT_FOUND
                return Response(status=status.HTTP_404_NOT_FOUND,
                                data=ERROR_RESP)

        except Exception as e:
            ERROR_RESP['error']['message'] = e.message
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=ERROR_RESP)
