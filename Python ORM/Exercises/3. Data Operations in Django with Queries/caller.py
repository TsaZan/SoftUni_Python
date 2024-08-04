import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom


# Imp your models here

def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(name=name, species=species)
    pet.save()
    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    artifact.save()
    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.age > 250 and artifact.is_magical == True:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    locations = Location.objects.all().order_by('-id')
    loc = []
    for l in locations:
        loc.append(f"{l.name} has a population of {l.population}!")

    return "\n".join(loc)


def new_capital():
    new = Location.objects.first()
    new.is_capital = True
    new.save()


def get_capitals():
    capitals = Location.objects.filter(is_capital=True)
    return capitals.values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()

    for c in cars:
        i = str(c.year)
        discount = sum(int(a) for a in i) / 100
        c.price_with_discount = float(c.price) - (float(c.price) * discount)
        c.save()


def get_recent_cars():
    cars = Car.objects.filter(year__gt=2020)
    return cars.values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    not_finished = Task.objects.all().filter(is_finished=False)
    tasks = []
    for task in not_finished:
        tasks.append(f"Task - {task.title} needs to be done until {task.due_date}!")

    return "\n".join(tasks)


def complete_odd_tasks():
    tasks = Task.objects.all()

    for t in tasks:
        if t.id % 2 != 0:
            t.is_finished = True
            t.save()


def encode_and_replace(text: str, task_title: str):
    encoded_text = "".join([chr(ord(s) - 3) for s in text])

    Task.objects.filter(title=task_title).update(description=encoded_text)


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type="Deluxe")
    result = []
    for room in deluxe_rooms:
        if room.id % 2 == 0:
            result.append(f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!")

    return "\n".join(result)


def reserve_first_room():
    first_room = HotelRoom.objects.all().first()
    first_room.is_reserved = True
    first_room.save()


def increase_room_capacity():
    # reserved_rooms = HotelRoom.objects.filter(is_reserved=True).order_by('id')
    #
    # if len(reserved_rooms) == 1:
    #     reserved_rooms[0].capacity = reserved_rooms[0].id
    #
    # for room in reserved_rooms:
    #     if room.id != 1:
    #         room.capacity = reserved_rooms[room.id - 1].capacity
    #         room.save()
    #     elif room.id == 1:
    #         room.capacity += 1
    #         room.save()
    all_rooms = HotelRoom.objects.all().order_by('id')

    for i in range(len(all_rooms)):
        room = all_rooms[i]

        if not room.is_reserved:
            continue

        if i == 0:
            room.capacity += room.id
        else:
            room.capacity += HotelRoom.objects.get(id=room.id - 1).capacity

        room.save()


def delete_last_room():
    last_room = HotelRoom.objects.all().last()
    if not last_room.is_reserved:
        last_room.delete()
