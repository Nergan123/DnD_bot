import xml.etree.ElementTree as ET
import os
import random


class Parser:
    def __init__(self, campaign=''):
        if campaign == '':
            self.campaign = 'nergan_campaign'
        else:
            self.campaign = campaign

    def get_music(self, location=''):
        path = os.path.join(os.getcwd(), 'campaign', self.campaign, 'map.xml')
        path_song = os.path.join(os.getcwd(), 'campaign', self.campaign, 'music', 'song.mp3')
        song_there = os.path.isfile(path_song)
        if song_there:
            os.remove(path_song)
        root_node = ET.parse(path).getroot()

        listing_url = []
        listing_name = []
        for child in root_node:
            music_list = child.find('music_calm')
            urls = music_list.findall('url')
            for link in urls:
                listing_url.append(link.text)
                listing_name.append(link.attrib['Name'])
        if len(listing_url) > 0:
            num = random.randint(0, len(listing_url)-1)
        else:
            num = 0

        return listing_url[num], listing_name[num]
