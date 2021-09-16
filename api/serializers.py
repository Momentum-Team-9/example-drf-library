from rest_framework import serializers
from .models import Book, BookRecord, BookReview, User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("pk", "title", "author", "featured")


class BookDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="book_reviews-detail"
    )

    class Meta:
        model = Book
        fields = ("pk", "title", "author", "publication_year", "featured", "reviews")


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
