class FetchingException(Exception):
    def __init__(self, url):
        message = "Failed to retrieve URL: " + url
        super().__init__(message)
