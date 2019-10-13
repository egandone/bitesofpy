from pathlib import Path
from urllib.request import urlretrieve
from collections import defaultdict

from bs4 import BeautifulSoup as Soup

out_dir = "/tmp"
html_file = f"{out_dir}/enchantment_list_pc.html"

HTML_FILE = Path(html_file)
URL = "https://www.digminecraft.com/lists/enchantment_list_pc.php"


class Enchantment:
    """Minecraft enchantment class

    Implements the following:
        id_name, name, max_level, description, items
    """

    def __init__(self, id_name, name, max_level, description):
        self.id_name = id_name
        self.name = name
        self.max_level = max_level
        self.description = description
        self.items = []

    def __str__(self):
        return f'{self.name} ({self.max_level}): {self.description}'


class Item:
    """Minecraft enchantable item class

    Implements the following:
        name, enchantments
    """

    def __init__(self, name):
        self.name = name
        self.enchantments = []

    def add_enchantment(self, enchantment):
        self.enchantments.append(enchantment)

    def __str__(self):
        title = self.name.replace('_', ' ').title()
        s = f'{title}: \n'
        s += '\n'.join([f'  [{e.max_level}] {e.id_name}'
                        for e in sorted(self.enchantments, key=lambda e: e.id_name)])
        return s


def parse_enchantment_cell(cell_text):
    """Transforms the text from the table to
    a tuple of (name, id)
    """
    (name, id) = cell_text.split('(')
    name = name.strip()
    id = id.strip(')')
    return (name, id)


# def parse_image_to_item_names(image_src):
#     for s in ['.', 'enchanted', 'iron', 'png', 'sm']:
#         image_src = image_src.replace(s, '')
#     return image_src.strip(' _').split('_')

def parse_image_to_item_names(image_src):
    image_src = image_src.replace('fishing_rod', 'fishingrod')
    for s in ['.', 'enchanted', 'iron', 'png', 'sm']:
        image_src = image_src.replace(s, '')
    image_src = image_src.strip(' _')
    image_src = image_src.replace('_', ' ')
    image_src = image_src.replace('fishingrod', 'fishing_rod')
    return image_src.split(' ')


def generate_enchantments(soup):
    """Generates a dictionary of Enchantment objects

    With the key being the id_name of the enchantment.
    """
    level_map = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7}
    items_table = soup.find_all('table', id='minecraft_items')
    if (len(items_table) != 1):
        raise ValueError(
            f'Expecting one and only one minecraft_items table - got {len(items_table)} instead')
    enchantments = dict()
    items_table = items_table[0]
    for item_row in items_table.find_all('tr'):
        item_cells = item_row.find_all('td')
        if len(item_cells) == 6:
            (name, name_id) = parse_enchantment_cell(item_cells[0].text)
            max_level = level_map[item_cells[1].text.strip()]
            description = item_cells[2].text
            image = item_cells[4].img['data-src'].split('/')[-1]
            enchantment = Enchantment(name_id, name, max_level, description)
            enchantment.items += parse_image_to_item_names(image)
            enchantments[name_id] = enchantment
    return enchantments


def generate_items(enchantments):
    """Generates a dictionary of Item objects

    With the key being the item name.
    """
    items = dict()
    for enchantment in enchantments.values():
        for item_id in enchantment.items:
            if item_id not in items:
                items[item_id] = Item(item_id)
            items[item_id].add_enchantment(enchantment)
    return items


def get_soup(file=HTML_FILE):
    """Retrieves/takes source HTML and returns a BeautifulSoup object"""
    if isinstance(file, Path):
        if not HTML_FILE.is_file():
            urlretrieve(URL, HTML_FILE)

        with file.open() as html_source:
            soup = Soup(html_source, "html.parser")
    else:
        soup = Soup(file, "html.parser")

    return soup


def main():
    """This function is here to help you test your final code.

    Once complete, the print out should match what's at the bottom of this file"""
    soup = get_soup()
    enchantment_data = generate_enchantments(soup)
    minecraft_items = generate_items(enchantment_data)
    for item in sorted(minecraft_items):
        print(minecraft_items[item], "\n")


if __name__ == "__main__":
    main()

"""
Armor:
  [1] binding_curse
  [4] blast_protection
  [4] fire_protection
  [4] projectile_protection
  [4] protection
  [3] thorns

Axe:
  [5] bane_of_arthropods
  [5] efficiency
  [3] fortune
  [5] sharpness
  [1] silk_touch
  [5] smite

Boots:
  [3] depth_strider
  [4] feather_falling
  [2] frost_walker

Bow:
  [1] flame
  [1] infinity
  [5] power
  [2] punch

Chestplate:
  [1] mending
  [3] unbreaking
  [1] vanishing_curse

Crossbow:
  [1] multishot
  [4] piercing
  [3] quick_charge

Fishing Rod:
  [3] luck_of_the_sea
  [3] lure
  [1] mending
  [3] unbreaking
  [1] vanishing_curse

Helmet:
  [1] aqua_affinity
  [3] respiration

Pickaxe:
  [5] efficiency
  [3] fortune
  [1] mending
  [1] silk_touch
  [3] unbreaking
  [1] vanishing_curse

Shovel:
  [5] efficiency
  [3] fortune
  [1] silk_touch

Sword:
  [5] bane_of_arthropods
  [2] fire_aspect
  [2] knockback
  [3] looting
  [1] mending
  [5] sharpness
  [5] smite
  [3] sweeping
  [3] unbreaking
  [1] vanishing_curse

Trident:
  [1] channeling
  [5] impaling
  [3] loyalty
  [3] riptide
"""
