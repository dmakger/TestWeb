from django.db import models


class Test(models.Model):
    title = models.CharField(max_length=200)
    url = models.SlugField()
    tag = models.CharField(max_length=50)
    difficult = models.FloatField()
    questions = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title


class ResultTest(models.Model):
    test_id = models.IntegerField()
    name = models.CharField(max_length=200)
    group = models.CharField(max_length=200)
    result = models.FloatField()

    def __str__(self):
        return f"{self.test_id}_{self.name}_{self.group}_{self.result}"


class Human(models.Model):
    name = models.CharField(max_length=200)
    group = models.CharField(max_length=200)