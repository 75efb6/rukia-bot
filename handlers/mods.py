## Copied from https://github.com/unclem2/osudroid-rx-server/blob/main/objects/mods.py

import re


def get_used_mods(mods: str):
    mods = re.sub(r"\bx\d+\.\d+\b", "", mods, flags=re.IGNORECASE)

    mods = re.sub(r"[^a-zA-Z]", "", mods)
    return mods


class Mods:
    def __init__(self, mods: int):
        self.mods = mods
        self.used_mods = get_used_mods(mods)

    @property
    def convert_std(self):
        mod_mapping = {
            "n": "NF",
            "e": "EZ",
            "h": "HD",
            "r": "HR",
            "u": "SD",
            "d": "DT",
            "x": "",
            "t": "HT",
            "c": "NC",
            "i": "FL",
            "v": "V2",
            "p": "AP",
            "a": "AT",
            "s": "PR",
            "l": "REZ",
            "m": "SC",
            "f": "PF",
            "b": "SU",
            "s": "PR",
        }

        mods = ""

        for char in self.used_mods:
            if char in mod_mapping:
                mods += mod_mapping[char]
        mods_final = f"{mods}{self.speed_multiplier}" if self.speed_multiplier else mods
        if mods_final == "":
            mods_final = "NM"

        return mods_final

    @property
    def convert_droid(self):
        mod_mapping = {
            "n": {"acronym": "NF"},
            "e": {"acronym": "EZ"},
            "h": {"acronym": "HD"},
            "r": {"acronym": "HR"},
            "u": {"acronym": "SD"},
            "d": {"acronym": "DT"},
            "x": {"acronym": ""},
            "t": {"acronym": "HT"},
            "c": {"acronym": "NC"},
            "i": {"acronym": "FL"},
            "v": {"acronym": "V2"},
            "p": {"acronym": "AP"},
            "a": {"acronym": "AT"},
            "s": {"acronym": "PR"},
            "l": {"acronym": "REZ"},
            "m": {"acronym": "SC"},
            "f": {"acronym": "PF"},
            "b": {"acronym": "SU"},
            "s": {"acronym": "PR"},
        }

        used_mods = []

        for char in self.used_mods:
            if char in mod_mapping:
                used_mods.append(mod_mapping[char])

        return used_mods

    @property
    def speed_multiplier(self):
        """
        Extracts the multiplier value from the mods string.
        For example, 'xs|x2.00' will return 'x2.00'.
        """
        match = re.search(r"\bx(\d+\.\d+)\b", self.mods, re.IGNORECASE)
        return match.group(1) + "x" if match else None

    @property
    def forcear(self):
        match = re.search(r"\bAR(\d+\.\d+)\b", self.mods)

        return match.group(1) if match else None

    @property
    def forcecs(self):
        match = re.search(r"\bCS(\d+\.\d+)\b", self.mods)

        return match.group(1) if match else None

    @property
    def fldelay(self):
        match = re.search(r"\bFLD(\d+\.\d+)\b", self.mods)

        return match.group(1) if match else None
