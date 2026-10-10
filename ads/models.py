from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=120)
    is_hidden = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.owner.username})"

    @property
    def first_image(self):
        """Vraća prvu sliku oglasa ili None ako nema slike"""
        return self.images.first()


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Image for Ad #{self.ad_id}"


class AdLike(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    VOTE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ad_likes')
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('ad', 'user')

    def __str__(self):
        return f"{self.user.username} {self.vote} Ad #{self.ad_id}"


class AdFavorite(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ('ad', 'user')

    def __str__(self):
        return f"{self.user.username} favorited Ad #{self.ad_id}"