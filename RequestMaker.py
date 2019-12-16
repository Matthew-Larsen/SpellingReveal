def get_merge_request(x0, x1, y0, y1):
    return {
        "mergeCells": {
            "range": {
                "startRowIndex": y0,
                "endRowIndex": y1,
                "startColumnIndex": x0,
                "endColumnIndex": x1
            },
            "mergeType": "MERGE_ALL"
        }
    }


def get_col_resize_request(size):
    return {
        "updateDimensionProperties": {
            "range": {
                "dimension": "COLUMNS",

            },
            "properties": {
                "pixelSize": size
            },
            "fields": "pixelSize"
        }
    }


def get_row_resize_request(size):
    return {
        "updateDimensionProperties": {
            "range": {
                "dimension": "ROWS",
            },
            "properties": {
                "pixelSize": size
            },
            "fields": "pixelSize"
        }
    }


def get_format_request(x, y, color, question_row, answer):
    return {
        "addConditionalFormatRule": {
            "rule": {
                "ranges": [
                    {
                        "startRowIndex": y,
                        "endRowIndex": y + 1,
                        "startColumnIndex": x + 4,
                        "endColumnIndex": x + 5,
                    }
                ],
                "booleanRule": {
                    "condition": {
                        "type": "CUSTOM_FORMULA",
                        "values": [
                            {
                                "userEnteredValue": "=$C$" + str(question_row + 1) + "=\"" + answer + "\""
                            }
                        ]
                    },
                    "format": {
                        "backgroundColor": {
                            "red": color[0] / 255,
                            "green": color[1] / 255,
                            "blue": color[2] / 255
                        }
                    }
                }
            },
            "index": 0
        }
    }


def get_create_request(name):
    return {
        "properties": {
            "title": name
        }
    }


def write_words_request(word, num):
    return {
        "range": "C" + str(num) + ":C" + str(num + 1),
        "majorDimension": "DIMENSION_UNSPECIFIED",
        "values": [[word]]
    }
