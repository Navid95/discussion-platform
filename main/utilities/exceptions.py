
class NoUserFound(Exception):
    """
    raised when no user is found by the persistence layer
    """
    code = 404

    @property
    def message(self):
        if self.args[0] is not None:
            return self.args[0]
        else:
            return "No User Found"
