from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from threads.models import Thread
from forums.models import Forum

class ThreadListSerializer(serializers.ModelSerializer):
    forum = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='forum-detail',
        lookup_field='slug'
    )
    creator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
        lookup_field='username'
    )
    class Meta:
        model = Thread
        fields = (
            'id',
            'name',
            'forum',
            'pinned',
            'content',
            'creator',
            'created_at',
            'last_activity'
        )

class ThreadCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=75, allow_blank=False)
    forum = serializers.SlugField(
        required=True,
        help_text=_('Required. Slug of the forum this thread is created in')
    )
    content = serializers.CharField(max_length=4000, default='')
    class Meta:
        model = Thread
        fields = (
            'name',
            'forum',
            'pinned',
            'content',
            'creator',
            'created_at',
            'last_activity'
        )
        read_only_fields=('pinned', 'creator', 'created_at', 'last_activity')

    def create(self, validated_data):
        name = validated_data['name']
        forum_slug = validated_data['forum']
        content = validated_data['content']

        # Get forum object
        try:
            forum = Forum.objects.get(slug=forum_slug)
        except Forum.DoesNotExist:
            raise serializers.ValidationError('Forum does not exist, please enter correct forum slug')

        # Get the requesting user
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        else:
            raise serializers.ValidationError('Must be authenticated to create thread')

        # Create the thread
        thread = Thread(
            name=name,
            forum=forum,
            content=content,
            creator=user
        )
        thread.save()
        return thread

class ThreadUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=75, allow_blank=True)
    content = serializers.CharField(max_length=4000, allow_blank=True)
    pinned = serializers.BooleanField(default=False)
    class Meta:
        model = Thread
        fields = (
            'name',
            'forum',
            'pinned',
            'content',
            'creator',
            'created_at',
            'last_activity'
        )
        read_only_fields=('forum', 'creator', 'created_at', 'last_activity')

    def update(self, instance, validated_data):
        # Update fields if there is any change
        for field, value in validated_data.items():
            if value != '':
                setattr(instance, field, value)
        instance.save()
        return instance


class ThreadDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'

class ThreadDetailSerializer(serializers.ModelSerializer):
    forum = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='forum-detail',
        lookup_field='slug'
    )
    creator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
        lookup_field='username'
    )
    class Meta:
        model = Thread
        fields = (
            'id',
            'name',
            'forum',
            'pinned',
            'content',
            'creator',
            'created_at',
            'last_activity'
        )
        read_only_fields = ('id',)
