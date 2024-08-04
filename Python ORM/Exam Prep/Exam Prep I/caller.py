import os
import django
from django.db.models import Avg, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Movie, Actor, Director


# Create queries within functions

def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""
    elif search_name is None and search_nationality:
        directors = Director.objects.filter(nationality__icontains=search_nationality).order_by('full_name')
    elif search_nationality is None and search_name:
        directors = Director.objects.filter(full_name__icontains=search_name).order_by('full_name')
    else:
        directors = Director.objects.filter(full_name__icontains=search_name,
                                            nationality__icontains=search_nationality).order_by('full_name')

    if not directors:
        return ""

    result = []

    for director in directors:
        result.append(f"Director: {director.full_name}, nationality: {director.nationality}, "
                      f"experience: {director.years_of_experience}")

    return '\n'.join(result)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()
    if not director or director.movie_count == 0:
        return ""
    return f'Top Director: {director.full_name}, movies: {director.movie_count}.'


def get_top_actor():
    actor = Actor.objects.annotate(star_count=Count('movie_star'), avg_rating=Avg('movie_star__rating')).order_by(
        '-star_count', 'full_name').first()
    if not actor or not actor.movie_star.all():
        return ""
    movies = []
    for m in actor.movie_star.all():
        movies.append(m.title)

    return f"Top Actor: {actor.full_name}, starring in movies: {', '.join(movies)}, movies average rating: {actor.avg_rating:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(movie_count=Count('movie_actors')).order_by('-movie_count', 'full_name')[:3]

    if not actors or not Movie.objects.all():
        return ""
    result = []

    for a in actors:
        result.append(f"{a.full_name}, participated in {a.movie_count} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()
    if not movie:
        return ""

    movie_cast = []
    for a in movie.actors.all().order_by('full_name'):
        movie_cast.append(a.full_name)

    return (f"Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. "
            f"Starring actor: {movie.starring_actor.full_name if movie.starring_actor else 'N/A'}. "
            f"Cast: {', '.join(movie_cast)}.")



def increase_rating():
    movie = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not Movie.objects.all() or not movie:
        return "No ratings increased."
    upgraded = movie.count()
    movie.update(rating = F('rating') + .1)

    return f"Rating increased for {upgraded} movies."