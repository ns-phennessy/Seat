from django.db import models


class User(models.Model):
    # whatever properties all users share
    # this is a "Suggestion" since we still have no models
    name = models.TextField()
    email = models.EmailField()  # sure, why not
