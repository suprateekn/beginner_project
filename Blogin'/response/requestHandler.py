class RequestHandler():

    """Getters and setters for Status, Content Type and Content"""

    def __init__(self):

        self.contentType = ""
        self.contents = False

    def getContents(self):
        return self.contents if hasattr(self, 'contents') else b'0'

    def read(self):
        return self.contents

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status if hasattr(self, 'status') else 200

    def getContentType(self):
        return self.contentType if hasattr(self, 'contentType') else ''

    def getType(self):
        return 'static'
