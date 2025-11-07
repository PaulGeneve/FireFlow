from flask_smorest import abort

def check_allowed_filter(attr, allowed_filters):
    """
    Check if the provided attribute is allowed for filtering.
    :param attr:
    :return:
    """
    if attr not in allowed_filters:
        abort(400, message=f"Filtering by '{attr}' is not allowed.")
    return True