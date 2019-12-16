import os.path
import pickle
import random

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from ImageLoader import *
from RequestMaker import *

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1cIPv9ON20eBlIb6ewWc3N78p4Gs3OP-sAzJA8j5QI2s'

# Some constants
# number of words needed to solve the puzzle
NUMWORDS = 10
# Size of side of the image (usually 2 * words)
IMAGESIZE = 20

ANSWERS = ["cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat"]
# Store picture here

def main():
    """
    Merges all of the cells in range 1 and 2 into 2x2 cell blocks
    :return: nothing
    """

    init(IMAGESIZE)

    # Get credentials and connect with the API
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'D:\Coding Projects\GoogleSheetsSpellingReveal\credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    requests = []
    # Merging the left hand cells into 2x2s
    requests.append(get_col_resize_request(50))
    requests.append(get_row_resize_request(50))
    for i in range(NUMWORDS):
        requests.append(get_merge_request(0, 2, i * 2, i * 2 + 2))
        requests.append(get_merge_request(2, 4, i * 2, i * 2 + 2))

    for x in range(IMAGESIZE):
        for y in range(IMAGESIZE):
            question_row = (random.randint(0, 9) * y + random.randint(0, 9) * x + random.randint(0, 9)) % NUMWORDS
            color = get_color_at_pos(x, y)
            answer = ANSWERS[question_row]
            requests.append(get_format_request(x, y, color, 2*question_row, answer))

    body = {'requests': requests}
    sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()



if __name__ == "__main__":
    main()
