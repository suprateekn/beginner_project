from response.requestHandler import RequestHandler
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader


class TemplateHandler(RequestHandler):
    def __init__(self):
        """Sets the content type to text/html and calls the init of the requestHandler  class
        """
        super().__init__()
        self.contentType = 'text/html'

    def find(self, routeData):
        """Renders the html files in the template folder as requested by the get method.

        Args:
            routeData (Str): Key int the routes files which is the path of request having a value as the template file 
            that has to be rendered.

        Returns:
            Boolean : Send to the setter method which sets the response_content and status.
        """
        try:
            env = Environment(loader=FileSystemLoader(
                '%s/template/' % "/home/mindfire/Projects/beginner_project/Blogin'"), autoescape=select_autoescape(['html', 'css']))
            print(routeData['template'])
            temp = env.get_template(routeData['template'])
            response_content = temp.render(
                hidden='hidden', hidden_password='hidden', hidden_email_text='hidden', hidden_user_name='hidden')
            self.contents = response_content
            self.setStatus(200)
            return True
        except BaseException as err:
            print(err)
            self.setStatus(404)
            return False
