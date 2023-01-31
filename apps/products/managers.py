from mptt.managers import TreeManager
from mptt.querysets import TreeQuerySet
from parler.managers import TranslatableManager, TranslatableQuerySet


class CategoryQuerySet(TranslatableQuerySet, TreeQuerySet):
    def as_manager(cls):
        manager = CategoryManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)


class CategoryManager(TreeManager, TranslatableManager):
    _queryset_class = CategoryQuerySet
