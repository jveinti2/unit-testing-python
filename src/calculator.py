def sum(a, b):
    """
    >>> sum(1, 2)
    3
    """
    return a + b

def subtract(a, b):
    """
    >>> subtract(1, 2)
    -1

    >>> subtract(2, 1)
    1
    """
    return a - b

def multiply(a, b):
    """
    >>> multiply(2, 3)
    6
    """
    return a * b

def divide(a, b):
    """
    >>> divide(6, 3)
    2.0

    >>> divide(6, 0)
    Traceback (most recent call last):
    ValueError: No se puede dividir por 0
    """
    if b == 0:
        raise ValueError('No se puede dividir por 0')
    return a / b