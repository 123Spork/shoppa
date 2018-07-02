class SQLOperationalError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SQLInvalidRequestError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SQLInternalError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SQLIntegrityError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ObjectNotFound(Exception):
    """
        An exception raised by Kanga if a read action hits an issue.
    """
    def __init__(self, object_id=None, model=None, *args, **kwargs):
        self.object_id = object_id
        self.model = model
        super().__init__(*args, **kwargs)