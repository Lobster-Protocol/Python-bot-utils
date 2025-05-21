# write a simple addition function
def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b

    Raises:
        TypeError: If a or b is not a number
    """
    if not isinstance(a, (int, float)) or a is None:
        raise TypeError("First argument must be a number")
    if not isinstance(b, (int, float)) or b is None:
        raise TypeError("Second argument must be a number")
    return a + b


# write a simple subtraction function
def subtract(a: int, b: int) -> int:
    """Subtract two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        The result of a - b

    Raises:
        TypeError: If a or b is not a number
    """
    if not isinstance(a, (int, float)) or a is None:
        raise TypeError("First argument must be a number")
    if not isinstance(b, (int, float)) or b is None:
        raise TypeError("Second argument must be a number")
    return a - b
