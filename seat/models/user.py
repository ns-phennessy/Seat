from django.db import models

class User(models.Model):
	# whatever properties all users share
	name = models.TextField() # this is a "Suggestion" since we still have no models
	email = models.EmailField() # sure, why not