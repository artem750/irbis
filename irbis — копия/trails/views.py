import os
import gpxpy
from django.http import JsonResponse, HttpResponseNotFound
from .models import Trail

def get_trail_coords(file_path):
    # Формируем полный путь к файлу GPX
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'gpx_files', file_path)
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        coords = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    coords.append([point.latitude, point.longitude])
        return coords

def get_trails(request):
    trails = Trail.objects.all()
    trails_list = []
    for trail in trails:
        trail_dict = {
            'name': trail.name,
            'description': trail.description,
        }
        trails_list.append(trail_dict)
    return JsonResponse(trails_list, safe=False)

def get_trail_with_coords(request, trail_name):
    try:
        trail = Trail.objects.get(name=trail_name)
        coords = get_trail_coords(f'{trail_name}.gpx')
        return JsonResponse({
            'name': trail.name,
            'description': trail.description,
            'coords': coords
        })
    except Trail.DoesNotExist:
        return HttpResponseNotFound("Trail not found")
