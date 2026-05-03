import urllib.request
import re
import zipfile
import subprocess
from pathlib import Path
import shutil
import json
import base64

with open("absolllute.megahack_original.geode", "wb") as file:
    file.write(urllib.request.urlopen(urllib.request.Request("https://absolllute.com/api/mega_hack/v9/files/v9.1.3/absolllute.megahack.geode", headers={"User-Agent": ""})).read())

def patch(data: bytearray, signature: bytes, patch: bytes):
    match = re.search(signature, data, re.DOTALL)
    if match:
        start = match.start()
        data[start:start + len(patch)] = patch

with zipfile.ZipFile("absolllute.megahack_original.geode", "r") as original_zipfile, zipfile.ZipFile("absolllute.megahack_cracked.geode", "w") as cracked_zipfile:
    for name in original_zipfile.namelist():
        if name == "absolllute.megahack.dll":
            data = bytearray(original_zipfile.read(name))
            patch(data, rb"\x56\x57\x48\x83\xEC\x48\x48\x83\x79\x10\x40", b"\xB8\x01\x00\x00\x00\xC3")
            patch(data, rb"\x55\x41\x56\x56\x57\x53\x48\x83\xEC\x70\x48\x8D\x6C\x24\x70\x48\xC7\x45\xF8\xFE\xFF\xFF\xFF\x48\x83\x39\x00", b"\xB8\x01\x00\x00\x00\xC3")
            patch(data, rb"\xE8....\x48\x83\x7F\x18\x10\x72", b"\xB8\x00\x00\x00\x00")
            patch(data, rb"\x55\x41\x57\x41\x56\x56\x57\x53\x48\x81\xEC\x48\x01\x00\x00\x48\x8D\xAC\x24\x80\x00\x00\x00\x48\xC7\x85\xC0\x00\x00\x00\xFE\xFF\xFF\xFF\x48\x89\xD7", b"\xC3")
            cracked_zipfile.writestr(name, bytes(data))
        else:
            cracked_zipfile.writestr(name, original_zipfile.read(name))

HOME = str(Path.home())
game_path = subprocess.check_output(["find", HOME, "-type", "f", "-name", "GeometryDash.exe", "-print", "-quit"], text=True)
if game_path:
    mods_path = Path(game_path).parent / "geode" / "mods"
    mods_path.mkdir(exist_ok=True)
    shutil.copy("absolllute.megahack_cracked.geode", mods_path)

with open("license", "w") as file:
    file.write(json.dumps({"data": base64.b64encode(json.dumps({"id":"","guid2":"0E841FA5BFE5CE8FC91EB11ADD1DCEF694045BEEAFCF521BF4341D3997C1C219"}).encode()).decode(), "sig": "", "token": ""}))
localappdata_game_path = subprocess.check_output(["find", HOME, "-type", "d", "-path", "*AppData/Local/GeometryDash", "-print", "-quit"], text=True)
if localappdata_game_path:
    license_path = Path(localappdata_game_path).parent / "absolllute.megahack"
    license_path.mkdir(exist_ok=True)
    shutil.copy("license", license_path)
