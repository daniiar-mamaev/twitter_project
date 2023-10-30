from django.db import models

from accounts.models import Profile


def tweet_image_store(instance, filename):
    return f'profile/{instance.profile.user.username}/{instance.created_at}/{filename}'


class Tweet(models.Model):
    text = models.CharField(max_length=140)
    image = models.ImageField(upload_to=tweet_image_store, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

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