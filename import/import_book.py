#!/usr/bin/env python
import fire
from pathlib import Path
import os
import sys
from bs4 import BeautifulSoup
import yaml
#import html
import quopri

class Highlights(object):
    """converts book highlights"""

    def html_to_yaml(self, html_file):
        """
        converts html file to yaml (for highlights jekyll site)
        """
        html_path = Path(html_file)
        yaml_path = html_path.parent / '../../_data/' / (str(html_path.stem) + '.yml')
        yaml_path = yaml_path.resolve()
        highlights = []
        if not html_path.exists():
            print(f"{html_file} does not exist")
            return

        with html_path.open() as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        #print(f"soup={soup}")
        for annotation in soup.find_all(name="div", class_='3D"annotation"'):
            #print(f"annotation={annotation}")
            chapter = annotation.find(name='div', class_='3D"annotationchapter"').get_text().lstrip().rstrip()
            text = annotation.find(name='p', class_='3D"annotationrepresentativetext"').get_text().lstrip()
            text = quopri.decodestring(text)
            text = text.decode('utf8').rstrip()
            highlights.append({'text': text, 'page': chapter})

        with yaml_path.open(mode='w') as f:
            yaml.dump(highlights, f)

        print(f"wrote {len(highlights)} entries")
        # TODO: create 


if __name__ == '__main__':
    fire.Fire(Highlights)


