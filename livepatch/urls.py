from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from livepatch import views as livepatch
from livepatch import admin_views as admin

images_url = "images"
image_root = "images/"

urlpatterns = [
    path('update/', livepatch.update_component),
    path('upload-image/', livepatch.upload_image),
    path('dashboard/', admin.dashboard),
] + static(images_url, document_root=image_root)

