from django.db import models
from django.db.models import Count


class AstronautsManager(models.Manager):

    def get_astronauts_by_missions_count(self):
        return (self.annotate(missions_num=Count('mission_astronauts'))
                .order_by('-missions_num', 'phone_number'))
