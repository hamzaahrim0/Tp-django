from django.contrib import admin

from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "label", "sepal_length", "sepal_width",
                    "petal_length", "petal_width")
    list_filter = ("label",)
    