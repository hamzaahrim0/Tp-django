from django.test import TestCase
from django.urls import reverse

from .ml import predict
from .models import Prediction

GOOD = {
    "sepal_length": "5.1", "sepal_width": "3.5",
    "petal_length": "1.4", "petal_width": "0.2",
}


class ExpertTests(TestCase):
    def test_recognises_clear_cases(self):
        self.assertEqual(predict([5.1, 3.5, 1.4, 0.2]), "setosa")
        self.assertEqual(predict([6.5, 3.0, 5.8, 2.2]), "virginica")


class PageTests(TestCase):
    def test_home_page_opens(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_valid_order_is_saved(self):
        response = self.client.post(reverse("index"), GOOD)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Prediction.objects.count(), 1)
        self.assertEqual(Prediction.objects.first().label, "setosa")

    def test_text_instead_of_number_is_rejected(self):
        bad = {**GOOD, "sepal_length": "abc"}
        self.client.post(reverse("index"), bad)
        self.assertEqual(Prediction.objects.count(), 0)

    def test_absurd_values_are_rejected(self):
        for value in ["-3", "0", "5000", "nan"]:
            self.client.post(reverse("index"), {**GOOD, "petal_width": value})
        self.assertEqual(Prediction.objects.count(), 0)

    def test_missing_field_is_rejected(self):
        incomplete = {k: v for k, v in GOOD.items() if k != "petal_width"}
        self.client.post(reverse("index"), incomplete)
        self.assertEqual(Prediction.objects.count(), 0)