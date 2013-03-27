from django import template

from tansu.forms import EntityEditForm

register = template.Library()

@register.simple_tag
def entity(entity, request):
    form = EntityEditForm(instance=entity)
    c = {'request': request,
         'entity':entity,
         'form': form,}
    t = template.loader.get_template('tansu/entity-tag.html')
    return t.render(template.Context(c))

@register.simple_tag
def list_entity(entity, request):
    c = {'request': request, 'entity':entity}
    t = template.loader.get_template('tansu/entity-tag-list.html')
    return t.render(template.Context(c))

@register.simple_tag
def list_instance(instance, request):
    c = {'request': request, 'instance':instance}
    t = template.loader.get_template('tansu/instance-tag.html')
    return t.render(template.Context(c))
