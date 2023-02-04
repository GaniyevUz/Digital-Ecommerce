from rest_framework.response import Response


class CountResultMixin:
    """
    Count a queryset.
    """

    def count_result_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = {
            'count': queryset.count()
        }
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data['result'] = serializer.data
        return Response(data)

    def get_count_result_list(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'count': queryset.count(),
            'result': serializer.data
        }
        return Response(data)

    def get_count_result_list(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'count': queryset.count(),
            'result': serializer.data
        }
        return Response(data)
