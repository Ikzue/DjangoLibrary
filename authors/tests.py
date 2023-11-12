import pytest
import random
from pprint import pprint

from django.urls import reverse
from django_countries.fields import countries
from .models import Author
from .forms import AuthorForm

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


class TestCreate():
    def test_get(self, db, client):
        response = client.get(reverse('authors:create'))
        form = response.context_data['form']
        assert isinstance(form, AuthorForm)

    def test_post_empty_KO(self, db, client):
        response = client.post(reverse('authors:create'), {})
        form = response.context_data['form']
        assert not form.is_valid()
        assert form.errors.keys() ==  {'last_name', 'country', 'birth_date'} 

    def test_post_invalid_date_KO(self, db, client, author_factory):
        author = author_factory()
        data = {
            "last_name": random_field(N),
            "first_name": random_field(N),
            "middle_name": random_field(N),
            "country": random.choice(list(countries))[0],
            "birth_date": "32/01/2023"
        }
        response = client.post(reverse('authors:create'), data)
        form = response.context_data['form']
        assert not form.is_valid()
        assert form.errors.keys() ==  {'birth_date'}
        assert form.errors['birth_date'] == ['Enter a valid date.'] 

    def test_post_valid(self, db, client, author_factory):
        last_name = random_field(N)
        first_name = random_field(N)
        data = {
            "last_name": last_name,
            "first_name": first_name,
            "middle_name": random_field(N),
            "country": random.choice(list(countries))[0],
            "birth_date": random_date().strftime("%d/%m/%Y")
        }
        response = client.post(reverse('authors:create'), data)
        created_author = Author.objects.last()
        assert response.status_code == 302
        assert response.url == reverse('authors:details', args=[created_author.id])
        assert created_author.first_name == first_name
        assert created_author.last_name == last_name


class TestRead():
    def test_list(self, db, client, author_factory):
        a1 = author_factory()
        a2 = author_factory()
        response = client.get(reverse("authors:list"))
        authors = response.context_data['object_list']
        
        assert a1 == authors[0]
        assert a2 == authors[1]

    def test_details(self, db, client, author_factory):
        a1 = author_factory()
        response = client.get(reverse("authors:details", args=[a1.id]))
        author = response.context_data['object']
        assert a1 == author

class TestUpdate():
    def test_get(self, db, client, author_factory,):
        author = author_factory()
        response = client.get(reverse('authors:update', args=[author.id]))
        form = response.context_data['form']
        assert isinstance(form, AuthorForm)

    def test_post_empty_KO(self, db, client, author_factory):
        author = author_factory()
        response = client.post(reverse('authors:update', args=[author.id]), {})
        form = response.context['form']
        assert not form.is_valid()
        assert form.errors.keys() ==  {'last_name', 'country', 'birth_date'}  

    def test_post_invalid_date_KO(self, db, client, author_factory):
        author = author_factory()
        data = {
            "last_name": random_field(N),
            "first_name": random_field(N),
            "middle_name": random_field(N),
            "country": random.choice(list(countries))[0],
            "birth_date": "32/01/2023"
        }
        response = client.post(reverse('authors:update', args=[author.id]), data)
        form = response.context['form']
        assert not form.is_valid()
        assert form.errors.keys() ==  {'birth_date'}
        assert form.errors['birth_date'] == ['Enter a valid date.'] 

    def test_post_valid(self, db, client, author_factory):
        author = author_factory()
        new_first_name = random_field(N*2)
        data = {
            "last_name": random_field(N),
            "first_name": new_first_name,
            "middle_name": random_field(N),
            "country": random.choice(list(countries))[0],
            "birth_date": random_date().strftime("%d/%m/%Y")
        }
        response = client.post(reverse('authors:update', args=[author.id]), data)
        author.refresh_from_db()
        assert response.status_code == 302
        assert response.url == reverse('authors:details', args=[author.id])
        assert author.first_name == new_first_name

class TestDelete():
    def test_get(self, db, client, author_factory):
        author = author_factory()
        response = client.get(reverse('authors:delete', args=[author.id]))
        confirm_msg = f'Are you sure you want to delete "{author.first_name} {author.last_name}"?'
        assert confirm_msg in response.rendered_content

    def test_post(self, db, client, author_factory):
        author = author_factory()
        nb_authors = Author.objects.count()
        response = client.post(reverse('authors:delete', args=[author.id]))
        assert response.status_code == 302
        assert response.url == reverse('authors:list')
        assert Author.objects.count() == nb_authors - 1
