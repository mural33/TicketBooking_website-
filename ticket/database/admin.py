from django.contrib import admin
from .models import UserData,Times,Demo,Dates,Booked
# Register your models here.
class AdminDemo(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)} 
admin.site.register(UserData)
admin.site.register(Times)
admin.site.register(Booked)
admin.site.register(Demo,AdminDemo)
admin.site.register(Dates)
