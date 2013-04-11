from django.db import models
from django import forms
        
class RefGene(models.Model):
    id = models.IntegerField(primary_key=True)
    bin = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    chrom = models.CharField(max_length=255, blank=True)
    strand = models.CharField(max_length=1, blank=True)
    start = models.IntegerField(null=True, db_column='txStart', blank=True)
    end = models.IntegerField(null=True, db_column='txEnd', blank=True)
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
        
class CPGIslands(models.Model):
    id = models.IntegerField(primary_key=True)
    bin = models.IntegerField()
    chrom = models.CharField(max_length=255)
    start = models.IntegerField(db_column='chromStart')
    end = models.IntegerField(db_column='chromEnd')
    name = models.CharField(max_length=255)
    length = models.IntegerField()
    cpgnum = models.IntegerField(db_column='cpgNum')
    gcnum = models.IntegerField(db_column='gcNum')
    percpg = models.FloatField(db_column='perCpg')
    pergc = models.FloatField(db_column='perGc')
    obsexp = models.FloatField(db_column='obsExp')
    class Meta:
        db_table = u'cpgislandext'

class VistaEnhancers(models.Model):
    id = models.IntegerField(primary_key=True)
    bin = models.IntegerField()
    chrom = models.CharField(max_length=255)
    start = models.IntegerField(db_column='chromStart')
    end = models.IntegerField(db_column='chromEnd')
    name = models.CharField(max_length=255)
    score = models.IntegerField()
    class Meta:
        db_table = u'vistaenhancers'

class SNP1(models.Model):
    id = models.IntegerField(primary_key=True)
    chrom = models.CharField(max_length=255)
    rsno = models.CharField(max_length=45)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    def __unicode__(self):
        return self.rsno
    class Meta:
        db_table = u'dbsnp_chr1'
        
class SNP2(models.Model):
    id = models.IntegerField(primary_key=True)
    chrom = models.CharField(max_length=255)
    rsno = models.CharField(max_length=45)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    def __unicode__(self):
        return self.rsno
    class Meta:
        db_table = u'dbsnp_chr2'
    
class SNP3(models.Model):
    id = models.IntegerField(primary_key=True)
    chrom = models.CharField(max_length=255)
    rsno = models.CharField(max_length=45)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    def __unicode__(self):
        return self.rsno
    class Meta:
        db_table = u'dbsnp_chr3'
    
class GWASCatalog(models.Model):
    id = models.IntegerField(primary_key=True)
    dateadded = models.CharField(max_length=10, db_column='dateAdded', blank=True)
    pubmedid = models.IntegerField(null=True, db_column='pubmedID', blank=True)
    firstauthor = models.CharField(max_length=255, db_column='firstAuthor', blank=True)
    pubdate = models.CharField(max_length=10, blank=True)
    journal = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    study = models.CharField(max_length=255, blank=True)
    disease = models.CharField(max_length=255, blank=True)
    initsamplesize = models.CharField(max_length=255, db_column='initSampleSize', blank=True)
    replsamplesize = models.CharField(max_length=255, db_column='replSampleSize', blank=True)
    region = models.CharField(max_length=10, blank=True)
    chrom = models.CharField(max_length=2, blank=True)
    pos = models.IntegerField(null=True, blank=True)
    reportedgenes = models.CharField(max_length=255, db_column='reportedGenes', blank=True)
    mappedgene = models.CharField(max_length=255, db_column='mappedGene', blank=True)
    upstreamgeneid = models.IntegerField(null=True, db_column='upstreamGeneID', blank=True)
    downstreamgeneid = models.IntegerField(null=True, db_column='downstreamGeneID', blank=True)
    snpgeneids = models.CharField(max_length=255, db_column='snpGeneIDs', blank=True)
    upstreamgenedistance = models.FloatField(null=True, db_column='upstreamGeneDistance', blank=True)
    downstreamgenedistance = models.FloatField(null=True, db_column='downstreamGeneDistance', blank=True)
    riskallele = models.CharField(max_length=255, db_column='riskAllele', blank=True)
    snps = models.CharField(max_length=255, blank=True)
    merged = models.CharField(max_length=1, blank=True)
    snpidcurrent = models.IntegerField(null=True, db_column='snpIDCurrent', blank=True)
    context = models.CharField(max_length=255, blank=True)
    intergenic = models.IntegerField(null=True, blank=True)
    riskallelefrequency = models.CharField(max_length=255, db_column='riskAlleleFrequency', blank=True)
    pvalue = models.FloatField(null=True, db_column='pValue', blank=True)
    pvaluemlog = models.FloatField(null=True, db_column='pValuemlog', blank=True)
    pvaluetext = models.CharField(max_length=255, db_column='pValueText', blank=True)
    ororbeta = models.CharField(max_length=100, db_column='ORorbeta', blank=True)
    number_95ci = models.CharField(max_length=40, db_column=u'95CI', blank=True)
    platform = models.CharField(max_length=255, blank=True)
    cnv = models.CharField(max_length=1, blank=True)
    def __unicode__(self):
        return 'GWAS PubMed ' + self.pubmedid
    class Meta:
        db_table = u'gwascatalog'

# class GeneForm(forms.Form):
    # chrom = forms.CharField(required=False)
    # strand = forms.CharField(required=False)
    # startf = forms.IntegerField(required=False)
    # endf = forms.IntegerField(required=False)
    
class DBSForm(forms.Form):
    rsno = forms.CharField(required=False)
    name = forms.CharField(required=False)
    
class FileForm(forms.Form):
    batch = forms.FileField()
    