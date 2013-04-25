from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from genedb.models import *
import string, csv

def index(request):
    t = loader.get_template('front.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

# When the query is submitted from the front page, this function reads the file and puts the data into the session. It then redirects to displaying the results
def submit(request):
    rsnums = []
    genenames = []
    batch = FileForm(request.POST, request.FILES)
    
    if batch.is_valid():
        # Expected file format is with the rsgarray function
        rsgarray(request.FILES['batch'], rsnums, genenames)
    # form = DBSForm(request.POST)
    # if form.is_valid():
        # rsnumber = form.cleaned_data['rsno']
        # genename = form.cleaned_data['name']
    # rsnums.append(rsnumber)
    # genenames.append(genename)
    
    # Store the checkbox states in the session
    # gpcons = request.POST.getlist('databases', [])
    inclds = request.POST.getlist('includes', [])
    elmnts = request.POST.getlist('regulatory', [])
    diseas = request.POST.getlist('disease', [])
    request.session['cpgic'] = 'CPGIslands' in inclds
    request.session['enhac'] = 'Enhancers' in inclds
    request.session['mrnac'] = 'microRNA' in elmnts
    request.session['lrnac'] = 'lncRNA' in elmnts
    request.session['irnac'] = 'lincRNA' in elmnts
    request.session['dbsnc'] = 'Map' in diseas
    
    # Perform the query and pass the results to the results page
    location = SNP1.objects.none()
    refg = RefGene.objects.none()
    mrna = MicroRNA.objects.none()
    lrna = LNCRNA.objects.none()
    irna = LincRNA.objects.none()
    cpgi = CPGIslands.objects.none()
    vsta = VistaEnhancers.objects.none()
    gwas = GWASCatalog.objects.none()
    
    # Gather locations from the list of snps
    x = 0
    while (x < len(rsnums)):
        if (len(genenames[x]) == 0):
            location = location | findsnp(rsnums[x])
        else:
            chrgene = RefGene.objects.filter(name__exact=genenames[x])
            chrm = chrgene.latest('id').chrom
            db = chrtosnp(chrm)
            location = location | db.objects.filter(rsno__exact=rsnums[x])
        rexp = rsnums[x] + "$|" + rsnums[x] + ","
        gwas = GWASCatalog.objects.filter(snps__regex=rexp)
        x = x + 1
    
    # Use the found locations to query the tables
    for result in location.iterator():
        chrom = result.chrom
        strand = result.strand
        min = str(result.start)
        max = str(result.end)
        
        qrefg = sformfilter(RefGene.objects, chrom, strand, min, max)
        refg = refg | qrefg
        
        qmrna = sformfilter(MicroRNA.objects, chrom, strand, min, max)
        mrna = mrna | qmrna
        qlrna = sformfilter(LNCRNA.objects, chrom, strand, min, max)
        lrna = lrna | qlrna
        qirna = sformfilter(LincRNA.objects, chrom, strand, min, max)
        irna = irna | qirna
        
        qcpgi = formfilter(CPGIslands.objects, chrom, min, max)
        cpgi = cpgi | qcpgi
        qvsta = formfilter(VistaEnhancers.objects, chrom, min, max)
        vsta = vsta | qvsta
        
    request.session['location'] = location
    request.session['refg'] = refg
    request.session['mrna'] = mrna
    request.session['lrna'] = lrna
    request.session['irna'] = irna
    request.session['cpgi'] = cpgi
    request.session['vsta'] = vsta
    request.session['gwas'] = gwas
    
    return HttpResponseRedirect('/result/')

# Retrieves the query results from the session and displays them
def result(request):
    t = loader.get_template('results.html')
    
    location = request.session['location']
    refg = request.session['refg']
    mrna = request.session['mrna']
    lrna = request.session['lrna']
    irna = request.session['irna']
    cpgi = request.session['cpgi']
    vsta = request.session['vsta']
    gwas = request.session['gwas']
    cpgic = request.session['cpgic']
    enhac = request.session['enhac']
    mrnac = request.session['mrnac']
    lrnac = request.session['lrnac']
    irnac = request.session['irnac']
    dbsnc = request.session['dbsnc']
    
    c = RequestContext(request, {
        "snps": location,
        "refgene": refg,
        "microrna": mrna,
        "lncrna": lrna,
        "lincrna": irna,
        "cpgislands": cpgi,
        "vistaenhancers": vsta,
        "gwascatalog": gwas,
        "c_microrna": mrnac,
        "c_lncrna": lrnac,
        "c_lincrna": irnac,
        "c_cpgislands": cpgic,
        "c_vistaenhancers": enhac,
        "c_gwascatalog": dbsnc,
    })
    return HttpResponse(t.render(c))

# Given the name of a set of results, generates a CSV file
def file(request, setname):
    file = HttpResponse(mimetype='text/csv')
    file['Content-Disposition'] = 'attachment; filename="results-' + setname + '.csv"'
    writer = csv.writer(file)
    
    if setname == "snps":
        set = request.session['location']
        writer.writerow(SNP.csvheader())
    else:
        set = request.session[setname]
        if setname == "refg":
            writer.writerow(RefGene.csvheader())
        elif setname == "mrna":
            writer.writerow(MicroRNA.csvheader())
        elif setname == "lrna":
            writer.writerow(LNCRNA.csvheader())
        elif setname == "irna":
            writer.writerow(LincRNA.csvheader())
        elif setname == "cpgi":
            writer.writerow(CPGIslands.csvheader())
        elif setname == "vsta":
            writer.writerow(VistaEnhancers.csvheader())
        elif setname == "gwas":
            writer.writerow(GWASCatalog.csvheader())
    for r in set:
        writer.writerow(r.csv())
    return file

# Filters the set based on chromosome location
def formfilter(set, chromosome, min, max):
    ret = set.filter(chrom__exact=chromosome)
    ret = ret.filter(start__lte=min)
    ret = ret.filter(end__gte=max)
    return ret

# Filters the set based on chromosome location, and the strand
def sformfilter(set, chromosome, strandside, min, max):
    ret = formfilter(set, chromosome, min, max)
    ret = ret.filter(strand__exact=strandside)
    return ret

# Given a file, populates the arrays rs and gene with the parsed rsnumbers and gene names.
# The expected file format is an rsnumber, tab for separation, and then a gene name that corresponds to that rsnumber.
#  The gene name assists in finding out which chomosome that rsnumber is on and has the potential to greatly increase query speed,
#   since the tables of DBSNP are separated by chromosome.
#  However, a row is allowed to have only one column, and no gene name.
def rsgarray(file, rs, gene):
    # If there is only one column, the first column is stored as the rsnumber and the gene name column for that row is empty.
    while 1:
        line = file.readline()
        if not line: break;
        parts = string.split(line,'\t')
        rs.append(string.strip(parts[0]))
        if (len(parts) > 1):
            gene.append(string.strip(parts[1]))
        else:
            gene.append("")

# Given an rs number, searches all chromosomes in DBSNP until it finds the matching entry.
def findsnp(rsno):
    x = 1
    # Only chromosomes 1-3 are available, so this stops at 3.
    while (x <= 3):
        db = eval("SNP" + str(x))
        cur = db.objects.filter(rsno__exact=rsno)
        if len(cur) > 0:
            return cur
        x = x + 1
    return SNP1.objects.none()

# Given the string "chr1", returns the model object SNP1, and so on.
def chrtosnp(chr):
    snp = "SNP" + chr[3:]
    return eval(snp)
