import re
import zipfile
import io
import urllib.request
import json
import base64
from pathlib import Path
import shutil

def patch(data: bytearray, signature: bytes, patch: bytes):
    match = re.search(signature, data, re.DOTALL)
    if match:
        start = match.start()
        data[start:start + len(patch)] = patch
        return True
    return False

print("- Downloading Mega Hack -")
with zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(urllib.request.Request("https://absolllute.com/api/mega_hack/v9/files/v9.1.3/absolllute.megahack.geode", headers = {"User-Agent": ""})).read()), "r") as original_zipfile, zipfile.ZipFile("absolllute.megahack.geode", "w") as patched_zipfile:
    print("Downloaded Mega Hack")
    for name in original_zipfile.namelist():
        if name == "absolllute.megahack.dll":
            print("\n- Patching Mega Hack -")
            data = bytearray(original_zipfile.read(name))
            patches = [
                patch(data, rb"\x56\x57\x48\x83\xEC\x48\x48\x83\x79\x10\x40", b"\xB8\x01\x00\x00\x00\xC3"),
                patch(data, rb"\x55\x41\x56\x56\x57\x53\x48\x83\xEC\x70\x48\x8D\x6C\x24\x70\x48\xC7\x45\xF8\xFE\xFF\xFF\xFF\x48\x83\x39\x00", b"\xB8\x01\x00\x00\x00\xC3"),
                patch(data, rb"\xE8....\x48\x83\x7F\x18\x10\x72", b"\xB8\x00\x00\x00\x00"),
                patch(data, rb"\x55\x41\x57\x41\x56\x56\x57\x53\x48\x81\xEC\x48\x01\x00\x00\x48\x8D\xAC\x24\x80\x00\x00\x00\x48\xC7\x85\xC0\x00\x00\x00\xFE\xFF\xFF\xFF\x48\x89\xD7", b"\xC3"),
            ]
            failed = False
            for i, found in enumerate(patches, start = 1):
                if not found:
                    print(f"Failed to find signature for patch {i}")
                    failed = True
                else:
                    print(f"Patch {i} applied successfully")
            if failed:
                exit(1)
            patched_zipfile.writestr(name, bytes(data))
        else:
            patched_zipfile.writestr(name, original_zipfile.read(name))

print("\n- Creating license -")
with open("license", "w") as license_file:
    license_file.write(json.dumps({"data": base64.b64encode(json.dumps({"id": "", "guid2": "0E841FA5BFE5CE8FC91EB11ADD1DCEF694045BEEAFCF521BF4341D3997C1C219"}).encode()).decode(), "sig": "", "token": ""}))
    print("Created license")

print("\n- Copying files -")
geometrydash_exe_path = next(Path.home().rglob("GeometryDash.exe"), None)
if geometrydash_exe_path:
    geode_mods_path = geometrydash_exe_path.parent / "geode" / "mods"
    geode_mods_path.mkdir(exist_ok = True)
    shutil.copy("absolllute.megahack.geode", geode_mods_path)
    print(f"Copied patched Mega Hack to {geode_mods_path}")
else:
    print("Failed to find GeometryDash.exe")

appdata_local_geometrydash_path = next(Path.home().rglob("AppData/Local/GeometryDash"), None)
if appdata_local_geometrydash_path:
    absolllute_megahack_path = appdata_local_geometrydash_path.parent / "absolllute.megahack"
    absolllute_megahack_path.mkdir(exist_ok = True)
    shutil.copy("license", absolllute_megahack_path)
    print(f"Copied license to {absolllute_megahack_path}")
else:
    print("Failed to find AppData/Local/GeometryDash")
