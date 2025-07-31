from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import uuid

class Post(models.Model):
    __tablename__='blogs_post'

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title= models.CharField(max_length=100)
    content= models.TextField()
    date_post= models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)  #Foregin Key if with user is deleted it's blog/post also delete

    def __str__(self):
        return self.title
    
    #get url
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    