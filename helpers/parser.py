import xml.etree.ElementTree as ET
import os
import random


class Parser:
    def __init__(self, campaign='', path=''):
        self.campaign = campaign
        self.path = os.path.join(path, 'campaign', self.campaign, 'map.xml')
        print(self.path)
        self.path_npc_xml = os.path.join(path, 'campaign', self.campaign)

    def get_music(self, location='', battle=False):
        root_node = ET.parse(self.path).getroot()

        listing_url = []
        if battle:
            tag = 'music_battle'
        else:
            tag = 'music_calm'

        for child in root_node:
            if child.attrib['Name'] == location:
                music_list = child.find(tag)
                urls = music_list.findall('url')
                for link in urls:
                    listing_url.append(link.text)

        return random.choice(listing_url)

    def get_location_image(self, location=''):
        root_node = ET.parse(self.path).getroot()

        for child in root_node:
            if child.attrib['Name'] == location:
                return child.attrib['image']

    def get_all_locations(self):
        root_node = ET.parse(self.path).getroot()

        locations = []
        for child in root_node:
            locations.append(child.attrib["Name"])

        return locations

    def get_npc(self, location='', name=''):
        root_node = ET.parse(self.path).getroot()

        for child in root_node:
            if child.attrib['Name'] == location:
                list_of_npcs = child.findall('NPC')
                for npc in list_of_npcs:
                    if name == npc.attrib['name']:
                        return npc.text

        return False

    def get_npc_info(self, xml):
        path = os.path.join(self.path_npc_xml, xml)
        root_node = ET.parse(path).getroot()
        for child in root_node:
            name = child.find('Name').text
            boss = child.find('Boss').text
            if boss == 0:
                boss = False
            else:
                boss = True
            image = child.find('Image').text
            mechanics = child.find('Mechanics').text
            bestiary = child.find('Bestiary').text

        return name, boss, image, mechanics, bestiary
