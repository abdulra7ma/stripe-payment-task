from os.path import join

import gspread
from django.conf import settings

gs = gspread.service_account(join(
    "/Users/abdulrahmandawoud/handy/interviews/google_statistics_puller", "core", "google-cred.json"))
sh = gs.open("my test")
wk_sheet = sh.worksheet("Sheet1")


def orders_pullers(work_sheet: gspread.Worksheet):
    all_sheet_recorders = next(work_sheet.get_all_records)
