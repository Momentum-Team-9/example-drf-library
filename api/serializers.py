from rest_framework import serializers
from .models import Book, BookRecord, User


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
        fields = ("book", "reader", "reading_state")
