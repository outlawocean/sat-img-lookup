import os
import requests
import geojson
import urllib.parse

def load_access_token():
    access_token = os.getenv('MAPBOX_ACCESS_TOKEN')
    if access_token is None:
        raise Exception("MAPBOX_ACCESS_TOKEN environment variable is not set.")
    return access_token


def set_options(opt):
    """
    Process options dictionary, override defaults with those given.
    """
    default = {}
    default['zoom'] = '16.5'
    default['width'] = 800
    default['height'] = 600
    default['access_token'] = load_access_token()
    default.update(opt)
    return default

def buildGeoJSON(lon, lat):
    pointGeoJSON = geojson.Point((float(lon), float(lat)))
    return f"geojson({geojson.dumps(pointGeoJSON)})"

def url(options):
    if options["marker"]:
        return f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{buildGeoJSON(options['lon'], options['lat'])}/{options['lon']},{options['lat']},{options['zoom']}/{options['width']}x{options['height']}@2x?access_token={options['access_token']}"
    else:
        return f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{options['lon']},{options['lat']},{options['zoom']}/{options['width']}x{options['height']}@2x?access_token={options['access_token']}"

def output_path(folder, id):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return os.path.join(folder, f"{id}.jpg")


def image_url(opts):
    # service = Static()
    options = set_options(opts)
    request_url = url(options)

    return request_url


def save_image(url, id, opts):
    response = requests.get(url)
    # print(url)
    # print(response.status_code)
    if response.status_code == 200:
        with open(output_path(opts['download_folder'], id), 'wb') as image_file:
            print(output_path(opts['download_folder'], id))
            image_file.write(response.content)
    else:
        print(f"Failed to fetch image: {url}")
