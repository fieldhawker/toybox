# coding: utf-8

import os

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'toybox/.env')
load_dotenv(dotenv_path)

# botアカウントのトークンを指定
API_TOKEN = os.environ.get("API_TOKEN")

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "何言ってんだこいつ"

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']
