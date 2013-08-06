from django.contrib import admin
import models 

class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class StoryAdmin(admin.ModelAdmin):
	list_display    = ('title', 'value', 'currency', 'current_value_usd', 'continuous', 'country', 'sticky', 'published')
	readonly_fields = ('current_value_usd', 'inflation_last_year',)
	search_fields   = ['title', 'value', 'current_value_usd', 'country']


admin.site.register(models.Story, StoryAdmin)
admin.site.register(models.Theme, ThemeAdmin)