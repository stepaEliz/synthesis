from django.db import models


class hotelrooms(models.Model):
    room_id = models.IntegerField()
    hotel_id = models.IntegerField()
    price = models.IntegerField()

