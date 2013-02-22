from django.db import models
from django import forms
 
# Create your models here.

# class Gene(models.Model):
    # name = models.CharField(max_length=40)
    # chrom = models.CharField(max_length=40)
    # strand = models.CharField(max_length=1)
    # txStart = models.IntegerField()
    # txEnd = models.IntegerField()
    
    # def __unicode__(self):
        # return self.name
        
class RefGene(models.Model):
    id = models.IntegerField(primary_key=True)
    bin = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    chrom = models.CharField(max_length=255, blank=True)
    strand = models.CharField(max_length=1, blank=True)
    txstart = models.IntegerField(null=True, db_column='txStart', blank=True)
    txend = models.IntegerField(null=True, db_column='txEnd', blank=True)
    cdsstart = models.IntegerField(null=True, db_column='cdsStart', blank=True)
    cdsend = models.IntegerField(null=True, db_column='cdsEnd', blank=True)
    exoncount = models.IntegerField(null=True, db_column='exonCount', blank=True)
    exonstarts = models.TextField(db_column='exonStarts', blank=True)
    exonends = models.TextField(db_column='exonEnds', blank=True)
    score = models.IntegerField(null=True, blank=True)
    name2 = models.CharField(max_length=255, blank=True)
    cdsstartstat = models.CharField(max_length=18, db_column='cdsStartStat', blank=True)
    cdsendstat = models.CharField(max_length=18, db_column='cdsEndStat', blank=True)
    exonframes = models.TextField(db_column='exonFrames', blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = u'refgene'

class LincRNA(models.Model):
    id = models.IntegerField(primary_key=True)
    chrom = models.CharField(max_length=255)
    source = models.CharField(max_length=45, blank=True)
    type = models.CharField(max_length=255)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    class Meta:
        db_table = u'lincrna'

class LNCRNA(models.Model):
    id = models.IntegerField(primary_key=True)
    chrom = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    class Meta:
        db_table = u'lncipedia'

class MicroRNA(models.Model):
    id = models.IntegerField(primary_key=True)
    chrom = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    class Meta:
        db_table = u'microrna'
    
class GeneForm(forms.Form):
    chrom = forms.CharField(required=False)
    strand = forms.CharField(required=False)
    startf = forms.IntegerField(required=False)
    endf = forms.IntegerField(required=False)
    