from django.contrib import admin

from testapp.models import Spare, Machine, Note, Img

admin.site.register(Spare)
admin.site.register(Machine)
admin.site.register(Note)
admin.site.register(Img)
