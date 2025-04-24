from django.db import models

class Disease(models.Model):
    disease_name = models.CharField(max_length=255)
    crop_name = models.CharField(max_length=255)
    symptoms = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        return self.disease_name
