from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Book, BookRecord
from .serializers import BookSerializer, BookRecordSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False)
    def featured(self, request):
        featured_books = Book.objects.filter(featured=True)
        serializer = self.get_serializer(featured_books, many=True)
        return Response(serializer.data)


class BookRecordViewSet(ModelViewSet):
    queryset = BookRecord.objects.all()
    serializer_class = BookRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(reader=self.request.user)
