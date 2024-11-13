class FetchingException(Exception):
    def __init__(self, url):
        message = ("Failed to retrieve URL: " + url + "." +
                   "Please make sure the ULR is correct and increase the download timeout if required")
        super().__init__(message)
