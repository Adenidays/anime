from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg


class AnimeList(models.Model):
    title = models.CharField(max_length=255)
    episodes = models.PositiveIntegerField()
    gener = models.ManyToManyField('Genres')
    image = models.CharField(max_length=500)
    status = models.CharField(max_length=255)
    synopsis = models.TextField()
    type = models.CharField(max_length=255)
    hasEpisode = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def update_average_rating(self):
        # Calculate the average rating based on related AnimeRating objects
        average_rating = self.anime_ratings.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            self.rating = round(average_rating, 2)
        else:
            self.rating = 0.00

    def __str__(self):
        return f"{self.title}-{self.pk}"


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    anime = models.ForeignKey(AnimeList, on_delete=models.CASCADE, related_name='anime_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.anime.title}'


class Genres(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Season(models.Model):
    anime = models.ForeignKey(AnimeList, on_delete=models.CASCADE)
    season_number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.anime.title} - Season {self.season_number}: {self.name}'


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    episode_number = models.PositiveIntegerField()
    video_file = models.FileField(upload_to='episode_videos/')

    def __str__(self):
        return f'{self.season.anime.title} - Season {self.season.season_number}, Episode {self.episode_number}'


class AnimeRating(models.Model):
    RATING_CHOICES = [
        (1, '1 - Awful'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    anime = models.ForeignKey(AnimeList, on_delete=models.CASCADE, related_name='anime_ratings')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.anime.update_average_rating()
        self.anime.save()

    def __str__(self):
        return f'{self.user.username}\'s rating of {self.anime.title}'
