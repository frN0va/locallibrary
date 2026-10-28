from django.contrib import admin

from .models import Author, Genre, Book, BookAuthor, BookInstance, Language

admin.site.register(Genre)
admin.site.register(Language)


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookAuthorInline]


admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    """Inline listing of BookInstance records, used on the Book detail view."""
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_genre')
    inlines = [BookAuthorInline, BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # Challenge
    list_display = ('book', 'status', 'due_back', 'id')

    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


admin.site.register(BookAuthor)