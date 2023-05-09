import inspect
from typing import TypeVar
from graphql import GraphQLError
from django.db import models #type: ignore


T = TypeVar('T')

def get_object_or_errror(klass: T, *args, **kwargs) -> T:
    """
    Gets and returns an object with the specified arguments from the specified class
    """
    #Ensure klass is a subclass of models.Model
    assert (inspect.isclass(klass) and issubclass(klass, models.Model)), "Invalid input"
    try:
        obj = klass.objects.get(*args, **kwargs)
        return obj
    except klass.DoesNotExist:
        raise GraphQLError(f"{klass} with {args} and {kwargs} was not found")
