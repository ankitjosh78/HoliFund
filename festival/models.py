from django.db import models
from django.db.models import Sum


class Building(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def total_collected(self):
        return (
            Member.objects.filter(room__floor__building=self).aggregate(
                total=Sum("amount_paid")
            )["total"]
            or 0
        )


class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    floor_number = models.IntegerField()

    def __str__(self):
        return f"{self.building.name} - Floor {self.floor_number}"

    def total_collected(self):
        return (
            Member.objects.filter(room__floor=self).aggregate(total=Sum("amount_paid"))[
                "total"
            ]
            or 0
        )


class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.floor} - Room {self.room_number}"

    def total_collected(self):
        return (
            Member.objects.filter(room=self).aggregate(total=Sum("amount_paid"))[
                "total"
            ]
            or 0
        )


class Member(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} (Room {self.room.room_number})"
