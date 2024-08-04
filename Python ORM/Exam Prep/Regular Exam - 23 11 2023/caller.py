import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review
from django.db.models import Count, Avg, Sum


def get_authors(search_name=None, search_email=None):
    global auth
    if not Author.objects.all():
        return ""

    elif search_name and search_email:
        auth = Author.objects.all().filter(full_name__icontains=search_name, email__icontains=search_email).order_by(
            '-full_name')
    elif search_name and search_email is None:
        auth = Author.objects.all().filter(full_name__icontains=search_name).order_by('-full_name')
    elif search_email and search_name is None:
        auth = Author.objects.all().filter(email__icontains=search_email).order_by('-full_name')
    elif search_name is None and search_email is None:
        return ""
    if not auth:
        return ""
    result = []

    for a in auth.order_by('-full_name'):
        if a.is_banned:
            ban = 'Banned'
        else:
            ban = 'Not Banned'
        result.append(f'Author: {a.full_name}, email: {a.email}, status: {ban}')

    return '\n'.join(result)


def get_top_publisher():
    if not Article.objects.all():
        return ''
    author = Author.objects.annotate(num_articles=Count('article_authors')).filter(num_articles__gt=0).order_by(
        '-num_articles', 'email').first()
    return f"Top Author: {author.full_name} with {author.num_articles} published articles."


def get_top_reviewer():
    if not Review.objects.all():
        return ''

    top_reviewer = Author.objects.annotate(num_reviews=Count('review__author')).filter(num_reviews__gt=0).order_by(
        '-num_reviews',
        'email').first()
    return f'Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_reviews} published reviews.'


def get_latest_article():
    article = Article.objects.annotate(review_count=Count('article_reviews'),
                                       avg_rate=Sum('article_reviews__rating')).last()
    if not Article.objects.all():
        return ""

    if not article:
        return ""

    if article.review_count == 0:
        article.avg_rate = 0.00
        article.save()
    else:
        article.avg_rate = article.avg_rate / article.review_count
        article.save()

    authors = []
    for a in article.authors.all().order_by('full_name'):
        authors.append(a.full_name)

    return (
        f"The latest article is: {article.title}. Authors: {', '.join(authors)}. Reviewed: {article.review_count} times. Average Rating: {article.avg_rate:.2f}.")


def get_top_rated_article():
    top_article = (Article.objects.annotate(rating=Avg('article_reviews__rating'),
                                            review_count=Count('article_reviews')).order_by('-rating', 'title')
                   .filter(review_count__gt=0).first())

    if not Review.objects.all() or not top_article:
        return ""

    if top_article.review_count == 0:
        top_article.rating = 0

    return (f"The top-rated article is: {top_article.title}, "
            f"with an average rating of {top_article.rating:.2f}, "
            f"reviewed {top_article.review_count} times.")


# print(get_top_rated_article())

def ban_author(email=None):
    author = Author.objects.filter(email__exact=email).annotate(num_reviews=Count('author_reviews')).first()

    if not author or email is None:
        return "No authors banned."

    author.is_banned = True
    author.save()
    for r in author.author_reviews.all():
        Review.objects.get(id=r.id).delete()

    return f"Author: {author.full_name} is banned! {author.num_reviews} reviews deleted."
