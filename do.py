from dotenv import load_dotenv
from src.dropletclitools import DropletCliTools
import os

load_dotenv()
DO_TOKEN = os.environ['DO_TOKEN']
MATTERMOST_WEBHOOK_URL = os.environ['MATTERMOST_WEBHOOK_URL']

def run_select():
    test = DropletCliTools(DO_TOKEN, MATTERMOST_WEBHOOK_URL)
    test.create_snapshot_for_droplets_in_csv('droplets.csv')
run_select()


