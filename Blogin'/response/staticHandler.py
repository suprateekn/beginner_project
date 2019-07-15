import os
from response.requestHandler import RequestHandler
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader


class StaticHandler(RequestHandler):
    def __init__(self):
        """Creates a dictionary having the required content type for the type of static file.
        """
        self.filetypes = {
            ".js": "text/javascript",
            ".css": "text/css",
            ".jpg": "image/jpeg",
            ".png": "image/png",
            "notfound": "text/plain"
        }

    def find(self, file_path):
        """Finds the file that has to be rendered for the respective path. 

        Args:
            file_path (str): Path of the request

        Returns:
            Boolean : Send to the setter method which sets the response_content and status.
        """
        split_path = os.path.splitext(file_path)
        extension = split_path[1]

        try:
            if extension in (".jpg", ".jpeg", ".png"):
                self.contents = open("public{}".format(file_path), 'rb').read()
            else:
                env = Environment(loader=FileSystemLoader(
                    '%s/public/' % "/home/mindfire/Projects/beginner_project/Blogin'"), autoescape=select_autoescape(['html', 'css']))
                temp = env.get_template(file_path)
                response_content = temp.render()
                self.contents = response_content

            self.setContentType(extension)
            self.setStatus(200)
            return True
        except:
            self.setContentType('notfound')
            self.setStatus(404)
            return False

    def setContentType(self, ext):
        """sets the content type according to the extension referring from the dictionary.

        Args:
            ext (str): The extension of the file requested.
        """
        self.contentType = self.filetypes[ext]
