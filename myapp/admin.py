from django.contrib import admin
from myapp import models

# Register your models here.
admin.site.register(models.Client) 
admin.site.register(models.RegisterLocation)


# admin.site.register(models.Car)
# admin.site.register(models.CarImage)

 
class CarImageInlineAdmin(admin.TabularInline):
    model = models.CarImage
    extra = 0


class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInlineAdmin]


admin.site.register(models.Car, CarAdmin)