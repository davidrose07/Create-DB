import re
import os
import glob

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def convert_xml_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define the pattern and replacement for opening and closing tags
    content = re.sub(r'<version number="(\d+)">', r'<verse number="\1">', content)
    content = re.sub(r'</version>', r'</verse>', content)
    
    with open(file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(content)

search_pattern = os.path.join(root_dir, "XML", "*.xml")
for file_path in glob.glob(search_pattern):
    if os.path.isfile(file_path):
        convert_xml_tags(file_path)
    else:
        print(f"{file_path} is not a file")

