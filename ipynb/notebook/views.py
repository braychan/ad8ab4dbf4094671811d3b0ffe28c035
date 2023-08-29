import os
import shutil
import tempfile
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import nbformat

@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if len(files) == 0:
            return HttpResponse('No files selected.')
        else:
            # Create temporary directory to store uploaded files
            temp_dir = tempfile.mkdtemp()
            # Merge notebooks
            merged_notebook = nbformat.v4.new_notebook()
            for f in files:
                notebook = nbformat.read(f, as_version=4)
                merged_notebook.cells.extend(notebook.cells)

            filepath = os.path.join(temp_dir, 'merged.ipynb')
            with open(filepath, 'w') as f:
                nbformat.write(merged_notebook, f)

            # Create response with merged notebook file
            response = HttpResponse(content_type='application/json')
            response['content-Disposition'] = 'attachment; filename="merged_notebook.ipynb"'

            with open(filepath, 'r') as f:
                response.write(f.read())
            
            # Delete temporary directory and files
            shutil.rmtree(temp_dir)

            return response
        
    return render(request, 'notebook/upload.html')