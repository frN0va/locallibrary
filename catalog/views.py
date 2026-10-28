from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

# Create your views here.

from .forms import AuthorForm, BookForm, RenewBookForm
from .models import Author, Book, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Challenge: counts for genres and books containing a particular word (case insensitive)
    num_genres = Genre.objects.filter(name__icontains='fiction').count()
    num_books_with_word = Book.objects.filter(title__icontains='the').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_word': num_books_with_word,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book


class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author


class LoanedBooksByUserListView(generic.ListView):
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status__exact="o",
        ).order_by("due_back")


@login_required
@permission_required("catalog.can_mark_returned", raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == "POST":
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save(update_fields=["due_back"])
            return redirect("all-borrowed")
    else:
        form = RenewBookForm(initial={"renewal_date": book_instance.due_back})
    return render(request, "catalog/bookinstance_renew.html", {
        "form": form,
        "bookinst": book_instance,
    })


@login_required
@permission_required("catalog.can_mark_returned", raise_exception=True)
def all_borrowed(request):
    instances = BookInstance.objects.filter(status__exact="o").select_related(
        "book", "borrower"
    )
    return render(request, "catalog/bookinstance_list_all_borrowed.html", {
        "bookinstance_list": instances,
    })


@login_required
@permission_required("catalog.add_book", raise_exception=True)
def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        return redirect(form.save().get_absolute_url())
    return render(request, "catalog/book_form.html", {"form": form})


@login_required
@permission_required("catalog.change_book", raise_exception=True)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        return redirect(form.save().get_absolute_url())
    return render(request, "catalog/book_form.html", {"form": form})


@login_required
@permission_required("catalog.delete_book", raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("books")
    return render(request, "catalog/book_confirm_delete.html", {"book": book})


@login_required
@permission_required("catalog.add_author", raise_exception=True)
def author_create(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        return redirect(form.save().get_absolute_url())
    return render(request, "catalog/author_form.html", {"form": form})


@login_required
@permission_required("catalog.change_author", raise_exception=True)
def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST or None, instance=author)
    if form.is_valid():
        return redirect(form.save().get_absolute_url())
    return render(request, "catalog/author_form.html", {"form": form})


@login_required
@permission_required("catalog.delete_author", raise_exception=True)
def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        author.delete()
        return redirect("authors")
    return render(request, "catalog/author_confirm_delete.html", {"author": author})