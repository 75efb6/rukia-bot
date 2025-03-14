class Player:
    def __init__(self, data: dict):
        self.data = data
        self.user_name: str = ""
        self.rank: int = 0
        self.pp: float = 0.0
        self.acc: float = 0.0
        self.pc: int = 0

    def parse_profile(self):
        p = self()
        try:
            p.user_name = self.data.get('name')
            stats = self.data.get('stats')
            p.rank = stats.get('rank')
            p.pp = stats.get('pp')
            p.acc = stats.get('accuracy')
            p.pc = stats.get('plays')
            return p
        except Exception as err:
            print(f"Error occured while parsing profile data: {err}")
            return None