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
                            "red": color[0],
                            "green": color[1],
                            "blue": color[2]
                        }
                    }
                }
            },
            "index": 0
        }
    }
