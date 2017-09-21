def str2bool(value):
    """
    convert string to bool
    """
    if value:
        return value.lower() in ("true",)
    else:
        return False