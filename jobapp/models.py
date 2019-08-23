from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length = 50)
    date_created = models.DateTimeField(default= timezone.now())
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey("Category",on_delete= models.CASCADE)

    def __str__(self):
        return self.title



class Category(models.Model):
    category = models.CharField(max_length=50)


    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Categories"


class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey("Job",on_delete= models.CASCADE)


    def __str__(self):
        return str(self.user.name)