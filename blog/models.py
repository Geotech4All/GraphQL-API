from datetime import timedelta
from django.contrib.auth import get_user_model #type: ignore
from django.db import models #type: ignore


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=300)
    abstract = models.TextField(max_length=500, verbose_name='short summary')
    body = models.TextField(max_length=700, null=False, blank=False)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    read_length = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.title}"

    def _set_read_length(self) -> float:
        word_count = len(str(self.body).split())
        avg_time_per_word = timedelta(milliseconds=200)
        read_length = avg_time_per_word * word_count
        read_length_in_seconds = read_length.total_seconds()
        return read_length_in_seconds

    def save(self, *args, **kwargs) -> None:
        self.read_length = self._set_read_length()
        return super().save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=400)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.pk} - {self.author.name}"
