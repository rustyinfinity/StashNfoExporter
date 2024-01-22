# StashNfoExporter
Export .nfo from Stash for services like Jellyfin Kodi Emby etc .

# Usage
Clone the repo to plugins folder of stash.

Make sure lxml and requests modules are installed.

```
pip install lxml requests
```

or 

```
pip install -r requirements.txt
```

# What it does ?
It will automatically create "filename.nfo" for all the organized files at the same directory of the video file when any movie is added or updated .

I don't use kodi regularly but use jellyfin and it works very nicely with it. 

I have added library as Movies and You can use select view as thumb in your library and it will show horizontal thumbs like stash with all the metadata.

You can change organized to False if you want.

Api key can be added in config if you have one.

# Example !
<img width="939" alt="Screenshot 2024-01-22 at 3 14 44 PM" src="https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/2617cc02-27c8-4ab9-8123-0fa7fa117cf1">
<img width="1067" alt="Screenshot 2024-01-22 at 9 34 14 AM" src="https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/6db29e48-32d6-4783-a2dd-b79c1f690e44">
<img width="1411" alt="Screenshot 2024-01-21 at 7 42 01 PM" src="https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/64a593fb-4f50-4dc1-b286-e7f8ca55df76">


# How i add to Kodi 
<img width="1142" alt="Screenshot 2024-01-22 at 9 07 22 AM" src="https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/fdf0a168-1123-4808-b00b-ff6fe53f2dd6">

# File Structure and File Names 
I will add .nfo naming according how you need once i get time in few weeks.

For Now i use this naming and achieve it by renamer plugin for stash.

You can also add all movies in same directory without creating subdirectories but make sure filenames are diffrent as now i have changed saving nfo as "filename.nfo".

<img width="1265" alt="Screenshot 2024-01-22 at 9 38 58 AM" src="https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/4a599cfa-dba1-43af-b863-1d820f4cd21d">
Source: https://kodi.wiki/view/Naming_video_files/Movies

# Issue
If Movie poster is not showing you can add local ip (192.168.xxx.xxx) in config instead of localhost and readd the library. 

# Conclusion
I just created this plugin as the https://github.com/scruffynerf/StashNfoExporterKodi was broken after 24.1.

There will be issues which I don't know yet so pls report them in issues Thanks !
