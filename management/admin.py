from django.contrib import admin
from django.apps import apps
# Register your models here.

# admin.site.register(Cusom)
# admin.site.register(Question)
# admin.site.register(Choice)
for model_name, model in apps.get_app_config('management').models.items():
    admin.site.register(model)