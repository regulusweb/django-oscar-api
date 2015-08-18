# On purpose raise ImportError
from django import NonExistingApp


class HeaderSessionMiddleware(NonExistingApp):
    pass