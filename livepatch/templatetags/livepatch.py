from django import template
import json
import hashlib
from livepatch.models import Image
from django.conf import settings
from livepatch.models import Component

register = template.Library()

wrapper = settings.LIVEPATCH_WRAPPER if hasattr(settings, 'LIVEPATCH_WRAPPER') else 'livepatch/base_wrapper.html'

def generate_component_id(template_name, **kwargs):
    prefix = template_name.replace('/', '-').replace('.', '-')
    
    # The 'default=str' ensures that if an object isn't a string (like a Date), 
    # it converts it to a string instead of crashing.
    kwargs_string = json.dumps(kwargs, sort_keys=True, default=str)
    
    hash_suffix = hashlib.md5(kwargs_string.encode()).hexdigest()[:8]
    return f"{prefix}-{hash_suffix}"

def is_public(arg):
    return arg.isupper()


@register.inclusion_tag(wrapper, takes_context=True)
def render_component(context, template_name, **kwargs):
    uid = generate_component_id(template_name, **kwargs)

    # copy the args passed from the render_component tag
    args = kwargs.copy()
    args['uid'] = uid
    # fetch the component and if its exists we update
    # the args based on the patches
    component = Component.objects.filter(uid=uid)
    if component:
        args.update(component[0].get_current_state())

    #The fields that can be edited
    public_fields = {}
    private_fields = {}
    for arg in args:
        if type(arg) == str:
            if is_public(arg):
                public_fields[arg] = args[arg]
            else:
                private_fields[arg] = args[arg]

    images = Image.objects.all()

    context_dict = {
        'public_fields': public_fields,
        'private_fields': private_fields,
        'component_template': template_name,
        'user': context.get('user'),
        'images': images
    }
    context_dict.update(args)
    return context_dict
