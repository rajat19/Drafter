from django import template

register = template.Library()


@register.filter('field_type')
def field_type(field):
    return field.field.widget.__class__.__name__


class GlobalVariable(object):
    def __init__(self, var_name, var_val):
        self.var_name = var_name
        self.var_val = var_val

    def name(self):
        return self.var_name

    def value(self):
        return self.var_val

    def set(self, new_val):
        self.var_val = new_val


class AssignNode(template.Node):
    def __init__(self, var_name, var_val):
        self.var_name = var_name
        self.var_val = var_val

    def render(self, context):
        gv = context.get(self.var_name, None)
        if gv:
            gv.set(self.var_val)
        else:
            gv = context[self.var_name] = GlobalVariable(self.var_name, self.var_val)
        return ''


@register.tag
def assign(parser, token):
    try:
        tag_name, var_name, var_val = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires two arguments' % token.contents.split()[0])
    return AssignNode(var_name, var_val)
