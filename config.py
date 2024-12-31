from os import getenv
from dotenv import load_dotenv

## Loading env variables
load_dotenv()

## Your discord bot token
discord_token = getenv("TOKEN", "")

## Your osu v1 API key
osu_key = getenv("OSU_KEY", "")

## Your WhiteList add and remove key
wl_key = getenv("WL_KEY", "")

## Your discord server role id for whitelist moderation
wl_roleid = getenv("WL_ROLE", "")

## Your private server domain (or ip) (with http or https)
domain = "https://example.com"

## Your discord server guild id
guild_id = 1234567890
