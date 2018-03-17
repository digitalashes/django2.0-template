from django.db.models import QuerySet
from django.shortcuts import _get_queryset


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object, or return None if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.

    """

    queryset = klass if isinstance(klass, QuerySet) else _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except AttributeError:
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            f'First argument to get_object_or_404() must be a Model, Manager, or QuerySet, not {klass__name}.'
        )
    except queryset.model.DoesNotExist:
        return None
