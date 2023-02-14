class ShopRequiredMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        if shop := self.kwargs.get('pk'):
            return qs.filter(shop=shop)
        return qs
