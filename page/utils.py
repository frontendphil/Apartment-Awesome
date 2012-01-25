import sys
import datetime
from os.path import abspath, dirname

import Image, ImageFont, ImageDraw, ImageFilter

HEADLINE_SIZE = 48
DATE_SIZE = 36
TITLE_SIZE = 36
SUBTITLE_SIZE = 20

MODE = "RGBA"

BACKGROUND_COLOR = (255, 255, 255, 0)

def get_font_dir():
    return abspath(dirname(__file__)) + "/static/fonts/"

def get_headline_font():
    return get_font_dir() + "playbook.ttf"
    
def get_content_font():
    return get_font_dir() + "crayon.ttf"

def date_string(date):
    return date.strftime("%d.%m.%Y")

def draw_date(event, image):
    font = ImageFont.truetype(get_headline_font(), DATE_SIZE, encoding="unic")
    
    today = datetime.date.today()
    
    while not date_string(today) == date_string(event.date):
        today += datetime.timedelta(days=1)
    
    tmp_image = Image.new(MODE, image.size, BACKGROUND_COLOR)
    
    draw = ImageDraw.Draw(tmp_image)
    draw.text((400, 40), date_string(today), font=font)
    
    tmp_image = tmp_image.rotate(-5, Image.BICUBIC)
    
    image.paste(tmp_image, (0,20), tmp_image)

def draw_headline(event, image):
    font = ImageFont.truetype(get_headline_font(), HEADLINE_SIZE, encoding="unic")
    
    tmp_image = Image.new(MODE, image.size, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(tmp_image)
    draw.text((80, 60), event.headline.upper(), font=font)
    
    tmp_image = tmp_image.rotate(9, Image.BICUBIC)
    
    image.paste(tmp_image, (0, 20), tmp_image)
    
    draw_date(event, image)

def draw_text(event, image):
    draw_headline(event, image)
    
    lines = event.content.split("\n")
    
    x, y = (0, 100)
    
    for i in range(len(lines)):
        line = lines[i].upper()
        
        size = TITLE_SIZE if i % 2 == 0 else SUBTITLE_SIZE
        font = ImageFont.truetype(get_content_font(), size, encoding="unic")

        tmp_image = Image.new("RGBA", image.size, BACKGROUND_COLOR)
        draw = ImageDraw.Draw(tmp_image)
        draw.text((100, 60), line, font=font)

        tmp_image = tmp_image.rotate(9, Image.BICUBIC)

        image.paste(tmp_image, (x,y), tmp_image)
        
        y += 30 if i % 2 == 0 else 50 
        x += 7

def create_blackboard(event):
    path = dirname(abspath(__file__))
    image = Image.open(path + "/static/images/blackboard.png")
    
    draw_text(event, image)
    
    image.save(path + "/static/images/events/" + date_string(event.date) + ".png", "PNG")
    