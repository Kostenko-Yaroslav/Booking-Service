from django.contrib import admin

from service.models import Booking, Room, Specialty

admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Specialty)
