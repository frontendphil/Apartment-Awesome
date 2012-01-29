import datetime

from hashlib import md5

from django.db import models

from PIL import Image, ImageFont, ImageDraw, ImageFilter

from apartmentawesome.settings import DEBUG, PROJECT_PATH, STATIC_ROOT
from apartmentawesome.page.utils import create_blackboard

if DEBUG:
    STATIC_ROOT = PROJECT_PATH + "/page/static"

MODE = "RGBA"
BACKGROUND_COLOR = (255, 255, 255, 0)

class Event(models.Model):
    HEADLINE_SIZE = 48
    DATE_SIZE = 36
    
    date = models.DateTimeField()
    headline = models.CharField(max_length=20)
    
    actvities = models.ManyToManyField("Activity")
    
    def __unicode__(self):
        return self.headline + " on " + self.date.strftime("%d.%m.%Y")
        
    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        
        self.create_blackboard()

    def create_blackboard(self):
        image = Image.open(STATIC_ROOT + "/images/blackboard.png")

        self.draw_text(image)

        image.save(STATIC_ROOT + "/images/events/" + self.date_string() + ".png", "PNG")
        
    def paste_rotated(self, angle, position, text, image):
        text = text.rotate(angle, Image.BICUBIC, expand=1)
        
        image.paste(text, position, text)
        
    def get_font(self, name, size):
        return ImageFont.truetype(name, size, encoding="unic")

    def create_text(self, text, font, image):
        text_image = Image.new(MODE, image.size, BACKGROUND_COLOR)

        draw = ImageDraw.Draw(text_image)
        draw.text((0,0), text, font=font)

        return text_image

    def draw_text(self, image):
        self.draw_headline(image)

        x, y = (70, 100)

        for activity in self.actvities.all():            
            self.paste_rotated(9, (x,y), activity.get_image(image.size), image)
            
            y += 80 
            x += 10
    
    def draw_headline(self, image):
        font = self.get_font(self.get_headline_font(), self.HEADLINE_SIZE)
        tmp_image = self.create_text(self.headline.upper(), font, image)
        
        self.paste_rotated(9, (60,20), tmp_image, image)
        self.draw_date(image)

    def draw_date(self, image):
        font = self.get_font(self.get_headline_font(), self.DATE_SIZE)
        today = datetime.date.today()

        while not self.date_string(today) == self.date_string():
            today += datetime.timedelta(days=1)

        tmp_image = self.create_text(self.date_string(today), font, image)

        self.paste_rotated(-5, (370,70), tmp_image, image)
        
    def get_font_dir(self):
        return STATIC_ROOT + "/fonts"

    def get_headline_font(self):
        return self.get_font_dir() + "/playbook.ttf"

    def date_string(self, date=None):
        if not date:
            date = self.date
        
        return date.strftime("%d.%m.%Y")
        
class Activity(models.Model):
    TITLE_SIZE = 36
    SUBTITLE_SIZE = 20
    
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.title + " at " + " and ".join([str(event) for event in self.event_set.all()])
        
    def save(self, *args, **kwargs):
        super(Activity, self).save(*args, **kwargs)
        
        for event in self.event_set.all():
            event.create_blackboard()
     
    def get_font(self, size):
        return ImageFont.truetype(STATIC_ROOT + "/fonts/crayon.ttf", size, encoding="unic")
    
    def create_text(self, text, font, image):
        text_image = Image.new(MODE, image.size, BACKGROUND_COLOR)

        draw = ImageDraw.Draw(text_image)
        draw.text((0,0), text, font=font)

        return text_image
        
    def create_title(self, image):
        font = self.get_font(self.TITLE_SIZE)

        return  self.create_text(self.title, font, image)
        
    def create_description(self, image):
        font = self.get_font(self.SUBTITLE_SIZE)

        return self.create_text(self.description, font, image)
    
    def get_image(self, size):
        image = Image.new(MODE, size, BACKGROUND_COLOR)
        
        title = self.create_title(image)
        description = self.create_description(image)
        
        image.paste(title, (0,0), title)
        image.paste(description, (0,35), description)
        
        return image
        
class Friend(models.Model):
    
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    
    # TODO: email field?
    email = models.CharField(max_length=255)
    
    events = models.ManyToManyField(Event)
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def save(self, *args, **kwargs):
        self.password = md5(self.password).hexdigest()
        
        super(Friend, self).save(*args, **kwargs)
        
    @classmethod
    def login(cls, name, password):
        password = md5(password).hexdigest()
        
        user = cls.objects.filter(name=name, password=password)
        
        if user:
            return user[0]