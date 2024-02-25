import requests
import config
import log
import lxml.etree as etree
import datetime
import os
import time

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

    # Unique ID
    unique_id_element = etree.SubElement(root, "uniqueid")
    unique_id_element.text = str(scene['id'])

    # Stash IDs
    for stash_id in scene['stash_ids']:
        stash_id_element = etree.SubElement(root, "uniqueid", type="stashdb")
        stash_id_element.text = str(stash_id['stash_id'])

    # MPAA Rating
    mpaa_element = etree.SubElement(root, "mpaa")
    mpaa_element.text = "XXX"  # Adjust as per your requirements

    # Play Count
    playcount_element = etree.SubElement(root, "playcount")
    playcount_element.text = str(scene['play_count'])

    # Date Added
    dateadded_element = etree.SubElement(root, "dateadded")
    dateadded_element.text = str(scene['created_at'])

    # Premiered Date
    premiered_element = etree.SubElement(root, "premiered")
    premiered_element.text = scene['date']

    # Year
    if scene['date'] is not None:
        year_element = etree.SubElement(root, "year")
        year_element.text = str(datetime.datetime.strptime(str(scene['date']),"%Y-%m-%d").year)

    # User Rating
    userrating_element = etree.SubElement(root, "userrating")
    userrating_element.text = str(scene['rating100'])

    # Plot
    plot_element = etree.SubElement(root, "plot")
    plot_element.text = scene['details']

    # Outline
    outline_element = etree.SubElement(root, "outline")
    outline_element.text = scene['details']

    # Studio
    studio = scene['studio']
    studio_element = etree.SubElement(root, "studio")
    studio_element.text = studio['name']
    studio_id_element = etree.SubElement(studio_element, "id")
    studio_id_element.text = str(studio['id'])
    studio_url_element = etree.SubElement(studio_element, "url")
    studio_url_element.text = studio['url']

    # Studio Thumbnail
    thumb_studio_element = etree.SubElement(root, "thumb", attrib={"aspect": "clearlogo"})
    thumb_studio_element.text = studio['image_path']

    # Set
    set_element = etree.SubElement(root, "set")
    set_name_element = etree.SubElement(set_element, "name")
    set_name_element.text = studio['name']
    set_thumb_element = etree.SubElement(set_element, "thumb", attrib={"aspect": "poster"})
    set_thumb_element.text = studio['image_path']

    # Director
    director_element = etree.SubElement(root, "director")
    director_element.text = scene['director']

    # Thumbnails
    thumb_poster_element = etree.SubElement(root, "thumb", attrib={"aspect": "poster"})
    thumb_poster_element.text = scene['paths']['screenshot']

    thumb_landscape_element = etree.SubElement(root, "thumb", attrib={"aspect": "landscape"})
    thumb_landscape_element.text = scene['paths']['screenshot']

    fanart_element = etree.SubElement(root, "fanart")
    fanart_thumb_element = etree.SubElement(fanart_element, "thumb")
    fanart_thumb_element.text = scene['paths']['screenshot']

    # Actors
    for actor in scene['performers']:
        actor_element = etree.SubElement(root, "actor")
        actor_name_element = etree.SubElement(actor_element, "name")
        actor_name_element.text = actor['name']
        gender_element = etree.SubElement(actor_element, "gender")
        gender_element.text = actor['gender']
        image_element = etree.SubElement(actor_element, "thumb", attrib={"aspect": "poster"})
        image_element.text = actor['image_path']
        profile_element = etree.SubElement(actor_element, "profile")
        profile_element.text = actor['url']

    # Genre
    for tag in scene['tags']:
        tag_element = etree.SubElement(root, "tag")
        tag_element.text = tag['name']

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

r = make_graphql_request(query)

if r is not None:
    if config.generate_nfo_for_files in ['Organized', 'Unorganized', 'All']:
        organizedScenes = [scene for scene in r.get('data', {}).get('allScenes', [])
                           if (config.generate_nfo_for_files == 'Organized' and scene['organized']) or
                           (config.generate_nfo_for_files == 'Unorganized' and not scene['organized']) or
                           (config.generate_nfo_for_files == 'All')]
        
        
        for scene in organizedScenes:
            root = process_scene(scene)
            file_path = scene['files'][0]['path'] 
            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            file_base_dir = os.path.dirname(file_path)
            nfo_file_name = f'{file_name_without_ext}.nfo'
            nfo_file_path = os.path.join(file_base_dir, nfo_file_name)
            write_nfo(root, nfo_file_path)
        log.debug("Execution time: {}s".format(round(time.time() - START_TIME, 5)))
    else:
        log.error("Please Check config -> make_graphql_request")
else:
    log.error("No response from GraphQL server")