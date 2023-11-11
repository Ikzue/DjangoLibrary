import pytest
import random
from typing import List, Optional
from .models import Book
from authors.models import Author
from proj.lib import random_field, random_date
from django_countries.fields import countries

@pytest.fixture
def author_factory(db):
    def create_author(
        last_name=random_field(20),
        middle_name=random_field(20),
        first_name=random_field(20),
        country=random.choice(list(countries)),
        birth_date=random_date()
    ):
        return Author(
            last_name=last_name,
            middle_name=middle_name,
            first_name=first_name,
            country=country,
            birth_date=birth_date
        )
    return create_author

@pytest.fixture
def author_A(db, author_factory):
    return author_factory()

'''
@pytest.fixture
def book_factory(db):
    def create_book(
        author =
    ) -> Book:

        user.groups.add(*groups)
        return user
'''

def test(db, author_A):
    print(author_A)
    assert "A" == "A"
    
def test_2(db, author_A):
    print(author_A)
    assert "A" == "A"