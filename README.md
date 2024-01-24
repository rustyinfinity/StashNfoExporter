# StashNfoExporter

<img width="1188" alt="Screenshot 2024-01-24 at 4 23 41 PM" src="https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/b3d246e6-c486-4ac2-9035-486fc0c32b2e">
<br>
<br>
<h2 align="center">
 Make '.nfo' file from metadata obtained via Stash for services like Jellyfin Kodi Emby etc .
</h2>

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

### By default only Videos that it scan are set to organized ones. You can change organized to False if you want in config.py.

# If you have credentials  
Api key can be generated from security section in stash settings and added in config.py.

# Example !
<img width="939" alt="Screenshot 2024-01-22 at 3 14 44 PM" src="https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/2617cc02-27c8-4ab9-8123-0fa7fa117cf1">
<br>
<br>
<a href="https://github.com/rustyinfinity/StashNfoExporter/blob/main/example.nfo">Click here to see example.nfo file in the repo</a>

# Jellyfin Example

### Theme that I am using in first image is https://github.com/loof2736/scyfin

## Default Theme Examples 

![Screenshot 2024-01-23 at 11 33 42 AM](https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/8e78e5d0-d059-4c52-a7f7-cd0f561d627d)
![Screenshot 2024-01-23 at 11 37 53 AM](https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/cf256f18-303f-409a-bb1a-55e3907d9c49)
<img width="1433" alt="Screenshot 2024-01-24 at 4 24 39 PM" src="https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/69de2895-5369-4fb0-8a90-8528e8fff0cd">
<br>
<br>
# How i add to Kodi 
<img width="1142" alt="Screenshot 2024-01-22 at 9 07 22 AM" src="https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/fdf0a168-1123-4808-b00b-ff6fe53f2dd6">
<br>
# File Structure and File Names 
I will add .nfo naming according how you need once i get time in few weeks.
<br>
For Now i use this naming and achieve it by <a href="https://github.com/stashapp/CommunityScripts/tree/main/plugins/renamerOnUpdate">renamer plugin for stash</a>.
<br>
### You can also add all movies in same directory without creating subdirectories but make sure filenames are diffrent as now i have changed saving nfo as "filename.nfo".
<br>
<img width="1265" alt="Screenshot 2024-01-22 at 9 38 58 AM" src="https://github.com/rustyinfinity/StashNfoExporter/assets/115462641/4a599cfa-dba1-43af-b863-1d820f4cd21d">
<br>
Source: https://kodi.wiki/view/Naming_video_files/Movies

# Issue
If Movie poster is not showing you can add local ip (192.168.xxx.xxx) in config instead of localhost and readd the library. 

# Conclusion
I just created this plugin as the https://github.com/scruffynerf/StashNfoExporterKodi was broken after 24.1.
<br>
I don't use Emby but I think it will work fine there too.
<br>
There will be issues which I don't know yet so pls report them in issues Thanks !
