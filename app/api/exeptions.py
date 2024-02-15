class NotAuthorizedError(Exception):
    def __init__(self, message="Not authorized to perform this action"):
        self.message = message
        super().__init__(self.message)