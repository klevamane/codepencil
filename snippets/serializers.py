from django.contrib.auth.models import User
from rest_framework import serializers, permissions
from .models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        # We could have also used CharField(read_only=True) in the model
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')


class UserSerializer(serializers.ModelSerializer):
    # Because 'snippets' is a reverse relationship on the User model, it will not be included by default when using the
    #  ModelSerializer class, so we needed to add an explicit field for it.
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')

# using Model serializer

# using serializer
# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.CharField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.CharField(choice=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """create and return a new snippet instance given the validated data"""
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """Update and return an existing 'Snippet' instance, given the validated data"""
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance
#
