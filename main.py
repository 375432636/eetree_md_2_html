import argparse
import base64
import os

import markdown
from pathlib import Path
from lxml import etree
from PIL import Image, ImageOps
import datetime


NOW = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_")


class Compress_img:

    def __init__(self, img_path):
        self.img_full_path = os.path.abspath(img_path)
        self.img_path = os.path.split(self.img_full_path)[0]
        self.img_name = os.path.split(self.img_full_path)[-1]
        self.ext = self.img_name.lower().split(".")[-1]

    def compress_img_PIL(self, compress_rate=0.5, show=False) -> str:
        if "svg" == self.ext:
            return self.img_full_path
        img = Image.open(self.img_full_path)
        img = ImageOps.exif_transpose(img)
        h, w = img.size
        max_width = int(720)
        if w > max_width:
            new_high = int(max_width/w*h)
            new_width = int(max_width)
            img_resize = img.resize(( new_high, new_width ))
            new_path = os.path.join(self.img_path, NOW + self.img_name)
            img_resize.save(str(new_path))
        else:
            new_path = self.img_full_path
        return new_path

def parse_args():
    parser = argparse.ArgumentParser(description="Convert markdown file to HTML")
    parser.add_argument("input_file", help="input markdown file")
    parser.add_argument("output_file", help="output HTML file")
    return parser.parse_args()



def read_markdown_file(file_path: Path) -> str:
    with open(file_path,encoding="utf8") as f:
        return f.read()


def convert_markdown_to_html(markdown_text: str) -> str:
    extensions = ["attr_list", "fenced_code"]
    return markdown.markdown(markdown_text, extensions=extensions)


def add_code_block_class(html_tree: etree.Element) -> None:
    for pre in html_tree.xpath('//pre'):
        pre.attrib['class'] = 'language-c'


def encode_images_as_base64(html_tree: etree.Element) -> None:
    for img in html_tree.xpath("//img"):
        src = Compress_img(img.attrib['src']).compress_img_PIL()
        with open(src, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        ext = src.split('.')[-1]
        img.attrib['src'] = f"data:image/{ext};base64,{encoded_image}"


def add_heading_styles(html_tree: etree.Element) -> None:
    for heading in html_tree.xpath("//*[self::h1 or self::h2 or self::h3]"):
        span = etree.XML(f'<span style="font-size: 24pt;"><strong>{heading.text}</strong></span>')
        heading.text = ""
        heading.append(span)


if __name__ == "__main__":
    args = parse_args()
    input_file = Path(args.input_file)
    output_file = Path(args.output_file)

    markdown_text = read_markdown_file(input_file)
    html_text = convert_markdown_to_html(markdown_text)
    html_tree = etree.HTML(html_text)

    add_code_block_class(html_tree)
    encode_images_as_base64(html_tree)
    add_heading_styles(html_tree)
    html_output = etree.tostring(html_tree, method="html", with_tail=False, encoding="unicode")
    with open(output_file, "w",encoding="utf8") as f:
        f.write(html_output)