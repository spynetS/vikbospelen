from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from os import listdir
from os.path import isfile, join
from django.template.loader import render_to_string
import json
from pathlib import Path
from django.core.exceptions import PermissionDenied
from livepatch.models import *


livepatch_path = "templates/livepatch/"

def update_component(request):
    if request.method == "POST":
        if request.user.is_staff:
            # 1. Extract data from the request
            uid = request.POST.get('id')
            name = request.POST.get('name')
            component, created = Component.objects.get_or_create(uid=uid)

            excluded_keys = ['id', 'uid', 'props', 'csrfmiddlewaretoken']
            public_fields = {}
            private_fields = {}
            for key, value in request.POST.items():
                if key not in excluded_keys:
                    if key.isupper():
                        public_fields[key] = value
                    else:
                        private_fields[key] = value
                    # add patch to db
                    patch = Patch(key=key,value=value, component=component, created_by=request.user)
                    patch.save()
            
            images = Image.objects.all()
            # We build a context that includes all the updated values for the re-render
            context = {
                **component.get_current_state(),
                'uid': uid,
                'public_fields': public_fields,
                'private_fields': private_fields,
                'component_template': f"{name}",
                'user': request.user,
                'images': images
            }
            
            html = render_to_string('livepatch/base_wrapper.html', context, request=request)
            return HttpResponse(html)
        raise PermissionDenied()    
    
def upload_image(request):
    if request.method == "POST" and request.user.is_staff:
        new_file = request.FILES.get('new_image')
        # Logic to save your image model
        img_obj = Image.objects.create(image=new_file)
        
        context = {
            'image': img_obj,
            'field': 'SRC'
        }
        
        return render(request,"livepatch/editor_image_select.html", context)
    raise PermissionDenied()
