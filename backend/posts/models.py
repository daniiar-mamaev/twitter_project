import io

from django.utils import timezone
from django.contrib import admin
from django.db import models
from PIL import Image, ImageDraw, ImageFont
from django.core.files import File

from accounts.models import Profile


def process_image(img, text=None, ext='png', font_type='arial.ttf', font_size=32, new_height=None, new_width=None):
    image = Image.open(img)

    width, height = image.size
    if new_width:
        new_height = int((height / width * new_width))
    elif new_height:
        new_width = int((width / height) * new_height)

    if new_width and new_height:
        image.resize((new_width, new_height))

    # if text:
    #     img_draw = ImageDraw.Draw(image)
    #     font = ImageFont.truetype(font_type, size=font_size)
    #     img_draw.text((10, 10), text, font=font)

    image_io = io.BytesIO()
    image.save(image_io, ext)
    return File(image_io, f'image.{ext}')


def tweet_image_store(instance, filename):
    return f'profile/{instance.profile.user.username}/{timezone.now().strftime("%Y%m%d_%H%M")}/{filename}'


class Tweet(models.Model):
    text = models.CharField(max_length=140)
    image = models.ImageField(upload_to=tweet_image_store, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Твит"
        verbose_name_plural = "Твиты"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = process_image(self.image, text='Property of me', font_size=24)
        super().save(*args, **kwargs)

    def all_reactions(self):
        result = {}
        for rtype in ReactionType.objects.all():
            result[rtype.name] = 0
        for reaction in self.reaction_set.all():
            result[reaction.reaction_type.name] += 1
        return result

    def get_reactions(self):
        reactions = self.reaction_set.all()
        result = {}
        for reaction in reactions:
            if result.get(reaction.reaction_type.name):
                result[reaction.reaction_type.name] += 1
            else:
                result[reaction.reaction_type.name] = 1
        return result

    @admin.display(description='reactions')
    def get_reactions_str(self):
        reactions = self.get_reactions()
        return str(reactions)

    def __str__(self):
        return self.text


class Reply(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def all_reactions(self):
        result = {}
        for rtype in ReactionType.objects.all():
            result[rtype.name] = 0
        for reaction in self.reactiontoreply_set.all():
            result[reaction.reaction_type.name] += 1
        return result

    def get_reactions(self):
        reactions = self.reactiontoreply_set.all()
        result = {}
        for reaction in reactions:
            if result.get(reaction.reaction_type.name):
                result[reaction.reaction_type.name] += 1
            else:
                result[reaction.reaction_type.name] = 1
        return result

    def __str__(self):
        return self.text


class ReactionType(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Reaction(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reaction_type = models.ForeignKey(ReactionType, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return f'{self.tweet} - {self.profile} - {self.reaction_type}'

    class Meta:
        unique_together = ['tweet', 'profile']


class ReactionToReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reaction_type = models.ForeignKey(ReactionType, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return f'{self.reply} - {self.profile} - {self.reaction_type}'

    class Meta:
        unique_together = ['reply', 'profile']


def tweet_multiple_images_store(instance, filename):
    return f'profile/{instance.tweet.profile.user.username}/{instance.tweet.text[:10]}/{filename}'


class TweetImage(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=tweet_multiple_images_store)