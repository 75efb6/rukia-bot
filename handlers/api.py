import config
from handlers.mods import Mods
from utils.requests import Requests as r
from objects.player import Player
import hashlib


class DroidAPI:
    def __init__(self):
        self.wl_key = config.wl_key

    def get_profile(self, uid):
        api_url = f'/api/get_user?id={uid}'
        try:
            response = r.do(isDroid=True, request_type="GET", api_endpoint=api_url)
            if response.status == 200:
                data = response.json()
                ## Parsing the data
                p = Player(data).parse_profile
                return p
            else:
                raise Exception("Error while calling API.")
        except Exception as err:
            print(f"Error occured while fetching profile data: {err}")
            return None

    def login(self, username, passwd):
        def get_md5_hash(input_string):
            return hashlib.md5(input_string.encode("utf-8")).hexdigest() # nosec
        try:
            api_url = f"/api/login.php"
            gameversion = 3 ## Game version specified in game server api
            salted_pswd = passwd + "taikotaiko" ## Adding salt to password
            pswd_hash = get_md5_hash(salted_pswd) ## Hashing password
            username = username.strip()
            params = {
                "username": username,
                "password": pswd_hash,
                "version": str(gameversion)
            }
            ## Requesting to API for verification process
            response = r.do(isDroid=True, request_type="POST", api_endpoint=api_url, data=params)
            if response.status == 200:
                response = response.text()
                response = response.splitlines()
                if len(response) >= 2:
                    data = response[1].split()
                    if len(data) < 6:
                        raise Exception
                else:
                    raise Exception
            else:
                raise Exception(f"Response is not 200. Status: {response.status}")
        except Exception as err:
            print(f"Error occured while logging into droid servers: {err}")
            return False
        uid = int(data[0])
        return uid

    def get_recent(self, uid, index):
        try:
            async with aiohttp.ClientSession() as session:
                api_url = f'{self.droid_api}/recent?id={uid}&index={index}'
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        rp = self()
                        ## Parsing the data
                        if isinstance(data, list):
                            item = data[0]
                            rp.acc = float(item.get("acc"))
                            rp.combo = item.get("combo")
                            rp.h100 = item.get("hit100")
                            rp.h300 = item.get("hit300")
                            rp.h50 = item.get("hit50")
                            rp.hmiss = item.get("hitmiss")
                            rp.mods = Mods(item.get("mods")).convert_std
                            rp.pp = item.get("pp")
                            maphash = item.get("maphash")
                            rp.map = oapi.get_mapdata_fromhash(maphash)
                            if rp.map is None:
                                raise Exception("No map found.")
                            return rp
                        else:
                            raise Exception("Server data is not list.")
                    else:
                        raise Exception(f"Response is not 200. Status: {response.status}")
        except Exception as err:
            print(f"Error occured fetching recent plays from UID {uid} for index {index}: {err}")
            return None

    def wl_fromset(self, setid, isAdd=True):
        try:
            beatmap_ids = oapi.get_mapid_fromset(setid)
            if beatmap_ids is not None:
                for beatmap_id in beatmap_ids:
                    ## Inserting maps into whitelist
                    async with aiohttp.ClientSession() as session:
                        api_url = f'{self.droid_api}/wl_add?key={config.wl_key}&bid={beatmap_id}' if isAdd is True else api_url == f'{self.droid_api}/wl_rm?key={config.wl_key}&bid={beatmap_id}'
                        async with session.get(api_url) as response:
                            if response.status == 200:
                                print(f"{beatmap_id} added to whitelist.") if isAdd is True else print(f"{beatmap_id} removed from whitelist")
                            else:
                                raise Exception(f"Could not fetch map ids, maybe map does not exist. (mapid = {beatmap_id})")
            else:
                raise Exception(f"Could not fetch map ids, maybe set does not exist. (setid = {setid})")
        except Exception as err:
            print(f"Error occured while adding maps to whitelist: {err}")
            return None


class OsuAPI:
    def __init__(self):
        self.osu_key = config.osu_key

    def get_mapdata_fromhash(self, hash):
        try:
            async with aiohttp.ClientSession() as session:
                osuapi = self.osu_api.join(f"/get_beatmaps?k={config.osu_key}&h={hash}")
                async with session.get(osuapi) as response:
                    if response.status == 200:
                        data = await response.json()
                        m = self()
                        ## Parsing map data
                        if isinstance(data, list):
                            for item in data:
                                m.artist = item.get("artist")
                                m.title = item.get("title")
                                m.version = item.get("version")
                                m.max_combo = item.get("max_combo")
                                m.sr = float(item.get("difficultyrating"))
                                m.setid = item.get("beatmapset_id")
                                m.diffid = item.get("beatmap_id")
                                return m
                    else:
                        raise Exception(f"Mapdata API is not 200 (Status: {response.status})")
        except Exception as err:
            print(f"Error occured while fetching mapdata from hash {hash}: {err}")
            return None

    def get_mapid_fromset(self, setid):
        try:
            async with aiohttp.ClientSession() as session:
                api_url = self.osu_api.join(f"/get_beatmaps?k={config.osu_key}&s={setid}")
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        beatmap_ids = [item['beatmap_id'] for item in data if 'beatmap_id' in item]
                        return beatmap_ids
                    else:
                        raise Exception(f"Could not get MapIDs from set {setid}")
        except Exception as err:
            print(f"Error occured while fetching map ids from mapset {setid}: {err}")
            return None
