from pathlib import Path
import json
import csv
import pickle


def get_directory_size(directory):
    size = sum(file.stat().st_size for file in directory.rglob('*'))
    return size


def get_directory_info(directory_path_user):
    directory_path = Path(directory_path_user)
    total_size = get_directory_size(directory_path)

    results = []
    for item in directory_path.rglob('*'):
        if item.is_file():
            results.append({
                'path': str(item.name),
                'type': 'file',
                'parent_directory': str(item.parent.name),
                'size_bytes': item.stat().st_size
            })
        elif item.is_dir():
            dir_size = get_directory_size(item)
            results.append({
                'path': str(item.name),
                'type': 'directory',
                'parent_directory': str(item.parent.name),
                'size_bytes': dir_size
            })
    with open('result.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)
    with open('result.csv', 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['path', 'type', 'parent_directory', 'size_bytes'])
        csv_writer.writeheader()
        csv_writer.writerows(results)
    with open('result.pickle', 'wb') as pickle_file:
        pickle.dump(results, pickle_file)
    print(f"Total directory size: {total_size} bytes")


get_directory_info(Path.cwd())
