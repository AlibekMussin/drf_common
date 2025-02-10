import os
from django.http import FileResponse, Http404


def download_file_view(request, filename):
    file_path = os.path.join('uploads', filename)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        raise Http404("File does not exist")
