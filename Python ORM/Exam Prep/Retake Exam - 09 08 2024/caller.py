import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, F, Min, Avg
from main_app.models import House, Quest, Dragon


# Create queries within functions
def get_houses(search_string=None):
    if not search_string:
        return "No houses match your search."

    search_quote = Q(name__istartswith=search_string) | Q(motto__istartswith=search_string)
    houses = House.objects.filter(search_quote).order_by('-wins', 'name')

    if not houses:
        return "No houses match your search."
    result = []
    for h in houses:
        result.append(f"House: {h.name}, wins: {h.wins}, motto: {h.motto if h.motto else 'N/A'}")

    return '\n'.join(result)


def get_most_dangerous_house():
    house = House.objects.get_houses_by_dragons_count().first()
    if house is None or house.dragon_house.count() == 0:
        return "No relevant data."

    return (f"The most dangerous house is the House of {house.name} with "
            f"{house.dragon_house.count()} dragons. Currently {'ruling' if house.is_ruling else 'not ruling'} the kingdom.")


def get_most_powerful_dragon():
    dragon = (Dragon.objects.all().annotate(num_quests=Count('dragon_quests'))
              .filter(is_healthy=True).order_by('-power', 'name').first())

    if not dragon:
        return "No relevant data."

    return (
        f"The most powerful healthy dragon is {dragon.name} with a power level of {dragon.power:.1f}, breath type {dragon.breath}, "
        f"and {dragon.wins} wins, coming from the house of {dragon.house.name}. "
        f"Currently participating in {dragon.num_quests} quests.")


def update_dragons_data():
    injured_dragons = Dragon.objects.filter(is_healthy=False, power__gt=1.0)

    num_of_dragons_affected = injured_dragons.update(
        power=F('power') - 0.1,
        is_healthy=True
    )

    if num_of_dragons_affected == 0:
        return "No changes in dragons data."

    min_power = Dragon.objects.aggregate(min_power=Min('power'))['min_power']

    return (f"The data for {num_of_dragons_affected} dragon/s has been changed. "
            f"The minimum power level among all dragons is {min_power:.1f}")


def get_earliest_quest():
    quest = Quest.objects.order_by('start_time').first()

    if quest is None:
        return "No relevant data."

    start_time = quest.start_time
    day = start_time.day
    month = start_time.month
    year = start_time.year

    dragons = quest.dragons.order_by('-power', 'name')
    dragon_names_str = "*".join([dragon.name for dragon in dragons])

    avg_power_level = dragons.aggregate(Avg('power'))['power__avg']
    avg_power_level = f"{avg_power_level:.2f}" if avg_power_level else "0.00"

    return (
        f"The earliest quest is: {quest.name}, code: {quest.code}, "
        f"start date: {day}.{month}.{year}, host: {quest.host.name}. "
        f"Dragons: {dragon_names_str}. Average dragons power level: {avg_power_level}")


def announce_quest_winner(quest_code):
    quest = Quest.objects.filter(code=quest_code).first()
    if quest is None:
        return "No such quest."

    winner_dragon = quest.dragons.order_by('-power', 'name').first()

    winner_dragon.wins += 1
    winner_dragon.save()

    winner_house = winner_dragon.house
    winner_house.wins += 1
    winner_house.save()

    quest_name = quest.name
    quest_reward = quest.reward
    quest.delete()

    return (f"The quest: {quest_name} has been won by dragon {winner_dragon.name} "
            f"from house {winner_house.name}. The number of wins has been updated as follows: "
            f"{winner_dragon.wins} total wins for the dragon and {winner_house.wins} total wins for the house. "
            f"The house was awarded with {quest_reward:.2f} coins.")