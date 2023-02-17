from django.db.models import QuerySet


class ShopRequiredMixin:
    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset

        if shop := self.kwargs.get('shop') is not None:
            return queryset.filter(shop=shop)
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset
