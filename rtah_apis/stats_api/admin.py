from django.contrib import admin

from .models import Person
from .models import Hike

admin.site.register(Hike)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = ['first_name','last_name','join_date','email','profile_img',]
    readonly_fields=('join_date',)

    class Meta:
        model = Person
