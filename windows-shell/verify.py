#!/usr/bin/env python3
"""Static checks for the produced PE. Requires pefile; does not execute the EXE."""
from pathlib import Path
import hashlib
import pefile

root = Path(__file__).resolve().parent.parent
output = root / 'release' / 'Nexida-Recovery.exe'
pe = pefile.PE(str(output))
assert pe.FILE_HEADER.Machine == 0x8664, 'Expected a 64-bit x86 PE'
assert pe.OPTIONAL_HEADER.Subsystem == 2, 'Expected Windows GUI subsystem'
assert pe.OPTIONAL_HEADER.AddressOfEntryPoint, 'Missing entry point'


def resource(type_id, resource_id):
    entry = next(e for e in pe.DIRECTORY_ENTRY_RESOURCE.entries if e.id == type_id)
    entry = next(e for e in entry.directory.entries if e.id == resource_id)
    entry = next(e for e in entry.directory.entries if e.id == 1033)
    return pe.get_data(entry.data.struct.OffsetToData, entry.data.struct.Size)


assert resource(3, 1) == (root / 'recovered-resources' / 'icon.png').read_bytes(), 'Icon mismatch'
assert resource(24, 1) == (root / 'recovered-resources' / 'app.manifest').read_bytes(), 'Manifest mismatch'
print('PASS: x64 GUI PE, icon and manifest verified')
print('SHA-256:', hashlib.sha256(output.read_bytes()).hexdigest())
