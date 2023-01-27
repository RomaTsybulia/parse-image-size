import asyncio

import gspread

from oauth2client.service_account import ServiceAccountCredentials

from data.secret_variables import PATH
from parse import parse_image_sizes

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

CREDS = ServiceAccountCredentials.from_json_keyfile_name(PATH, scopes=SCOPES)

START_FIELD_GET = "A3"
END_FIELD_GET = "A46889"

START_FIELD_PUT = "B3"
END_FIELD_PUT = "B46889"


def connection_to_sheet():
    file = gspread.authorize(CREDS)
    workbook = file.open("Image_sizes")
    return workbook.sheet1


def get_urls_from_sheet():
    sheet = connection_to_sheet()
    return [
        url.value
        for url in sheet.range(f"{START_FIELD_GET}:{END_FIELD_GET}")
    ]


def get_all_sizes():
    image_sizes = []
    end_field = 0
    step = 50
    urls = get_urls_from_sheet()

    while end_field <= len(urls):
        start_field = end_field
        if end_field + step > len(urls):
            end_field = len(urls) + 2
        else:
            end_field += step

        image_sizes.extend(asyncio.run(parse_image_sizes(urls[start_field:end_field])))

    return image_sizes


def insert_sizes_into_sheet():
    sheet = connection_to_sheet()
    size_list = get_all_sizes()
    sheet.update(f"{START_FIELD_PUT}:{END_FIELD_PUT}", size_list)


def main():
    insert_sizes_into_sheet()


if __name__ == "__main__":
    main()
