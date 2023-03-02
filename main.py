import markdown
from lxml import etree
from lxml.etree import tounicode
import base64
# import re

with open("./main.md", "r",encoding="utf8") as f:
    TEXT = f.read()
# print(TEXT)
# TEXT = TEXT.replace("```","```\n\r")
HTML = markdown.markdown(TEXT,extensions=['attr_list','fenced_code'])

tree = etree.HTML(HTML)
for i in tree.xpath('//pre'):
    i.attrib['class'] = 'language-c'
# tree.find('idinfo/timeperd/timeinfo/rngdates/enddate').text = '1/1/2011'
for i in tree.xpath("//img"):
    # print(i.attrib['src'])
    src = i.attrib['src']
    with open(src, "rb") as image_file:
        i.attrib['src'] = "data:image/jpeg;base64,"+ base64.b64encode(image_file.read()).decode()
for i in tree.xpath("//*[self::h1 or self::h2 or self::h3]"):
    i.append(etree.XML(f"""<span style="font-size: 24pt;"><strong>{i.text}</strong></span>""").xpath("//span")[0])
    i.text = ""
# HTML = tounicode(i,method="HTML",with_tail=False)
HTML = tounicode(tree,method="HTML",with_tail=False)
with open("./out.html","w",encoding="utf8") as f:
    f.write(HTML)
