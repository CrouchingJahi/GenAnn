from django.template import RequestContext, loader
from django.core import serializers
from django.http import HttpResponse
from genedb.models import RefGene, LincRNA, LNCRNA, MicroRNA#, GeneForm
from genedb.models import SNP2, DBSForm
from genedb import tracks
import csv

def index(request):
    # t = loader.get_template('test.html')
    # form = GeneForm(request.GET)
    # c = RequestContext(request, {'form': form})
    t = loader.get_template('front_dj.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
    
def result(request):
    # t = loader.get_template('result2.html')
    t = loader.get_template('resultst_dj.html')
    form = DBSForm(request.GET)
    if form.is_valid():
        rsnumber = form.cleaned_data['rsno']
        genename = form.cleaned_data['name']
    
    # using python script queries
    rsnumber = str(rsnumber)
    chrgene = RefGene.objects.filter(name__exact=genename)
    chr = chrgene.latest('id').chrom
    db = chrtosnp(chr)
    location = db.objects.filter(rsno__exact=rsnumber) # Should always return 1 item
    result = location.latest('id')
    chrom = result.chrom
    strand = result.strand
    min = str(result.start)
    max = str(result.end)
    
    table = tracks.Track('refgene', 'id, name, chrom, strand, txStart, txEnd', 'chrom', 'strand', 'txStart', 'txEnd')
    where = []
    where.append(table.makeRangeCheck([chrom, strand, min, max]))
    qrefg = table.makeQuery(table.orWheres(where))
    table = tracks.Track('microrna', 'id, chrom, strand, start, end', 'chrom', 'strand', 'start', 'end')
    where = []
    where.append(table.makeRangeCheck([chrom, strand, min, max]))
    qmrna = table.makeQuery(table.orWheres(where))
    table = tracks.Track('lncipedia', 'id, chrom, strand, start, end', 'chrom', 'strand', 'start', 'end')
    where = []
    where.append(table.makeRangeCheck([chrom, strand, min, max]))
    qlrna = table.makeQuery(table.orWheres(where))
    table = tracks.Track('lincrna', 'id, chrom, strand, start, end', 'chrom', 'strand', 'start', 'end')
    where = []
    where.append(table.makeRangeCheck([chrom, strand, min, max]))
    qirna = table.makeQuery(table.orWheres(where))
    refg = RefGene.objects.raw(qrefg)
    refgcount = len(list(refg))
    mrna = MicroRNA.objects.raw(qmrna)
    mrnacount = len(list(mrna))
    lrna = LNCRNA.objects.raw(qlrna)
    lrnacount = len(list(lrna))
    irna = LincRNA.objects.raw(qirna)
    irnacount = len(list(irna))

    c = RequestContext(request, {
        "snps": location,
        "refgene": refg,
        "microrna": mrna,
        "lncrna": lrna,
        "lincrna": irna,
        "refgenecount": refgcount,
        "micrornacount": mrnacount,
        "lncrnacount": lrnacount,
        "lincrnacount": irnacount
    })
    return HttpResponse(t.render(c))
    
def rsnumber(*args):
    return 0;

def formfilter(set, min, max, chromosome, strandside):
    if min == None and max != None:
        set = set.filter(txend__lte=max)
    if min != None and max == None:
        set = set.filter(txstart__gte=min)
    if min != None and max != None:
        set = set.filter(txstart__range=(min, max))
        set = set.filter(txend__range=(min, max))
    if chromosome != "":
        set = set.filter(chrom__exact=chromosome)
    if strandside != "":
        set = set.filter(strand__exact=strandside)
    return set
    
def rformfilter(set, min, max, chromosome, strandside):
    if min == None and max != None:
        set = set.filter(end__lte=max)
    if min != None and max == None:
        set = set.filter(start__gte=min)
    if min != None and max != None:
        set = set.filter(start__range=(min, max))
        set = set.filter(end__range=(min, max))
    if chromosome != "":
        set = set.filter(chrom__exact=chromosome)
    if strandside != "":
        set = set.filter(strand__exact=strandside)
    return set
    
def chrtosnp(chr):
    snp = "SNP" + chr[3:]
    return eval(snp)