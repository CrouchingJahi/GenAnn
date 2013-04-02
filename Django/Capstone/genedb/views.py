from django.template import RequestContext, loader
from django.core import serializers
from django.http import HttpResponse
from genedb.models import *
# import csv

def index(request):
    # form = GeneForm(request.GET)
    # c = RequestContext(request, {'form': form})
    t = loader.get_template('front.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
    
def result(request):
    t = loader.get_template('results.html')
    form = DBSForm(request.GET)
    if form.is_valid():
        rsnumber = form.cleaned_data['rsno']
        genename = form.cleaned_data['name']
    # using python script queries
    chrgene = RefGene.objects.filter(name__exact=genename)
    chrm = chrgene.latest('id').chrom
    db = chrtosnp(chrm)
    location = db.objects.filter(rsno__exact=rsnumber)
    
    #import pdb; pdb.set_trace()
    
    # for result in location.iterator():
    result = location.latest('id')
    chrom = result.chrom
    strand = result.strand
    min = str(result.start)
    max = str(result.end)
    
    refg = RefGene.objects.none()
    mrna = MicroRNA.objects.none()
    lrna = LNCRNA.objects.none()
    irna = LincRNA.objects.none()
    cpgi = CPGIslands.objects.none()
    vsta = VistaEnhancers.objects.none()

    for result in location.iterator():
        chrom = result.chrom
        strand = result.strand
        min = str(result.start)
        max = str(result.end)
        
        qrefg = formfilter(RefGene.objects, chrom, strand, min, max)
        refg = refg | qrefg
        
        qmrna = formfilter(MicroRNA.objects, chrom, strand, min, max)
        mrna = mrna | qmrna
        qlrna = formfilter(LNCRNA.objects, chrom, strand, min, max)
        lrna = lrna | qlrna
        qirna = formfilter(LincRNA.objects, chrom, strand, min, max)
        irna = irna | qirna
        
        qcpgi = cformfilter(CPGIslands.objects, chrom, min, max)
        cpgi = cpgi | qcpgi
        qvsta = cformfilter(VistaEnhancers.objects, chrom, min, max)
        vsta = vsta | qvsta
    
    c = RequestContext(request, {
        "snps": location,
        "refgene": refg,
        "microrna": mrna,
        "lncrna": lrna,
        "lincrna": irna,
        "cpgislands": cpgi,
        "vistaenhancers": vsta
    })
    return HttpResponse(t.render(c))
    
def rsnumber(*args):
    return 0

def formfilter(set, chromosome, strandside, min, max):
    ret = set.filter(chrom__exact=chromosome)
    ret = ret.filter(start__lte=min)
    ret = ret.filter(end__gte=max)
    ret = ret.filter(strand__exact=strandside)
    return ret
    
def cformfilter(set, chromosome, min, max):
    ret = set.filter(chrom__exact=chromosome)
    ret = ret.filter(start__lte=min)
    ret = ret.filter(end__gte=max)
    return ret    
    
def chrtosnp(chr):
    snp = "SNP" + chr[3:]
    return eval(snp)