import config
from utils.requests import Requests as r
from objects.player import Player
from objects.mapdata import Map
import hashlib


class DroidAPI:
    def __init__(self):
        self.wl_key = config.wl_key

    def get_profile(self, uid):
        api_url = f"/get_user?id={uid}"
        try:
            response = r().do(isDroid=True, request_type="GET", api_endpoint=api_url)
            if response.status_code == 200:
                data = response.json()
                p = Player(data).parse_profile
                return p
            else:
                raise Exception(
                    f"Error while calling API. (Status Code = {response.status_code})"
                )
        except Exception as err:
            print(f"Error occured while fetching profile data: {err}")
            return None

    def login(self, username, passwd):
        def get_md5_hash(input_string):
            return hashlib.md5(input_string.encode("utf-8")).hexdigest()  # nosec

        try:
            api_url = f"/login.php"
            gameversion = 2  ## Game version specified in game server api
            salted_pswd = passwd + "taikotaiko"  ## Adding salt to password
            pswd_hash = get_md5_hash(salted_pswd)  ## Hashing password
            username = username.strip()
            params = {
                "username": username,
                "password": pswd_hash,
                "version": str(gameversion),
            }
            ## Requesting to API for verification process
            response = r().do(
                isDroid=True, request_type="POST", api_endpoint=api_url, data=params
            )
            if response.status_code == 200:
                response = response.text
                response = response.splitlines()
                if len(response) >= 2:
                    data = response[1].split()
                    if len(data) < 6:
                        raise Exception("1")
                else:
                    raise Exception("2")
            else:
                raise Exception(
                    f"Response is not 200. status_code: {response.status_code}"
                )
        except Exception as err:
            print(
                f"Error occured while logging into droid servers: {err}, response: {response}"
            )
            return False
        uid = int(data[0])
        return uid

    def get_recent(self, uid, index):
        try:
            api_url = f"/recent?id={uid}&offset={index}"
            response = r().do(isDroid=True, request_type="GET", api_endpoint=api_url)
            if response.status_code == 200:
                data = response.json()
                rp = Player(data).parse_recent
                return rp
            else:
                raise Exception(
                    f"Response is not 200. status_code: {response.status_code}"
                )
        except Exception as err:
            print(
                f"Error occured fetching recent plays from UID {uid} for index {index}: {err}"
            )
            return None

    def wl_fromset(self, setid, isAdd=True):
        try:
            beatmap_ids = OsuAPI().get_mapid_fromset(setid=setid)
            if beatmap_ids is not None:
                for beatmap_id in beatmap_ids:
                    ## Inserting maps into whitelist
                    api_url = (
                        f"/wl_add?key={self.wl_key}&bid={beatmap_id}"
                        if isAdd is True
                        else api_url = f"/wl_rm?key={self.wl_key}&bid={beatmap_id}"
                    )
                    response = r().do(
                        isDroid=True, request_type="GET", api_endpoint=api_url
                    )
                    if response.status_code == 200:
                        print(
                            f"{beatmap_id} added to whitelist."
                        ) if isAdd is True else print(
                            f"{beatmap_id} removed from whitelist"
                        )
                    else:
                        raise Exception(
                            f"Could not fetch map ids, maybe map does not exist. (mapid = {beatmap_id})"
                        )
            else:
                raise Exception(
                    f"Could not fetch map ids, maybe set does not exist. (setid = {setid})"
                )
        except Exception as err:
            print(f"Error occured while adding/removing maps to whitelist: {err}")
            return None

    def wl_fromid(self, mapid, isAdd=True):
        try:
            api_url = (
                f"/wl_add?key={self.wl_key}&bid={mapid}"
                if isAdd is True else f"/wl_rm?key={self.wl_key}&bid={mapid}"
            )
            response = r().do(isDroid=True, request_type="GET", api_endpoint=api_url)
            if response.status_code == 200:
                print(f"{mapid} added to whitelist.") if isAdd is True else print(
                    f"{mapid} removed from whitelist"
                )
            else:
                raise Exception(f"Could not add/remove map from wl. (mapid= {mapid})")
        except Exception as err:
            print(f"Error occured while adding/removing maps to whitelist: {err}")


class OsuAPI:
    def __init__(self):
        self.apikey = config.osu_key

    def get_mapdata_fromhash(self, hash):
        try:
            api_url = f"/get_beatmaps?k={self.apikey}&h={hash}"
            response = r().do(isDroid=False, request_type="GET", api_endpoint=api_url)
            if response.status_code == 200:
                data = response.json()
                m = Map(data).parse_mapdata
                return m
            else:
                raise Exception(
                    f"Mapdata API is not 200 (status_code: {response.status_code})"
                )
        except Exception as err:
            print(f"Error occured while fetching mapdata from hash {hash}: {err}")
            return None

    def get_mapid_fromset(self, setid):
        try:
            api_url = f"/get_beatmaps?k={self.apikey}&s={setid}"
            response = r().do(isDroid=False, request_type="GET", api_endpoint=api_url)
            if response.status_code == 200:
                data = response.json()
                beatmap_ids = [
                    item["beatmap_id"] for item in data if "beatmap_id" in item
                ]
                return beatmap_ids
            else:
                raise Exception(f"Could not get MapIDs from set {setid}")
        except Exception as err:
            print(f"Error occured while fetching map ids from mapset {setid}: {err}")
            return None
