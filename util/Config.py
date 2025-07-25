import os
import shutil

from pyhocon import ConfigFactory


class Config:
    def __init__(self):
        if not os.path.exists("./kuma.conf"):
            shutil.copyfile("./example.conf", "./kuma.conf")

        self.bots: list[str] = list()

        # info
        self.version = None
        # log
        self.log_level = None
        # nonebot
        self.listen_host = None
        self.listen_port = None
        self.token = None
        # group
        self.dev_group = None
        self.special_group = None
        # nsfw
        self.allowed_accounts = None
        # diving_fish
        self.df_token = None
        # lxns
        self.lx_token = None
        # admin
        self.admin_accounts = None
        # backend
        self.backend_url = None
        # llm
        self.ark_api_key = None
        self.llm_system_prompt = None
        self.llm_user_prompt = None
        self.llm_enabled_groups = None

        # 解析配置文件
        self.read_config()

    def read_config(self):
        data = ConfigFactory.parse_file("./kuma.conf")
        self.version = data["info"]["version"]
        self.log_level = data["log"]["log_level"]
        self.listen_host = data["nonebot"]["listen_host"]
        self.listen_port = data["nonebot"]["listen_port"]
        self.token = data["nonebot"]["token"]
        self.dev_group = data["group"]["dev"]
        self.special_group = data["group"]["special"]
        self.allowed_accounts = data["nsfw"]["allowed_accounts"]
        self.df_token = data["diving_fish"]["token"]
        self.lx_token = data["lxns"]["token"]
        self.admin_accounts = data["admin"]["accounts"]
        self.backend_url = data["backend"]["url"]
        self.ark_api_key = data["llm"]["ark_api_key"]
        self.llm_system_prompt = data["llm"]["system_prompt"]
        self.llm_user_prompt = data["llm"]["user_prompt"]
        self.llm_enabled_groups = data["llm"]["enabled_groups"]


config = Config()
