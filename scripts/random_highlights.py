import os
import sys
import argparse
from pathlib import Path
import random
import yaml
from jinja2 import Environment, FileSystemLoader
random.seed()

root_path = Path(__file__).parent.parent
file_loader = FileSystemLoader(root_path / '_includes' / 'email')
jinja_env = Environment(loader=file_loader)

# reads random highlights from books and outputs them to a file (to be emailed)
# TODO: we could do tags based
def main(args):
    # I'm going to go with only 1 highlight per book so if num-highlights > num-books you are
    # going to get shortened
    #print(f"args={args}")
    #print(f"root_path={root_path}")
    # _posts is where all the info is
    post_path = root_path / '_posts'
    all_books = sorted(post_path.glob("*.md"))
    #print(f"all_books={all_books}")
    selected_books = random.choices(all_books, k=args.num_highlights)
    #print(f"selected_books={selected_books}")
    highlights = []
    for book_path in selected_books:
        print(f"path={book_path}")
        with book_path.open() as f:
            # I'm not sure why but the _post/*.md is a yaml but with 2 documents (2nd document empty...)
            # maybe a jekyll related thing?
            info_gen = yaml.load_all(f, Loader=yaml.FullLoader)
            info = next(info_gen)
        #print(f"info={info}")

        highlights_path = book_path.parent.parent / '_data' / f"{info.get('book')}.yml"
        #print(f"highlights_path={highlights_path}")
        with highlights_path.open() as f:
            book_highlights = yaml.load(f, Loader=yaml.FullLoader)

        highlight = random.choice(book_highlights)
        #print(f"highlight={highlight}")
        highlights.append({
            'book_title': info.get('title'),
            'author': info.get('author'),
            'tags': info.get('tags'),
            'text': highlight.get('text'),
            'page': highlight.get('page'),


        })
        

    # TODO: template
    from pprint import pprint
    pprint(highlights)
    #print(f"highlights={highlights}")
    # TODO: output to output file, if no output file STDOUT
    template = jinja_env.get_template('highlights.html.j2')

    html = template.render(highlights=highlights)
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(html)
    else:
        print(html)
    

def parse_args():
    parser = argparse.ArgumentParser(description='read random highlights from posts/data')
    parser.add_argument('--num-highlights', type=int, default=5, help='how many highlights to store')
    parser.add_argument('--output', type=str, help='output file')
    args = parser.parse_args()
    return args
    

if __name__ == '__main__':
    args = parse_args()
    main(args)

