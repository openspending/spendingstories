from django.contrib import admin
import models 

class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class StoryAdmin(admin.ModelAdmin):
	readonly_fields = ('current_value_usd', 'inflation_last_year')

admin.site.register(models.Story, StoryAdmin)
admin.site.register(models.Theme, ThemeAdmin)