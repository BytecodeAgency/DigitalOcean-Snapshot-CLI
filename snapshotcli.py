from dotenv import load_dotenv
from src.dropletclitools import DropletCliTools
import os

load_dotenv()
DO_TOKEN = os.environ['DO_TOKEN']
MATTERMOST_WEBHOOK_URL = os.environ['MATTERMOST_WEBHOOK_URL']

cliTools = DropletCliTools(DO_TOKEN, MATTERMOST_WEBHOOK_URL)

def run_select():
    # cli_tools.create_snapshot_for_droplets_in_csv('droplets.csv')
    autosnaps = cliTools.dropletUtils.getAllAutoSnapshots()
    for snap in autosnaps:
        print(snap)
        # from dateutil import parser
        # date = parser.parse(snap.created_at)
        # print(date)
        # print(type(date))

run_select()

