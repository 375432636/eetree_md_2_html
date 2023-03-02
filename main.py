import argparse
import base64
import markdown
from pathlib import Path
from lxml import etree

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
        src = img.attrib['src']
        with open(src, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        img.attrib['src'] = f"data:image/jpeg;base64,{encoded_image}"


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