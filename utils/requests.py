from requests import get, post
import config

class Requests:
    def __init__(self):
        self.odrx_url = config.domain
        self.odrx_api = f"{config.domain}/api"
        self.osu_api = "https://osu.ppy.sh/api"
    
    def do(self, isDroid: bool = False, request_type: str = None, api_endpoint: str = None, data: dict = None):
        try:
            if request_type not in ["GET", "POST"]:
                raise Exception("Request type must be POST or GET.")  
            if request_type == "GET":
               r = get(url=self.odrx_api + api_endpoint) if isDroid is True else get(url=self.osu_api + api_endpoint)
               return r
            elif request_type == "POST":
                if data is None:
                    raise Exception("Data must be sent while making a POST request.")
                r = post(url=self.odrx_api + api_endpoint, data=data) if isDroid is True else get(url=self.osu_api + api_endpoint, data=data)
                return r
        except Exception as err:
            print(f"Error ocurred while trying to make a request to an API (isDroid = {isDroid}, err: {err})")
            return None