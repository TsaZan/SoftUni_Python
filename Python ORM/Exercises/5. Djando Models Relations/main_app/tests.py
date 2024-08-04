from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from caller import show_all_authors_with_their_books, delete_all_authors_without_books
from main_app.models import Author, Book


class LibraryTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        self.author3 = Author.objects.create(name="Harper Lee")
        self.author4 = Author.objects.create(name="Mark Twain")

        # Create books associated with the authors
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            price=19.99,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="1984",
            price=14.99,
            author=self.author2
        )

        self.book3 = Book.objects.create(
            title="To Kill a Mockingbird",
            price=12.99,
            author=self.author3
        )

    def test_zero_show_authors_with_books(self):
        """
        Test zero show authors with books.
        Test if the result is returned with the correct relations
        """
        result = show_all_authors_with_their_books()
        expected_result = (
            "J.K. Rowling has written - Harry Potter and the Philosopher's Stone!\n"
            'George Orwell has written - 1984!\n'
            'Harper Lee has written - To Kill a Mockingbird!'
        )

        self.assertEqual(expected_result, result.strip())

class LibraryTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        self.author3 = Author.objects.create(name="Harper Lee")
        self.author4 = Author.objects.create(name="Mark Twain")

        # Create books associated with the authors
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            price=19.99,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="1984",
            price=14.99,
            author=self.author2
        )

        self.book3 = Book.objects.create(
            title="To Kill a Mockingbird",
            price=12.99,
            author=self.author3
        )

    def test_zero_delete_authors_without_books(self):
        """
        Test zero delete authors without books.
        Test if the authors are being deleted
        """
        delete_all_authors_without_books()
        self.assertEqual(Author.objects.count(), 3)