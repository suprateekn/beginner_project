from response.requestHandler import RequestHandler


class BadRequestHandler(RequestHandler):
    def __init__(self):
        """Sets the content type to text/plain and status code to 404 when ever a bad request is made.
        """
        super().__init__()
        self.contentType = 'text/plain'
        self.setStatus(404)
