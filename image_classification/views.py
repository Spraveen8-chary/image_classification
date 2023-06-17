from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
import shutil
from deepface import DeepFace
import time
def home(request):
    return render(request, 'base.html')

def selection(request):
    if request.method == 'POST':
        # Get the path of the selected folder
        folder_path = request.POST.get('folderInput')
        
        # Get the selected image file
        image_file = request.FILES.get('formFile')
        
        # Print the paths of the folder and image file
        print("Selected Folder Path:", folder_path)
        print("Selected Image Path:", image_file.name)
        
        input_image_path = f"C:\\Users\\Admin\\Desktop\\DJANGO\\first_project\\image_classification\\static\\images\\uploads\\{image_file.name}"
        print(input_image_path)
        group_images_folder = "C:\\Users\\Admin\\Desktop\\DJANGO\\first_project\\image_classification\\static\\images\\students"
        output_dir = "C:\\Users\\Admin\\Desktop\\DJANGO\\first_project\\image_classification\\static\\images\\FETCHED"

        group_image_paths = [os.path.join(group_images_folder, file) for file in os.listdir(group_images_folder)]
        
        input_image = input_image_path
        for group_image_path in group_image_paths:
            result = DeepFace.verify(input_image, group_image_path, model_name='Facenet', distance_metric='euclidean_l2', enforce_detection=False)
            if result['verified'] and result['distance'] <= 0.5:
                # The faces are considered a match
                print(f"Match found with similarity score: {result['distance']}")
                if output_dir is not None:
                    # Copy the matching group image to the output directory
                    shutil.copy(group_image_path, output_dir)
        
        response_data = {
            'progress': 100
        }

        return JsonResponse(response_data)
    
    return render(request, 'base.html')
    
