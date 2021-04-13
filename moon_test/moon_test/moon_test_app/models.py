from django.db import models

# Create your models here.

class Test(models.Model):
    title = models.CharField(max_length=200)
    url = models.SlugField()
    tag = models.CharField(max_length=50)
    difficult = models.FloatField()
    image = models.ImageField()

    def __str__(self):
        return self.title