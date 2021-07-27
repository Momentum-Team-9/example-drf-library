from rest_framework import serializers
from .models import Book, BookRecord, BookReview, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("title", "author", "publication_year", "featured")


class BookRecordSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    reader = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = BookRecord
        fields = ("pk", "book", "reader", "reading_state")


class BookReviewSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(read_only=True, slug_field="title")
    reviewed_by = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = BookReview
        fields = ("pk", "body", "book", "reviewed_by")


class UserSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = User
        fields = ["pk", "username", "photo"]
