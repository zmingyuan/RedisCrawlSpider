from django.db import models

# Create your models here.
#工作信息类
class Jobs(models.Model):
    url = models.CharField(max_length=255)
    enterprise_name = models.CharField(max_length=50)
    pname = models.CharField(max_length=255)
    smoney = models.FloatField()
    emoney = models.FloatField()
    plocation = models.CharField(max_length=30)
    parea = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    position_education = models.CharField(max_length=10)
    tags = models.CharField(max_length=255)
    date_pub = models.CharField(max_length=10)
    advantage = models.TextField(max_length=255)
    jobdesc = models.TextField(max_length=255)
    ptype = models.CharField(max_length=10)
    crawl_time = models.IntegerField()
    pnumber = models.CharField(max_length=255)
    company_profile = models.TextField()

    def dicts(self):
        return {'id':self.id,'url':self.url,'enterprise_name':self.enterprise_name,'pname':self.pname,'smoney':self.smoney,'emoney':self.emoney, 'plocation':self.plocation,'parea':self.parea,'experience':self.experience,'position_education':self.position_education,'tags':self.tags,'date_pub':self.date_pub,'advantage':self.advantage,'jobdesc':self.jobdesc,'ptype':self.ptype,'crawl_time':self.crawl_time,'pnumber':self.pnumber,'company_profile':self.company_profile}

    class Meta:
        db_table = "job"