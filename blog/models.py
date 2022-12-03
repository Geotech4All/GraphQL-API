from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=300)
    abstract = models.TextField(max_length=500, verbose_name='short summary')
    post = models.TextField(max_length=700, null=False, blank=False)
    likes = models.PositiveIntegerField()
    dislikes = models.PositiveIntegerField()
    read_length = models.DurationField()
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.title}"

    def _set_read_length(self):
        word_count = len(str(self.post).split())
        avg_time_per_word = timedelta(milliseconds=200)
        read_length = avg_time_per_word * word_count
        return read_length

    def save(self, *args, **kwargs) -> None:
        self.read_length = self._set_read_length()
        return super().save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blog_post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.author.name}"
