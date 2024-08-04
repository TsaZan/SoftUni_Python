import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, Sum, Avg
from main_app.models import Astronaut, Mission, Spacecraft


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    search_query = (Q(name__icontains=search_string) | Q(phone_number__icontains=search_string))
    astronauts = Astronaut.objects.filter(search_query).order_by('name')

    if not astronauts.exists():
        return ""

    result = []

    for a in astronauts:
        result.append(f"Astronaut: {a.name}, phone number: {a.phone_number}, "
                      f"status: {'Active' if a.is_active else 'Inactive'}")

    return '\n'.join(result)


def get_top_astronaut():
    if not Astronaut.objects.all().exists():
        return "No data."
    top_astronaut = (Astronaut.objects.all().annotate(mission_count=Count('mission_astronauts'))
                     .filter(mission_count__gt=0).order_by('-mission_count', 'phone_number')).first()

    if not top_astronaut:
        return "No data."

    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.mission_count} missions."


def get_top_commander():
    if not Mission.objects.all().exists():
        return "No data."

    top_commander = Astronaut.objects.annotate(missions=Count('mission_commander')).order_by('-missions',
                                                                                             'phone_number').filter(
        missions__gt=0).first()

    if not top_commander:
        return "No data."

    return f"Top Commander: {top_commander.name} with {top_commander.missions} commanded missions."


def get_last_completed_mission():
    last_mission = Mission.objects.order_by('-launch_date').filter(status__exact='Completed').annotate(
        spacewalks=Sum('astronauts__spacewalks')).first()

    if not last_mission:
        return "No data."
    astronauts = []
    for a in last_mission.astronauts.all().order_by('name'):
        astronauts.append(a.name)

    return (f"The last completed mission is: {last_mission.name}. "
            f"Commander: {last_mission.commander.name if last_mission.commander else 'TBA'}. "
            f"Astronauts: {', '.join(astronauts)}. Spacecraft: {last_mission.spacecraft.name}. "
            f"Total spacewalks: {last_mission.spacewalks}.")


def get_most_used_spacecraft():
    spacecraft = (Spacecraft.objects.annotate(miss_count=Count('mission_spacecraft', distinct=True),
                                              astronauts_on=Count('mission_spacecraft__astronauts', distinct=True))
                  .filter(miss_count__gt=0).order_by('-miss_count', 'name').distinct().first())

    if not spacecraft:
        return "No data."

    return (f"The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.miss_count} missions, astronauts on missions: {spacecraft.astronauts_on}.")


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.all().filter(mission_spacecraft__status__exact='Planned',
                                                  weight__gte=200.0).distinct()

    if not spacecrafts:
        return "No changes in weight."

    num = 0
    for s in spacecrafts:
        num += 1
        s.weight -= 200.0
        s.save()

    if num == 0:
        return "No changes in weight."

    all_space = Spacecraft.objects.all()
    weight = []
    for a in all_space:
        weight.append(a.weight)

    return (f"The weight of {num} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {sum(weight) / len(weight)}kg")
