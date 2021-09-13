from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Book, BookRecord, BookReview, User
from .serializers import (
    BookSerializer,
    BookDetailSerializer,
    BookRecordSerializer,
    BookReviewSerializer,
    UserSerializer,
)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return BookSerializer
        return super().get_serializer_class()

    @action(detail=False)
    def featured(self, request):
        featured_books = Book.objects.filter(featured=True)
        serializer = self.get_serializer(featured_books, many=True)
        return Response(serializer.data)


class BookRecordViewSet(ModelViewSet):
    queryset = BookRecord.objects.all()
    serializer_class = BookRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(reader=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reader=self.request.user)


class BookReviewViewSet(ModelViewSet):
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = BookReview.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [FileUploadParser, JSONParser]

    @action(detail=True, methods=["put", "patch"])
    def photo(self, request, id=None):
        if "file" not in request.data:
            raise ParseError("Missing file attachment")

        file = request.data["file"]
        user = self.get_object()
        user.photo.save(file.name, file, save=True)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=201)

    def get_object(self):
        user_instance = get_object_or_404(self.get_queryset(), pk=self.kwargs["id"])
        if self.request.user.pk != user_instance.pk:
            raise PermissionDenied()
        return user_instance

    def get_parser_classes(self):
        if "file" in self.request.data:
            return [FileUploadParser]

        return [JSONParser]
