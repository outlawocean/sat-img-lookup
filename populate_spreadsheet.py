from datetime import date
import os
import pandas as pd
import pprint
from mapbox_helper import image_url, save_image
import uuid
import time

EXCEL_EXTENSIONS = [ "xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt" ]
CSV_EXTENSIONS = [ "csv", "tsv" ]

def set_output_file_name(spreadsheet_file_name, output):
    [file_name, file_ext] = os.path.splitext(
        os.path.split(spreadsheet_file_name)[1]
    )
    if output == '<timestamp>':
        output = f"{file_name}_{date.today().isoformat()}{file_ext}"
    return output


def load_spreadsheet(spreadsheet_file_name):
    print(f"Reading: {spreadsheet_file_name}")
    file_ext = str.lower(os.path.splitext(
        os.path.split(spreadsheet_file_name)[1]
    )[1][1:])

    if file_ext in EXCEL_EXTENSIONS:
        return pd.read_excel(spreadsheet_file_name, dtype=str)
    elif file_ext in CSV_EXTENSIONS:
        return pd.read_csv(spreadsheet_file_name, dtype=str, sep="\t" if file_ext == "tsv" else ",")
    else:
        raise Exception(f"Unsupported file extension: {file_ext}")


def fetch_image_url(lon, lat, zoom, marker):
    # print(id, ": ", lat, "-" ,lon)
    return image_url({"lat": lat, "lon": lon, "zoom": zoom, "marker": marker})


def write_output(spreadsheet_data, output_file_name):
    print(f"Writing: ./{output_file_name}")
    file_ext = os.path.splitext(output_file_name)[1][1:]
    if file_ext in EXCEL_EXTENSIONS:
        spreadsheet_data.to_excel(output_file_name, index=False)
    elif file_ext in CSV_EXTENSIONS:
        spreadsheet_data.to_csv(output_file_name, index=False, sep="\t" if file_ext == "tsv" else ",")

def main(options):
    output_file_name = set_output_file_name(options['spreadsheet_file_name'], options['output'])
    spreadsheet_data = load_spreadsheet(options['spreadsheet_file_name'])
    # print(output_file_name)

    if "id" not in spreadsheet_data.columns:
        spreadsheet_data['id'] = [uuid.uuid5(uuid.NAMESPACE_DNS, f"{row['Latitude']}-{row['Longitude']}") for i, row in spreadsheet_data.iterrows()]
        id_col = spreadsheet_data.pop('id')
        spreadsheet_data.insert(0, 'id', id_col)

    for i, row in spreadsheet_data.iterrows():
        image_url = fetch_image_url(row['Longitude'], row['Latitude'], options["zoom"], options["marker"])
        # print(image_url)
        if options['save_images']:
            save_image(image_url, row['id'], options)
            if i > 0 and i % 100 == 0:
                print("sleeping...")
                time.sleep(10)
        spreadsheet_data.loc[spreadsheet_data['id'] == row['id'], 'Imagery'] = image_url

    if not options['save_images']:
        spreadsheet_data.pop('id')

    write_output(spreadsheet_data, output_file_name)
