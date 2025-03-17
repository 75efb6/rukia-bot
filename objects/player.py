from handlers.mods import Mods

class Player:
    def __init__(self, data: dict):
        self.data = data
        ## Profile
        self.user_name: str = ""
        self.rank: int = 0
        self.pp: float = 0.0
        self.acc: float = 0.0
        self.pc: int = 0
        ## Recent
        self.acc: float = 0.0
        self.combo: int = 0
        self.h100: int = 0
        self.h300: int = 0
        self.h50: int = 0
        self.hmiss: int = 0
        self.mods: str = ""
        self.pp: float = ""
        self.maphash: int = 0

    @property
    def parse_profile(self):
        p = self
        try:
            p.user_name = self.data.get("name")
            stats = self.data.get("stats")
            p.rank = stats.get("rank")
            p.pp = stats.get("pp")
            p.acc = stats.get("accuracy")
            p.pc = stats.get("plays")
            return p
        except Exception as err:
            print(f"Error occured while parsing profile data: {err}")
            return None

    @property
    def parse_recent(self):
        rp = self
        try:
            rp.acc = float(self.data.get("acc"))
            rp.combo = self.data.get("combo")
            rp.h100 = self.data.get("hit100")
            rp.h300 = self.data.get("hit300")
            rp.h50 = self.data.get("hit50")
            rp.hmiss = self.data.get("hitmiss")
            rp.mods = Mods(self.data.get("mods")).convert_std
            rp.pp = self.data.get("pp")
            rp.maphash = self.data.get("maphash")
            return rp
        except Exception as err:
            print(f"Error occured while parsing recent play: {err}")
            return None
