from django.db import models

# Create your models here.
class Destinations(models.Model):

    country_name = models.CharField(max_length=200, null=False)
    been = models.BooleanField(default=False)
    want_to_go = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.country_name} | I have been: {self.been} | I want to go: {self.want_to_go}'


class User(models.Model):

    username = models.Charfield(max_length=20, null=False)
    password = models.CharField(max_length=20, null=False)

    def __str__(self):
        return f'username: {self.username} | password: {self.password}'