from django.conf import settings
from django.conf.urls.static import static

# /ireport, /ireport_details urls defined in msa urls.py

urlpatterns = [

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
