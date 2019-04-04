from django import template

register = template.Library()


@register.filter('fieldtype')
def fieldtype(field):
	return field.field.widget.__class__.__name__


class GlobalVariable( object ):
	def __init__( self, varname, varval ):
		self.varname = varname
		self.varval  = varval

	def name( self ):
		return self.varname

	def value( self ):
		return self.varval

	def set( self, newval ):
		self.varval = newval


class AssignNode(template.Node):
	def __init__(self, varname, varval):
		self.varname = varname
		self.varval = varval

	def render(self, context):
		gv = context.get(self.varname, None)
		if gv:
			gv.set(self.varval)
		else:
			gv = context[self.varname] = GlobalVariable(self.varname, self.varval)
		return ''


@register.tag
def assign(parser, token):
	try:
		tag_name, varname, varval = token.contents.split()
	except ValueError:
		raise template.TemplateSyntaxError('%r tag requires two arguements' %token.contents.split()[0])
	return AssignNode(varname, varval)