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
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        raise GraphQLError(f"{klass.__name__} with {kwargs} was not found")
