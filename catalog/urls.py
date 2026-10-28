import pathlib

# I solemnly swear I'm not pasting this where I pasted the several preceding pastes!
# this is in locallibrary/catalog/urls.py which I *just* created
# the current file is definitely NOT locallibrary/locallibrary_config/urls.py!
_this_dir = pathlib.Path(__file__).resolve().parent
assert not (_this_dir / "settings.py").exists(), "catalog/urls.py should NOT have a sibling named settings.py"
assert (_this_dir / "models.py").exists(), "catalog/urls.py should have a sibling named models.py"

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.all_borrowed, name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/create/', views.book_create, name='book-create'),
    path('book/<int:pk>/update/', views.book_update, name='book-update'),
    path('book/<int:pk>/delete/', views.book_delete, name='book-delete'),
    path('author/create/', views.author_create, name='author-create'),
    path('author/<int:pk>/update/', views.author_update, name='author-update'),
    path('author/<int:pk>/delete/', views.author_delete, name='author-delete'),
]