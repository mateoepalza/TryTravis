from django.contrib import admin
from .models import Flight, Passenger, Airport

# Register your models here.


# -> The StackedInline class will allow us in a stacked format add new relationships
#    between objects
# -> Basically, ths class will represent the place on the admin interface where I
#    would like to be able to add and modify passengers in flight section
class PassengerInLine(admin.StackedInline):
    # -> This model will refere to the class Passenger in models.py, to the property
    #    flights and the through refers to the intermediary table many to many table
    model = Passenger.flights.through
    # -> This extra equals one means that i want to be able to add one additional
    #    passenger at a time.
    extra = 1

class FlightAdmin(admin.ModelAdmin):
    # -> In here I'm saying that i want to add this additional inline section
    #    of the Admin page called PassengerInLine that was the one that we created
    #    above
    inlines = [PassengerInLine]

# admin.ModelAdmin -> we are extending from the class ModelAdmin
# This class is going to be a especial set of configurations settings
# that I'm only going to use when I'm editing passengers
class PassengerAdmin(admin.ModelAdmin):
    # this is a setting that will allow us to create a different control in order
    # to make easier the management of the flights of a singl passenger
    filter_horizontal = ("flights",)


admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Airport)
