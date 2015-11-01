from django.db import models

# Create your models here.
class image(models.Model):
    img_path = models.CharField(max_length=200)
    key = models.CharField(max_length=200, null=True)
    def __unicode__ (self):
        return self.img_path
