from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Book, BookRecord, BookReview
from .serializers import BookSerializer, BookRecordSerializer, BookReviewSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

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
