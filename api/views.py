from django.contrib.postgres.search import SearchVector
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.generics import CreateAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Book, BookRecord, BookReview, User
from .serializers import (
    BookSerializer,
    BookDetailSerializer,
    BookRecordSerializer,
    BookReviewSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from .custom_permissions import (
    IsAdminOrReadOnly,
    IsReaderOrReadOnly,
    IsReviewerOrReadOnly,
)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().order_by("title")
    serializer_class = BookDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return BookSerializer
        return super().get_serializer_class()

    @action(detail=False)
    def featured(self, request):
        featured_books = Book.objects.filter(featured=True)
        serializer = self.get_serializer(featured_books, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if self.request.query_params.get("search"):
            search_term = self.request.query_params.get("search")
            queryset = Book.objects.annotate(
                search=SearchVector("title", "reviews__body")
            ).filter(search=search_term)
            return queryset
        return super().get_queryset()


class BookRecordViewSet(ModelViewSet):
    queryset = BookRecord.objects.all()
    serializer_class = BookRecordSerializer
    permission_classes = [IsAuthenticated, IsReaderOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(reader=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reader=self.request.user)


class BookRecordCreateView(CreateAPIView):
    pass


class BookReviewListCreateView(ListCreateAPIView):
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = BookReview.objects.filter(book_id=self.kwargs["book_pk"])
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            queryset = queryset.filter(
                body__search=self.request.query_params.get("search")
            )

        return queryset

    def perform_create(self, serializer, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs["book_pk"])
        serializer.save(reviewed_by=self.request.user, book=book)


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serlializer_class = UserCreateSerializer
    parser_classes = [JSONParser, FileUploadParser]

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
        if self.request.user is not user_instance:
            raise PermissionDenied()
        return user_instance

    def get_parser_classes(self):
        if "file" in self.request.data:
            return [FileUploadParser]

        return [JSONParser]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserSerializer
        return super().get_serializer_class()
