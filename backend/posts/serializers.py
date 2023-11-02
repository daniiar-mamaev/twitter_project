from rest_framework import serializers
from django.db.utils import IntegrityError

from .models import Tweet, Reply, ReactionType, Reaction, ReactionToReply


class ReplySerializer(serializers.ModelSerializer):
    reactions = serializers.ReadOnlyField(source='get_reactions')
    all_reactions = serializers.ReadOnlyField()

    class Meta:
        model = Reply
        fields = '__all__'
        read_only_fields = ['profile', 'tweet']


class TweetSerializer(serializers.ModelSerializer):
    reactions = serializers.ReadOnlyField(source='get_reactions')
    all_reactions = serializers.ReadOnlyField()

    class Meta:
        model = Tweet
        fields = '__all__'
        read_only_fields = ['profile', ]


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
        read_only_fields = ['profile', 'tweet']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            new_reaction_type = validated_data.pop('reaction_type')
            instance = self.Meta.model.objects.get(**validated_data)
            # instance = Reaction.objects.get(**validated_data)
            # Та же запись, но чтобы не повторять из Мета выше model = Reaction, сделали self.Meta.model
            instance.reaction_type = new_reaction_type
            instance.save()
            return instance


class ReactionToReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactionToReply
        fields = '__all__'
        read_only_fields = ['profile', 'reply']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            new_reaction_type = validated_data.pop('reaction_type')
            instance = self.Meta.model.objects.get(**validated_data)
            # instance = Reaction.objects.get(**validated_data)
            # Та же запись, но чтобы не повторять из Мета выше model = Reaction, сделали self.Meta.model
            instance.reaction_type = new_reaction_type
            instance.save()
            return instance


class ReactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactionType
        fields = '__all__'