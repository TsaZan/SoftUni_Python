from django.test import TestCase
from main_app.models import Author
from caller import find_authors_nationalities


class AuthorNationalitiesTestCase(TestCase):
    def setUp(self):
        authors = [
            Author(first_name="John", last_name="Smith", birth_date="1980-05-15", nationality="American"),
            Author(first_name="Jane", last_name="Johnson", nationality="British",
                   biography="Jane Johnson is a renowned fantasy writer, famous for her epic fantasy series."),
            Author(first_name="Michael", last_name="Brown", birth_date="1990-02-10",
                   biography="Michael Brown is a science fiction author with a passion for space exploration."),
            Author(first_name="Sarah", last_name="Lee", nationality="Australian",
                   biography="Sarah Lee is a best-selling author of romantic novels."),
            Author(first_name="Maria", last_name="Garcia",
                   biography="Maria Garcia is a poet and writer, celebrated for her lyrical style."),
            Author(first_name="Emily", last_name="White", birth_date="1992-03-12", nationality="American",
                   biography="Emily White is a young adult fiction author, known for her coming-of-age stories."),
            Author(first_name="Laura", last_name="Hall", birth_date="1982-08-04", nationality="American"),
            Author(first_name="John", last_name="Grisham", birth_date="1955-02-08", nationality="American"),
            Author(first_name="John", last_name="Steinbeck",
                   biography="John Steinbeck was a renowned American author, famous for his classic novels."),
            Author(first_name="Robert", last_name="Miller", birth_date="1970-12-18", nationality="British",
                   biography="Robert Miller is a historical fiction writer, often exploring medieval themes."),
        ]

        Author.objects.bulk_create(authors)

    def test_find_authors_nationalities(self):
        result = find_authors_nationalities()
        self.assertEqual(result.strip(), """John Smith is American
Jane Johnson is British
Sarah Lee is Australian
Emily White is American
Laura Hall is American
John Grisham is American
Robert Miller is British""")
