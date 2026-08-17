import yaml
import xml.etree.ElementTree as xml_tree

with open('feed.yaml', 'r') as file:
  yaml_data = yaml.safe_load(file)

  rss_element = xml_tree.Element('rss', {'version':'2.0',
    'xmlns:itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content':'http://purl.org/rss/1.0/modules/content/'})

channel_element = xml_tree.SubElement(rss_element, 'channel')

link_prefix = yaml_data['link']

xml_fields = {
  'title': 'title',
  'format': 'format',
  'subtitle': 'subtitle',
  'itunes:author': 'author',
  'description': 'description',
  'language': 'language',
}

for element_name, yaml_key in xml_fields.items():
  xml_tree.SubElement(channel_element, element_name).text = yaml_data[yaml_key]

xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
xml_tree.SubElement(channel_element, 'link').text = link_prefix

xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

for item in yaml_data['item']:
  item_element = xml_tree.SubElement(channel_element, 'item')
  item_fields = {
    'title': item['title'],
    'itunes:author': yaml_data['author'],
    'description': item['description'],
    'itunes:duration': item['duration'],
    'pubDate': item['published'],
  }

  for element_name, value in item_fields.items():
    xml_tree.SubElement(item_element, element_name).text = value

  xml_tree.SubElement(item_element, 'enclosure', {
    'url': link_prefix + item['file'],
    'type': yaml_data['format'],
    'length': item['length'],
  })

output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)