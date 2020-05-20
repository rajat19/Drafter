from django_countries.widgets import CountrySelectWidget


class StaticTemplates:
    create_template = '{}/forms/create/{}.html'
    view_template = '{}/{}.html'
    update_template = '{}/forms/update/{}.html'

    def __init__(self, app):
        self.app = app

    def create(self, link):
        return self.create_template.format(self.app, link)

    def view(self, link):
        return self.view_template.format(self.app, link)

    def update(self, link):
        return self.update_template.format(self.app, link)


class Helper:
    @staticmethod
    def get_country_widget():
        return {'country': CountrySelectWidget()}
