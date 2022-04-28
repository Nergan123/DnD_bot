import xml.etree.ElementTree as ET
import os
import random


class Parser:
    def __init__(self, campaign=''):
        self.campaign = campaign
        self.path = os.path.join(os.getcwd(), 'campaign', self.campaign, 'map.xml')

    def get_music(self, location=''):
        path_song = os.path.join(os.getcwd(), 'campaign', self.campaign, 'music', 'song.mp3')
        song_there = os.path.isfile(path_song)
        if song_there:
            os.remove(path_song)
        root_node = ET.parse(self.path).getroot()

        listing_url = []
        for child in root_node:
            music_list = child.find('music_calm')
            urls = music_list.findall('url')
            for link in urls:
                listing_url.append(link.text)

        return random.choice(listing_url)

    def get_all_locations(self):
        root_node = ET.parse(self.path).getroot()

        locations = []
        for child in root_node:
            locations.append(child.attrib["Name"])

        return locations
