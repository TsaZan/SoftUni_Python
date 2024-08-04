import os
import django
from django.db.models import Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match


def get_tennis_players(search_name=None, search_country=None):

    global players
    if search_name is None and search_country is None:
        return ""
    elif search_name and search_country:
        players = TennisPlayer.objects.all().filter(full_name__icontains=search_name,
                                                    country__icontains=search_country).order_by('ranking')
    elif search_name:
        players = TennisPlayer.objects.all().filter(full_name__icontains=search_name).order_by('ranking')
    elif search_country:
        players = TennisPlayer.objects.all().filter(country__icontains=search_country).order_by('ranking')

    if not players:
        return ""
    result = []
    for p in players:
        result.append(f'Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}')

    return '\n'.join(result)

# print(get_tennis_players('p', None))

def get_top_tennis_player():
    top_player = TennisPlayer.objects.all().annotate(wins = Count('match_winner')).order_by('-wins', 'full_name').first()
    if not top_player:
        return ""
    return f"Top Tennis Player: {top_player.full_name} with {top_player.wins} wins."

# print(get_top_tennis_player())



def get_tennis_player_by_matches_count():

    if not TennisPlayer.objects.all() or not Match.objects.all():
        return ""
    most_played = (TennisPlayer.objects.all().annotate(matches = Count('match_players'))
                   .filter(matches__gt = 0).order_by('-matches', 'ranking').first())

    if not most_played:
        return ""

    return f"Tennis Player: {most_played.full_name} with {most_played.matches} matches played."

# print(get_tennis_player_by_matches_count())

def get_tournaments_by_surface_type(surface=None):

    if surface is None or not Tournament.objects.all():
        return ""

    tournaments = Tournament.objects.all().filter(surface_type__icontains =surface).annotate(match =Count('match_tournament')).order_by('-start_date')

    if not tournaments:
        return ""

    result = []

    for t in tournaments:
        result.append(f"Tournament: {t.name}, "
                      f"start date: {t.start_date}, matches: {t.match}")

    return '\n'.join(result)


# print(get_tournaments_by_surface_type('hard'))

def get_latest_match_info():

    if not Match.objects.all():
        return ""

    last_one = Match.objects.all().order_by('date_played', 'id').last()

    players = []

    for p in last_one.players.all().order_by('full_name'):
        players.append(p.full_name)

    return (f"Latest match played on: {last_one.date_played}, tournament: {last_one.tournament.name}, score: {last_one.score}, "
            f"players: {players[0]} vs {players[1]}, "
            f"winner: {last_one.winner.full_name if last_one.winner else 'TBA'}, summary: {last_one.summary}")

# print(get_latest_match_info())


def get_matches_by_tournament(tournament_name=None):

    if not Tournament.objects.all() or tournament_name is None:
        return "No matches found."

    matches = Match.objects.all().filter(tournament__name__exact=tournament_name).order_by('-date_played')


    if not matches:
        return "No matches found."

    result = []
    for m in matches:
        result.append(f"Match played on: {m.date_played}, score: {m.score}, "
                      f"winner: {m.winner.full_name if m.winner else 'TBA'}")

    return '\n'.join(result)

# print(get_matches_by_tournament('Tournament 3'))