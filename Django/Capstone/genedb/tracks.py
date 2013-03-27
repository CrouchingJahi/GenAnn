class Track:
    __name = ''
    __col_want = ''
    
    __col_chr = ''
    __col_strand = ''
    __col_start = ''
    __col_end = ''
    
    def __init__(self, name, want, chr, strand, start, end):
        self.__name = name
        self.__want = want
        self.__col_chr = chr
        self.__col_strand = strand
        self.__col_start = start
        self.__col_end = end
    
    def __makeSinglePositionCheck(self, chr, strand, pos):
        chr_num = self.__col_chr + ' = "' + chr + '"'
        chr_strand = self.__col_strand + ' = "' + strand + '"'
        chr_start = pos + ' >= ' + self.__col_start
        chr_end = pos + ' <= ' + self.__col_end
        return '(' + chr_num + ' AND ' + chr_strand + ' AND '  + chr_start + ' AND ' + chr_end + ')'
    
    def makePositionCheck(self, args):
        result = ''
        i = 3
        while len(args) >= i:
            if (result):
                result = result + ' OR '
            result = result + self.__makeSinglePositionCheck(args[i-3],args[i-2],args[i-1])
            i = i + 3
        
        return result
    
    def __makeSingleRangeCheck(self, chr, strand, start, end):
        # Pre-work for making the query
        chr_num = self.__col_chr + ' = "' + chr + '"'
        chr_strand = self.__col_strand + ' = "' + strand + '"'
        # Check for overlap in ranges
        inside_area = '(' + start + ' >= ' + self.__col_start + ' AND ' + start + ' <= ' + self.__col_end
        inside_area = inside_area + ') OR (' + self.__col_start + ' >= ' + start + ' AND ' + self.__col_start + ' <= ' + end + ')'
        return '((' + inside_area + ') AND ' + chr_strand + ' AND ' + chr_num + ')'
    
    def makeRangeCheck(self, args):
        result = ''
        i = 4
        while len(args) >= i:
            if (result):
                result = result + ' OR '
            result = result + self.__makeSingleRangeCheck(args[i-4],args[i-3],args[i-2],args[i-1])
            i = i + 4
        
        return result
        
    def orWheres(self, args):
        result = ''
        i = 1
        while i <= len(args):
            if (result):
                result = result + ' OR '
            result = result + args[i-1]
            i = i + 1
        return result

    def makeQuery(self, sql_check):
        return 'SELECT ' + self.__want + ' FROM ' + self.__name + ' WHERE ' + sql_check + ';'