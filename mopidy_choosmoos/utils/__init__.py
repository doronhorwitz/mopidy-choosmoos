from math import floor
from uuid import UUID


# https://gist.github.com/ShawnMilo/7777304
def validate_uuid4(uuid_string):

    """
    Validate that a UUID string is in
    fact a valid uuid4.
    Happily, the uuid module does the actual
    checking for us.
    It is vital that the 'version' kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.
    """

    try:
        val = UUID(uuid_string, version=4)
    except (ValueError, TypeError):
        # If it's a ValueError or TypeError, then the string
        # is not a valid hex code for a UUID.
        return False

    # If the uuid_string is a valid hex code,
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a
    # valid uuid4. This is bad for validation purposes.

    return val.hex == uuid_string.replace("-", "")


# https://stackoverflow.com/a/2272174/506770
def floor_to_base_int(value, base):
    return int(base * floor(float(value) / base))
