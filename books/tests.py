import pytest
import random
from typing import List, Optional
from .models import Book
from .forms import BookForm
from authors.models import Author
from proj.lib import random_field, random_date
from django_countries.fields import countries
from django.test import TestCase
from django.urls import reverse
from pprint import pprint

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


class TestCreate():
    def test_create_get(self, db, client):
        response = client.get(reverse('books:create'))
        form = response.context_data['form']
        assert isinstance(form, BookForm)

    def test_post_empty_KO(self, db, client):
        response = client.post(reverse('books:create'), {})
        form = response.context_data['form']
        assert not form.is_valid()
        assert form.errors.keys() ==  {'author', 'title', 'isbn', 'release_date'} 

    def test_post_invalid_date_KO(self, db, client, author_factory):
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

    def test_post_valid(self, db, client, author_factory):
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
    def test_list(db, book_factory, client):
        b1 = book_factory()
        b2 = book_factory()
        response = client.get(reverse("books:list"))
        books = response.context_data['object_list']
        
        assert b1 == books[0]
        assert b2  == books[1]
