__author__ = 'najeeb'

from django.conf.urls import include, url
from django.contrib import admin

from book_app.book.views import BooksView
from book_app.genre.views import GenreView
from book_app.user.views import CreateUserView

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/register$', CreateUserView.as_view()),
    url(r'^genre$', GenreView.as_view()),
    url(r'^book$', BooksView.as_view()),
    url(r'^book/(?P<id>[0-9]+)/$',
        BooksView.as_view())
]
