import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    pass


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(300),
            MaxValueValidator(datetime.date.today().year),
        ],
        null=True,
        blank=True,
    )
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["title", "author"], name="unique_by_author")
        ]

    def __repr__(self):
        return f"<Book title={self.title} pk={self.pk}>"

    def __str__(self):
        return f"{self.title} by {self.author}"


class BookRecord(models.Model):
    class ReadingState(models.TextChoices):
        WANT_TO_READ = "wr", "want to read"
        READING = "rg", "reading"
        READ = "rd", "read"

    book = models.ForeignKey(
        to="Book", on_delete=models.CASCADE, related_name="book_records"
    )
    reader = models.ForeignKey(
        to="User", on_delete=models.CASCADE, related_name="book_records"
    )
    reading_state = models.CharField(
        max_length=2, choices=ReadingState.choices, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __repr__(self):
        return (
            f"<BookRecord pk={self.pk} user_pk={self.user.pk} book_pk={self.book.pk}>"
        )

    def __str__(self):
        return f"{self.user.username} {self.reading_state}: {self.book.title}"
