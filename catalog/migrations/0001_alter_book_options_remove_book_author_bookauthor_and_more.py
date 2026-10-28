import django.db.models.deletion
from django.db import migrations, models


def authorize_books(apps, schema_editor):
    Book = apps.get_model("catalog", "Book")
    BookAuthor = apps.get_model("catalog", "BookAuthor")
    for book in Book.objects.exclude(author=None):
        BookAuthor.objects.create(book=book, author=book.author, author_order=1)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', 'seed_catalog_20260915_0930'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title']},
        ),
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_order', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.author')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
            ],
            options={
                'ordering': ['author_order'],
            },
        ),
        migrations.RunPython(authorize_books, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='books', through='catalog.BookAuthor', to='catalog.author'),
        ),
        migrations.AddConstraint(
            model_name='bookauthor',
            constraint=models.UniqueConstraint(fields=('book', 'author'), name='unique_book_author'),
        ),
    ]
