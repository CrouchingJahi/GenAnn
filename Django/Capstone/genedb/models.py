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
    @staticmethod
    def csvheader():
        return ["bin", "name", "chrom", "strand", "txStart", "txEnd", "cdsStart", "cdsEnd", "exonCount", "exonStarts", "exonEnds", "score", "name2", "cdsStartStat", "cdsEndStat", "exonFrames"]
    def csv(self):
        return [str(self.bin), self.name, self.chrom, self.strand, str(self.start), str(self.end), str(self.cdsstart), str(self.cdsend), str(self.exoncount), self.exonstarts, self.exonends, str(self.score), self.name2, self.cdsstartstat, self.cdsendstat, self.exonframes]
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = u'refgene'
        
class RNA(models.Model):
    id = models.IntegerField(primary_key=True)
    chrom = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    @staticmethod
    def csvheader():
        return ["chrom", "type", "start", "end", "strand"]
    def csv(self):
        return [self.chrom, self.type, str(self.start), str(self.end), self.strand]
    class Meta:
        abstract = True

class LincRNA(RNA):
    source = models.CharField(max_length=45, blank=True)
    @staticmethod
    def csvheader():
        return ["chrom", "type", "source", "start", "end", "strand"]
    def csv(self):
        return [self.chrom, self.type, self.source, str(self.start), str(self.end), self.strand]
    class Meta:
        db_table = u'lincrna'

class LNCRNA(RNA):
    class Meta:
        db_table = u'lncipedia'

class MicroRNA(RNA):
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
    @staticmethod
    def csvheader():
        return ["bin", "chrom", "chromStart", "chromEnd", "name", "length", "cpgNum", "gcNum", "perCpg", "perGc", "obsExp"]
    def csv(self):
        return [str(self.bin), self.chrom, str(self.start), str(self.end), self.name, str(self.length), str(self.cpgNum), str(self.gcNum), str(self.perCpg), str(self.perGc), str(self.obsExp)]
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
    @staticmethod
    def csvheader():
        return ["bin", "chrom", "chromStart", "chromEnd", "name", "score"]
    def csv(self):
        return [str(self.bin), self.chrom, str(self.start), str(self.end), self.name, str(self.score)]
    class Meta:
        db_table = u'vistaenhancers'
        
class SNP(models.Model):
    id = models.IntegerField(primary_key=True)
    chrom = models.CharField(max_length=255)
    rsno = models.CharField(max_length=45)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    @staticmethod
    def csvheader():
        return ["rsno", "chrom", "strand", "start", "end"]
    def csv(self):
        return [self.rsno, self.chrom, self.strand, str(self.start), str(self.end)]
    def __unicode__(self):
        return self.rsno
    class Meta:
        abstract = True
        
class SNP1(SNP):
    class Meta:
        db_table = u'dbsnp_chr1'
        
class SNP2(SNP):
    class Meta:
        db_table = u'dbsnp_chr2'
    
class SNP3(SNP):
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
    @staticmethod
    def csvheader():
        return ["dateAdded", "pubmedID", "firstAuthor", "pubdate", "journal", "link", "study", "disease", "initSampleSize", "replSampleSize", "region", "chrom", "pos", "reportedGenes", "mappedGene", "upstreamGeneID", "downstreamGeneID", "snpGeneIDs", "upstreamGeneDistance", "downstreamGeneDistance", "riskAllele", "snps", "merged", "snpIDCurrent", "context", "intergenic", "riskAlleleFrequency", "pValue", "pValuemlog", "pValueText", "ORorbeta", "95CI", "platform", "cnv"]
    def csv(self):
        return [self.dateadded, str(self.pubmedid), self.firstauthor, self.pubdate, self.journal, self.link, self.study, self.disease, self.initsamplesize, self.replsamplesize, self.region, self.chrom, str(self.pos), self.reportedgenes, self.mappedgene, str(self.upstreamgeneid), str(self.downstreamgeneid), self.snpgeneids, str(self.upstreamgenedistance), str(self.downstreamgenedistance), self.riskallele, self.snps, self.merged, str(self.snpidcurrent), self.context, str(self.intergenic), self.riskallelefrequency, str(self.pvalue), str(self.pvaluemlog), self.pvaluetext, self.ororbeta, self.number_95ci, self.platform, self.cnv]
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
    batch = forms.FileField(required=False)
    