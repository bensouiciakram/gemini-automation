class CloseWindowException(Exception):
    def __str__(self):
        return 'Closing window flag has been raised'