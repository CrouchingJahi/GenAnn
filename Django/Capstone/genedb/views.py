from django.template import RequestContext, loader
from django.core import serializers
from django.http import HttpResponse
from genedb.models import *
# import csv
import string

def index(request):
    # form = GeneForm(request.GET)
    # c = RequestContext(request, {'form': form})
    t = loader.get_template('front.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
    
def result(request):
    t = loader.get_template('results.html')
    
    # form = DBSForm(request.GET)
    # if form.is_valid():
        # rsnumber = form.cleaned_data['rsno']
        # genename = form.cleaned_data['name']
    # # using python script queries
    # chrgene = RefGene.objects.filter(name__exact=genename)
    # chrm = chrgene.latest('id').chrom
    # db = chrtosnp(chrm)
    # location = db.objects.filter(rsno__exact=rsnumber)
    
    batch = FileForm(request.POST, request.FILES)
    if batch.is_valid():
        rsnums = []
        genenames = []
        rsarray(request.FILES['batch'], rsnums, genenames)
    
    location = SNP1.objects.none()
    refg = RefGene.objects.none()
    mrna = MicroRNA.objects.none()
    lrna = LNCRNA.objects.none()
    irna = LincRNA.objects.none()
    cpgi = CPGIslands.objects.none()
    vsta = VistaEnhancers.objects.none()
    
    gpcons = request.POST.getlist('databases', False)
    inclds = request.POST.getlist('includes', False)
    elmnts = request.POST.getlist('regulatory', False)
    diseas = request.POST.getlist('disease', False)
    
    refsc = 'RefSeq' in gpcons
    cpgic = 'CPGIslands' in inclds
    enhac = 'Enhancers' in inclds
    mrnac = 'microRNA' in elmnts
    lrnac = 'lncRNA' in elmnts
    irnac = 'lincRNA' in elmnts
    dbsnc = 'Map' in diseas    
    
    x = 0
    while (x < len(rsnums)):
        chrgene = RefGene.objects.filter(name__exact=genenames[x])
        chrm = chrgene.latest('id').chrom
        db = chrtosnp(chrm)
        location = location | db.objects.filter(rsno__exact=rsnums[x])
        for result in location.iterator():
            chrom = result.chrom
            strand = result.strand
            min = str(result.start)
            max = str(result.end)
            
            if refsc == True:
                qrefg = sformfilter(RefGene.objects, chrom, strand, min, max)
                refg = refg | qrefg
            
            if mrnac == True:
                qmrna = sformfilter(MicroRNA.objects, chrom, strand, min, max)
                mrna = mrna | qmrna
            if lrnac == True:
                qlrna = sformfilter(LNCRNA.objects, chrom, strand, min, max)
                lrna = lrna | qlrna
            if irnac == True:
                qirna = sformfilter(LincRNA.objects, chrom, strand, min, max)
                irna = irna | qirna
            
            if cpgic == True:
                qcpgi = formfilter(CPGIslands.objects, chrom, min, max)
                cpgi = cpgi | qcpgi
            if enhac == True:
                qvsta = formfilter(VistaEnhancers.objects, chrom, min, max)
                vsta = vsta | qvsta
        
        if dbsnc == True:
            rexp = rsnums[x] + "$|" + rsnums[x] + ","
            gwas = GWASCatalog.objects.filter(snps__regex=rexp)
        x = x + 1
    
    c = RequestContext(request, {
        "snps": location,
        "refgene": refg,
        "microrna": mrna,
        "lncrna": lrna,
        "lincrna": irna,
        "cpgislands": cpgi,
        "vistaenhancers": vsta,
        "gwascatalog": gwas
    })
    return HttpResponse(t.render(c))

def formfilter(set, chromosome, min, max):
    ret = set.filter(chrom__exact=chromosome)
    ret = ret.filter(start__lte=min)
    ret = ret.filter(end__gte=max)
    return ret
    
def sformfilter(set, chromosome, strandside, min, max):
    ret = formfilter(set, chromosome, min, max)
    ret = ret.filter(strand__exact=strandside)
    return ret
  
# Throws a list index out of range error if the input file is not correctly formatted with 2 columns per line and instead only has 1.
def rsarray(file, rs, gene):
    while 1:
        line = file.readline()
        if not line: break;
        parts = string.split(line,'\t')
        rs.append(string.strip(parts[0]))
        gene.append(string.strip(parts[1]))

def chrtosnp(chr):
    snp = "SNP" + chr[3:]
    return eval(snp)