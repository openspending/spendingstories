from django.contrib import admin
import models 

class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(models.Story)
admin.site.register(models.Theme, ThemeAdmin)