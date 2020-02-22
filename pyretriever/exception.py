class RetrieverError(Exception):
    """Generic exception for mylib"""

    def __init__(self, msg: str, original_exception: Exception):
        super(RetrieverError, self).__init__(f"{msg}: {original_exception}")
        self.original_exception = original_exception
