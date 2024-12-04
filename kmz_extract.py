# kmz_extract.py 
# extracts the contents of a .kmz file to a folder.
import zipfile

def convert_to_kml(kmz_file: str) -> None:
    """
    """
    with zipfile.ZipFile(kmz_file, 'r') as kmz:
        kmz.extractall(f"{kmz_file}.extracted_kmz")


