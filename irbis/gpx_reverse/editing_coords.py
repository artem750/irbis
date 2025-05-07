import gpxpy
import gpxpy.gpx

# Путь к исходному GPX-файлу
input_gpx_file = r"C:\Users\Admin\Desktop\Аракуль.gpx"

# Путь к выходному GPX-файлу с перевернутой тропой
output_gpx_file = r"C:\Users\Admin\Desktop\Аракуль.gpx"

# ID тропы, которую нужно перевернуть
way_id_to_reverse = 117811760
#


# Функция для нахождения тропы по ID
def find_track_by_way_id(gpx, way_id):
    for track in gpx.tracks:
        if str(way_id) in track.name:
            return track
    return None

# Функция для переворачивания координат тропы
def reverse_track_points(track):
    reversed_segments = []
    for segment in track.segments:
        reversed_points = list(reversed(segment.points))
        reversed_segment = gpxpy.gpx.GPXTrackSegment()
        reversed_segment.points = reversed_points
        reversed_segments.append(reversed_segment)
    return reversed_segments

# Чтение исходного GPX-файла
with open(input_gpx_file, 'r', encoding='utf-8') as file:
    gpx = gpxpy.parse(file)

# Поиск и переворачивание тропы
track_to_reverse = find_track_by_way_id(gpx, way_id_to_reverse)
if track_to_reverse:
    reversed_segments = reverse_track_points(track_to_reverse)
    track_to_reverse.segments = reversed_segments

# Сохранение изменений в новый GPX-файл
with open(output_gpx_file, 'w', encoding='utf-8') as file:
    file.write(gpx.to_xml())

print(f"Перевернутая тропа сохранена в файл: {output_gpx_file}")






import gpxpy
import os

def merge_tracks_continuous(input_path):
    # Чтение файла
    with open(input_path, 'r', encoding='utf-8') as f:
        gpx = gpxpy.parse(f)
    
    # Создаем новый GPX объект
    new_gpx = gpxpy.gpx.GPX()
    
    # Копируем метаданные
    if hasattr(gpx, 'metadata') and gpx.metadata:
        new_gpx.metadata = gpx.metadata
    
    # Желаемый порядок треков (как в Overpass-запросе)
    track_order = [
        'way/1072652833',
        'way/1080477200', 
    ]
    
    # Создаем словарь треков для быстрого доступа
    tracks_dict = {track.name: track for track in gpx.tracks}
    
    # Создаем единый трек с одним сегментом
    merged_track = gpxpy.gpx.GPXTrack(name="Непрерывный маршрут")
    continuous_segment = gpxpy.gpx.GPXTrackSegment()
    
    # Обрабатываем треки в заданном порядке
    for track_name in track_order:
        if track_name in tracks_dict:
            track = tracks_dict[track_name]
            for segment in track.segments:
                # Добавляем все точки из всех сегментов подряд
                continuous_segment.points.extend(segment.points)
    
    # Добавляем сегмент в трек
    merged_track.segments.append(continuous_segment)
    
    # Добавляем трек в GPX
    new_gpx.tracks.append(merged_track)
    
    # Сохраняем результат
    temp_path = input_path + ".tmp"
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(new_gpx.to_xml())
    
    # Заменяем исходный файл
    os.replace(temp_path, input_path)
    print("Все треки успешно объединены в один непрерывный маршрут!")

# Использование
input_path = r"C:\Users\Admin\Desktop\Аракуль.gpx"
merge_tracks_continuous(input_path)