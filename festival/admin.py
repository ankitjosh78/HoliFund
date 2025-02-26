from django.contrib import admin
from .models import Building, Floor, Room, Member

admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Member)
