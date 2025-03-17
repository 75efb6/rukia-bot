class Map:
    def __init__(self, data):
        self.data = data
        self.artist: str = ""
        self.title: str = ""
        self.version: str = ""
        self.max_combo: int = 0
        self.sr: float = 0.0
        self.setid: int = 0
        self.diffid: int = 0

    @property
    def parse_mapdata(self):
        m = self
        try:
            if isinstance(self.data, list):
                for item in self.data:
                    m.artist = item.get("artist")
                    m.title = item.get("title")
                    m.version = item.get("version")
                    m.max_combo = item.get("max_combo")
                    m.sr = float(item.get("difficultyrating"))
                    m.setid = item.get("beatmapset_id")
                    m.diffid = item.get("beatmap_id")
                    return m
            else:
                raise Exception("Map data is not list.")
        except Exception as err:
            print(f"Error occured while parsing profile data: {err}")
            return None
