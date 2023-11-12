import pytest
import random
from pprint import pprint

from django.urls import reverse
from django_countries.fields import countries

from django.contrib.auth.models import User
from .models import Book
from .forms import BookForm
from authors.models import Author
from proj.lib import random_field, random_date

N = 20

@pytest.fixture
def author_factory(db):
    def create_author(
        last_name=random_field(N),
        middle_name=random_field(N),
        first_name=random_field(N),
        country=random.choice(list(countries)),
        birth_date=random_date()
    ) -> Author:
        return Author.objects.create(
            last_name=last_name,
            middle_name=middle_name,
            first_name=first_name,
            country=country,
            birth_date=birth_date
        )
    return create_author


@pytest.fixture
def book_factory(db, author_factory):
    def create_book(
        author=author_factory(),
        co_authors=[author_factory(), author_factory()],
        title=random_field(N*2),
        isbn=random_field(17),
        release_date=random_date(),
        description=random_field(N*5)
    ) -> Book:
        book = Book.objects.create(
            author=author,
            title=title,
            isbn=isbn,
            release_date=release_date,
            description=description
        )
        book.co_authors.set(co_authors)
        return book
    return create_book


@pytest.fixture
def user(db):
    return User.objects.create_user("username", "username@domain.com", "pw")

class TestCreate():
    def test_get(self, db, client, user):
        client.force_login(user)
        response = client.get(reverse('books:create'))
        form = response.context_data['form']
        assert isinstance(form, BookForm)

    def test_post_empty_KO(self, db, client, user):
        client.force_login(user)
        response = client.post(reverse('books:create'), {})
        form = response.context_data['form']
        assert not form.is_valid()
        assert form.errors.keys() ==  {'author', 'title', 'isbn', 'release_date'} 

    def test_post_invalid_date_KO(self, db, client, user, author_factory):
        client.force_login(user)
        author = author_factory()
        data = {
            "author": author.id,
            "title": random_field(N*2),
            "isbn": random_field(17),
            "release_date": "32/01/2023"
        }
        response = client.post(reverse('books:create'), data)
        form = response.context_data['form']
        assert not form.is_valid()
        assert form.errors.keys() ==  {'release_date'}
        assert form.errors['release_date'] == ['Enter a valid date.'] 

    def test_post_valid(self, db, client, user, author_factory):
        client.force_login(user)
        author = author_factory()
        title = random_field(N*2)
        data = {
            "author": author.id,
            "title": title,
            "isbn": random_field(17),
            "release_date": "31/01/2023"
        }
        response = client.post(reverse('books:create'), data)
        created_book = Book.objects.last()
        assert response.status_code == 302
        assert response.url == reverse('books:details', args=[created_book.id])
        assert created_book.title == title


class TestRead():
    def test_list(self, db, client, book_factory):
        b1 = book_factory()
        b2 = book_factory()
        response = client.get(reverse("books:list"))
        books = response.context_data['object_list']
        
        assert b1 == books[0]
        assert b2  == books[1]

    def test_details(self, db, client, book_factory):
        b1 = book_factory()
        response = client.get(reverse("books:details", args=[b1.id]))
        book = response.context_data['object']
        assert b1 == book

class TestUpdate():

    def test_get(self, db, client, user, book_factory,):
        client.force_login(user)
        book = book_factory()
        response = client.get(reverse('books:update', args=[book.id]))
        form = response.context_data['form']
        assert isinstance(form, BookForm)

    def test_post_empty_KO(self, db, client, user, book_factory):
        client.force_login(user)
        book = book_factory()
        response = client.post(reverse('books:update', args=[book.id]), {})
        form = response.context['form']
        assert not form.is_valid()
        assert form.errors.keys() ==  {'author', 'title', 'isbn', 'release_date'} 

    def test_post_invalid_date_KO(self, db, client, user, book_factory, author_factory):
        client.force_login(user)
        book = book_factory()
        author = author_factory()
        data = {
            "author": author.id,
            "title": random_field(N*2),
            "isbn": random_field(17),
            "release_date": "32/01/2023"
        }
        response = client.post(reverse('books:update', args=[book.id]), data)
        form = response.context['form']
        assert not form.is_valid()
        assert form.errors.keys() ==  {'release_date'}
        assert form.errors['release_date'] == ['Enter a valid date.'] 

    def test_post_valid(self, db, client, user, book_factory, author_factory):
        client.force_login(user)
        book = book_factory()
        author = author_factory()
        new_title = random_field(N*2)
        data = {
            "author": author.id,
            "title": new_title,
            "isbn": random_field(17),
            "release_date": "31/01/2023"
        }
        response = client.post(reverse('books:update', args=[book.id]), data)
        book.refresh_from_db()
        assert response.status_code == 302
        assert response.url == reverse('books:details', args=[book.id])
        assert book.title == new_title

class TestDelete():
    def test_get(self, db, client, user, book_factory):
        client.force_login(user)
        book = book_factory()
        response = client.get(reverse('books:delete', args=[book.id]))
        confirm_msg = f'Are you sure you want to delete "{book.title}"?'
        assert confirm_msg in response.rendered_content

    def test_post(self, db, client, user, book_factory):
        client.force_login(user)
        book = book_factory()
        nb_books = Book.objects.count()
        response = client.post(reverse('books:delete', args=[book.id]))
        assert response.status_code == 302
        assert response.url == reverse('books:list')
        assert Book.objects.count() == nb_books - 1
