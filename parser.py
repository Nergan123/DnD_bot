import xml.etree.ElementTree as ET
import os
import random


class Parser:
    def __init__(self, campaign=''):
        self.campaign = campaign
        self.path = os.path.join(os.getcwd(), 'campaign', self.campaign, 'map.xml')
        self.path_npc_xml = os.path.join(os.getcwd(), 'campaign', self.campaign)

    def get_music(self, location=''):
        root_node = ET.parse(self.path).getroot()

        listing_url = []
        for child in root_node:
            if child.attrib['Name'] == location:
                music_list = child.find('music_calm')
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
            image = child.find('Image').text
            mechanics = child.find('Mechanics').text
            bestiary = child.find('Bestiary').text

        return name, image, mechanics, bestiary
