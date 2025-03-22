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
        self.country: str = ""
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
        self.status: str = ""
        self.rank: str = ""
        self.score: int = 0

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
            p.country = self.data.get("country")
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
            status = self.data.get("status")
            if status in [-2, -1, 0]:
                rp.status = "https://files.catbox.moe/m0erx1.png"
            elif status in [1, 5]:
                rp.status = "https://files.catbox.moe/l8ljgc.png"
            elif status in [2, 3]:
                rp.status = "https://files.catbox.moe/k6j7bg.png"
            elif status == 4:
                rp.status = "https://files.catbox.moe/6sdyhr.png"
            else:
                rp.status = "https://files.catbox.moe/m0erx1.png"
            rank = self.data.get("rank")
            if rank == "XH":
                rp.rank = "<:rXH:1353106728434270359>"
            elif rank == "X":
                rp.rank = "<:rX:1353106737326067782>"
            elif rank == "SH":
                rp.rank = "<:rSH:1353106747207847998>"
            elif rank == "S":
                rp.rank = "<:rS:1353106761913077812>"
            elif rank == "A":
                rp.rank = "<:rA:1353106791336120361>"
            elif rank == "B":
                rp.rank = "<:rB:1353106781861056595>"
            elif rank == "C":
                rp.rank = "<:rC:1353106715238989855>"
            elif rank == "D":
                rp.rank = "<:rD:1353106773132841090>"
            rp.score = self.data.get("score")
            return rp
        except Exception as err:
            print(f"Error occured while parsing recent play: {err}")
            return None
