from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.


class Block(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    online = models.ManyToManyField(User, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def online_users(self):
        return self.online.count()

    def connect(self, user):
        self.online.add(user)
        self.save()

    def disconnect(self, user):
        self.online.remove(user)
        self.save()

    def get_absolute_url(self):
        return reverse('block_group', args=[self.slug,])

    def __str__(self):
        return self.name


class GroupBlock(models.Model):
    user = models.ForeignKey(User, related_name="user_messages", on_delete=models.CASCADE)
    block = models.ForeignKey(Block, related_name="block_messages", on_delete=models.CASCADE)
    content = models.CharField(max_length=655)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user.username


class PrivateBlock(models.Model):
    user = models.ForeignKey(User, related_name="user_private_block", on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    block_thread = models.CharField(max_length=255, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.block_thread
