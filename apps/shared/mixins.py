from rest_framework.response import Response


class ShopRequiredMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        if shop := self.kwargs.get('shop'):
            return qs.filter(shop=shop)
        return qs
