from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

# Create your models here.
class User(AbstractUser):
    pass

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Posts(models.Model):
    tittle = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(default=datetime.datetime.now)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    id = models.IntegerField(primary_key=True, editable=False)
    class Meta:
        ordering = ['-created_on']
    def __str__(self):
        return f"{self.tittle}"