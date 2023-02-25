from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page': self.page.number,
            'results': data
        })


class CountResultPaginate(PageNumberPagination):
    page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'results': data
        })
