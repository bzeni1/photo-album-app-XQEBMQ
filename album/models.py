from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    name = models.CharField(max_length=40)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    storage_path = models.CharField(max_length=300)
    public_url = models.URLField()



    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")



    def __str__(self):
        return self.name