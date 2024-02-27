from genericpath import exists
from json import loads
import requests
import config
import log
import lxml.etree as etree
import datetime
import os
import time
import sqlite3

HEADERS = {
    'Content-Type': 'application/json',
    'ApiKey': f'{config.api_key}',
    'Accept': 'application/json',
    'Connection': 'keep-alive',
    'DNT': '1',
}

def make_graphql_request(query):
    try:
        json_query = {"query": query}
        response = requests.post(config.graphql_url, json=json_query, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log.error(f"Error making GraphQL request: {e}")
        return None

def write_nfo(root, file_path):
    xml_string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")
    file = open(file_path, 'wb')
    try:
        file.write(xml_string)
    finally:
        file.close()
        log.info(f"Added {file_path}")

def process_scene(scene):
    root = etree.Element("movie")

    # Title
    title_element = etree.SubElement(root, "title")
    title_element.text = scene['title']

    # Original Title
    original_title_element = etree.SubElement(root, "originaltitle")
    original_title_element.text = scene['title']

    # Sort Title
    sort_title_element = etree.SubElement(root, "sorttitle")
    sort_title_element.text = scene['title']

    # User Rating
    userrating_element = etree.SubElement(root, "userrating")
    userrating_element.text = str(scene['rating100'])

    # Plot
    plot_element = etree.SubElement(root, "plot")
    plot_element.text = str(scene['details'])

    # Studio Thumbnail (Logo)
    thumb_studio_element = etree.SubElement(root, "thumb", attrib={"aspect": "clearlogo"})
    if scene['studio'] is None:
        thumb_studio_element.text = ""
    else:
        thumb_studio_element.text =  scene['studio']['image_path']

    # Landscape Thumbnail
    thumb_landscape_element = etree.SubElement(root, "thumb", attrib={"aspect": "landscape"})
    thumb_landscape_element.text = scene['paths']['screenshot']

    # Vertical Thumbnail
    thumb_poster_element = etree.SubElement(root, "thumb", attrib={"aspect": "poster"})
    thumb_poster_element.text = scene['paths']['screenshot']

    # Fanart Thumbnail
    fanart_element = etree.SubElement(root, "fanart")
    fanart_thumb_element = etree.SubElement(fanart_element, "thumb")
    fanart_thumb_element.text = scene['paths']['screenshot']

    # MPAA Rating
    mpaa_element = etree.SubElement(root, "mpaa")
    mpaa_element.text = "XXX"

    # Play Count
    playcount_element = etree.SubElement(root, "playcount")
    playcount_element.text = str(scene['play_count'])

    # Unique ID
    unique_id_element = etree.SubElement(root, "uniqueid")
    unique_id_element.set("default", "true")
    unique_id_element.text = str(scene['id'])

    # Stash IDs
    for stash_id in scene['stash_ids']:
        stash_id_element = etree.SubElement(root, "uniqueid", type="stashdb")
        stash_id_element.text = str(stash_id['stash_id'])

    # Tag
    for tag in scene['tags']:
        tag_element = etree.SubElement(root, "tag")
        tag_element.text = tag['name']

    # Set
    set_element = etree.SubElement(root, "set")
    set_name_element = etree.SubElement(set_element, "name")
    if scene['studio'] is None:
        set_name_element.text = "No Studio"
    else:
        set_name_element.text = scene['studio']['name']

    # Director
    director_element = etree.SubElement(root, "director")
    director_element.text = scene['director']

    # Premiered Date
    premiered_element = etree.SubElement(root, "premiered")
    premiered_element.text = scene['date']

    # Year
    if scene['date'] is not None:
        year_element = etree.SubElement(root, "year")
        year_element.text = str(datetime.datetime.strptime(str(scene['date']),"%Y-%m-%d").year)

    # Studio
    studio_element = etree.SubElement(root, "studio")
    if scene['studio'] is None:
         studio_element.text = ""
    else:
         studio_element.text = scene['studio']['name']

    # File Information
    for file_info in scene['files']:
        fileinfo_element = etree.SubElement(root, "fileinfo")
        streamdetails_element = etree.SubElement(fileinfo_element, "streamdetails")

        # Video
        video_element = etree.SubElement(streamdetails_element, "video")
        video_codec_element = etree.SubElement(video_element, "codec")
        video_codec_element.text = file_info['video_codec']
        aspect_element = etree.SubElement(video_element, "aspect")
        aspect_element.text = str(round(file_info['width'] / file_info['height'], 2))
        width_element = etree.SubElement(video_element, "width")
        width_element.text = str(file_info['width'])
        height_element = etree.SubElement(video_element, "height")
        height_element.text = str(file_info['height'])
        duration_element = etree.SubElement(video_element, "durationinseconds")
        duration_element.text = str(file_info['duration'])

        # Audio
        audio_element = etree.SubElement(streamdetails_element, "audio")
        audio_codec_element = etree.SubElement(audio_element, "codec")
        audio_codec_element.text = file_info['audio_codec']


    # Actors
    order = 0
    for actor in scene['performers']:
        actor_element = etree.SubElement(root, "actor")
        actor_name_element = etree.SubElement(actor_element, "name")
        actor_name_element.text = actor['name']
        order_element = etree.SubElement(actor_element, "order")
        order_element.text = str(order)
        image_element = etree.SubElement(actor_element, "thumb", attrib={"aspect": "poster"})
        image_element.text = actor['image_path']
        order += 1

    # Date Added
    dateadded_element = etree.SubElement(root, "dateadded")
    dateadded_element.text = str(scene['created_at'])

    return root

query = """
{
   allScenes {
    id
    title
    details
    director
    date
    rating100
    organized
    play_count
    created_at
    updated_at
    files {
      path
      video_codec
      width
      height
      duration
      audio_codec
    }
    paths {
      screenshot
    }
    studio {
      name
      id
      url
      image_path
    }
    tags {
      name
    }
    performers {
      name
      gender
      image_path
      url
    }
    stash_ids {
      stash_id
    }
  }
}
"""

START_TIME = time.time()

conn = sqlite3.connect('updates_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS scenes (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    last_updated_at TEXT
                  )''')
conn.commit()
cursor.execute("SELECT id, last_updated_at FROM scenes")
rows = cursor.fetchall()
last_updated_dict = {row[0]: row[1] for row in rows}

r = make_graphql_request(query)

if r is not None:
    if config.generate_nfo_for_files in ['Organized', 'Unorganized', 'All']:
        organizedScenes = [scene for scene in r.get('data', {}).get('allScenes', [])
                           if (config.generate_nfo_for_files == 'Organized' and scene['organized']) or
                           (config.generate_nfo_for_files == 'Unorganized' and not scene['organized']) or
                           (config.generate_nfo_for_files == 'All')]

        for scene in organizedScenes:
            file_path = scene['files'][0]['path']
            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            file_base_dir = os.path.dirname(file_path)
            nfo_file_name = f'{file_name_without_ext}.nfo'
            # For testing only save path is my local  nfo_test folder !
            nfo_file_path = os.path.join(file_base_dir, nfo_file_name)
            if int(scene['id']) in last_updated_dict and scene['updated_at'] == last_updated_dict[int(scene['id'])] and os.path.exists(nfo_file_path):
                 continue
            else:
                print("Changes Detected Adding to Database" +scene['title'] )
                cursor.execute('''INSERT OR REPLACE INTO scenes (id, title, last_updated_at)
                                VALUES (?, ?, ?)''', (scene['id'], scene['title'], scene['updated_at']))
                conn.commit()
                last_updated_dict[scene['id']] = scene['updated_at']
        for scene in organizedScenes:
            file_path = scene['files'][0]['path']
            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            file_base_dir = os.path.dirname(file_path)
            nfo_file_name = f'{file_name_without_ext}.nfo'
            # For testing only save path is my local  nfo_test folder !
            nfo_file_path = os.path.join(file_base_dir, nfo_file_name)
            if int(scene['id']) in last_updated_dict and scene['updated_at'] == last_updated_dict[int(scene['id'])] and os.path.exists(nfo_file_path):
                 continue
            else:
                print("Changes Detected" ,scene['title'] )
                root = process_scene(scene)
                file_path = scene['files'][0]['path']
                file_name = os.path.basename(file_path)
                file_name_without_ext = os.path.splitext(file_name)[0]
                file_base_dir = os.path.dirname(file_path)
                nfo_file_name = f'{file_name_without_ext}.nfo'
                # For testing only save path is my local  nfo_test folder !
                # For Custom Path you can change base dir
                nfo_file_path = os.path.join(file_base_dir, nfo_file_name)
                write_nfo(root, nfo_file_path)
        log.debug("Execution time: {}s".format(round(time.time() - START_TIME, 5)))
    else:
        log.error("Please Check config -> make_graphql_request")
else:
    log.error("No response from GraphQL server")
