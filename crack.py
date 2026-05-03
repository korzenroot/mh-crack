import json
import base64
import zipfile
import urllib.request

with open("absolllute.megahack_original.geode", "wb") as file:
    file.write(urllib.request.urlopen(urllib.request.Request("https://absolllute.com/api/mega_hack/v9/files/v9.1.3/absolllute.megahack.geode", headers={"User-Agent": ""})).read())

def patch(data: bytearray, pattern: str, repl: str) -> bool:
    pat = [None if x == "?" else int(x, 16) for x in pattern.split()]
    rep = bytes(int(x, 16) for x in repl.split())
    for i in range(len(data) - len(pat) + 1):
        if all(p is None or data[i+j] == p for j, p in enumerate(pat)):
            if i + len(rep) > len(data):
                return False
            data[i:i+len(rep)] = rep
            return True
    return False

with zipfile.ZipFile("absolllute.megahack_original.geode", "r") as original_zipfile, zipfile.ZipFile("absolllute.megahack_cracked.geode", "w") as cracked_zipfile:
    for name in original_zipfile.namelist():
        if name == "absolllute.megahack.dll":
            data = bytearray(original_zipfile.read(name))
            patch(data, "56 57 48 83 EC 48 48 83 79 10 40", "B8 01 00 00 00 C3")
            patch(data, "55 41 56 56 57 53 48 83 EC 70 48 8D 6C 24 70 48 C7 45 F8 FE FF FF FF 48 83 39 00", "B8 01 00 00 00 C3")
            patch(data, "E8 ? ? ? ? 48 83 7F 18 10 72", "B8 00 00 00 00")
            patch(data, "55 41 57 41 56 56 57 53 48 81 EC 48 01 00 00 48 8D AC 24 80 00 00 00 48 C7 85 C0 00 00 00 FE FF FF FF 48 89 D7", "C3")
            cracked_zipfile.writestr(name, bytes(data))
        else:
            cracked_zipfile.writestr(name, original_zipfile.read(name))

with open("license", "w") as file:
    file.write(json.dumps({"data": base64.b64encode(json.dumps({"id":"","guid2":"0E841FA5BFE5CE8FC91EB11ADD1DCEF694045BEEAFCF521BF4341D3997C1C219"}).encode()).decode(), "sig": "", "token": ""}))
