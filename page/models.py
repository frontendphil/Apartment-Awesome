from django.db import models

from apartmentawesome.page.utils import create_blackboard

class Event(models.Model):
    date = models.DateTimeField()
    headline = models.CharField(max_length=20)
    content = models.TextField()
    
    def __unicode__(self):
        return self.headline + " on " + self.date.strftime("%d.%m.%Y")
        
    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        
        create_blackboard(self)
