from django.db.models import Count
from django.shortcuts import render

from .ml import predict
from .models import Prediction

FIELDS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

#Salam ana Hamza Ahrim, je suis un étudiant en 2ème année à l'ESI, et je suis en train de travailler sur un projet Django. J'ai besoin d'aide pour compléter le code de la vue index. Voici le code que j'ai jusqu'à présent :
def index(request):
    result = None
    error = None

    if request.method == "POST":
        try:
            values = [float(request.POST[name]) for name in FIELDS]
        except (KeyError, ValueError):
            error = "Please enter four valid numbers."
        else:
            if not all(0 < v <= 20 for v in values):
                error = "Each measurement must be between 0 and 20 cm."
            else:
                result = predict(values)
                Prediction.objects.create(**dict(zip(FIELDS, values)), label=result)

    history = Prediction.objects.all()[:20]
    counts = Prediction.objects.values("label").annotate(n=Count("id")).order_by("label")
    chart = {
        "labels": [c["label"] for c in counts],
        "values": [c["n"] for c in counts],
    }

    return render(request, "index.html", {
        "result": result,
        "error": error,
        "history": history,
        "chart": chart,
    })
    
