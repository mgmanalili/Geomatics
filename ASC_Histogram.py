#Manalili, Michael Andrew
#2003-96643
#Machine Problem 1
# .ASC to .XYZ

from collections import Counter
import gdal

#Function that asks multiple user inputs including path to file locations and header file information
def main():
#This line opens the header (first 6 lines) of the ASC file
    ans1 = raw_input("Would you like to print the header of the ASC data? [Y/N]: ")
    if ans1 == 'Y':
        fn = raw_input("Enter the unquoted path of the ASC data: ")
        d = open(fn, 'r')
        def print_header():
            for i in range(6):
                line = d.next().split()
                print line    
        a = print_header()
        print a        
        d.close()
    else:
        print "Failed to open the file. Remove the quote please."  
    if ans1 == 'N':
        print "Goodbye!"
    else:
        pass
    
#This line returns the new xllcorner and yllcorner for the ASC file. The user must explicitly edit the raw file    
    ans2 = raw_input("Would you like to shift the lower left corner value of the pixel to center? [Y/N]: ")
    if ans2 == 'Y':
        def replace_header():
            xllcorner = float(raw_input("Enter the xllcorner from the ASC header:"))
            yllcorner = float(raw_input("Enter the yllcorner from the ASC header:"))
            dx = float(raw_input("Enter the dx from the ASC header:"))
            dy = float(raw_input("Enter the dy from the ASC header:"))
            newx = xllcorner - dx/2
            newy = yllcorner - dy/2
            return newx, newy
        new_corners = replace_header()
        print "Kindly please edit source ASC file with this new corners: \nxllcorner = %f\nyllcorners = %f" %new_corners
    else:
        print "Failed to open the file. Remove the quote please."  
    if ans2 == 'N':
        print "Goodbye!"
    else:
        pass
    
#This ask if user wants to convert the ASC to XYZ format
    ans3 = raw_input("Would you like to convert ASC to XYZ? [Y/N]:")
    if ans3 == 'Y':
        infile = raw_input("Enter the unquoted path of the ASC file you want to convert>")
        outfile = raw_input("Enter the unquoted path of the destination path and name with file extension as(.xyz)>")
        asc2xyz(infile,outfile)
        print "Successfully converted the file!"
    else:
        print "Failed to open/convert the given file"  
    if ans3 == 'N':
        print "Goodbye!"
    else:
        pass
    
#This line asks user if histigram will be computed and displayed
    ans4 = raw_input("Would you like to compute the histogram? [Y/N]: ")
    if ans4 == 'Y':       
        hist()
        print "Successfully created Histogram!"
    else:
        print "Failed to create histogram"
    if ans4 == 'N':
        print "Goodbye!"
    else:
        pass
    
#Defines the function for file conversion
def asc2xyz(infile,outfile):
    infile = gdal.Open(infile)
    if infile is None:
        print "Cannot open %s" %infile
        return
    else:
        print "Successfully opened the file!"
            
    xyz = gdal.GetDriverByName("xyz")
    if xyz is None:
        print "ERROR: driver not available"
    else:
        pass          
    options = []
    xyz.CreateCopy(outfile, infile, 0, options)
    return asc2xyz

#Defines the function for computing and displaying histogram of the Z value
def hist():
    x = []
    y = []
    z = []
    dic = []
    xyzfile = raw_input("Enter the path to the converted xyz file: ")
    d = open(xyzfile, 'r')
    for word in d.readlines():
        dic = word.split(' ')
        x.append(dic[0].strip())
        y.append(dic[1].strip())
        z.append(dic[2].strip())
    zfloat = map(float,z)
    zint = map(int,zfloat) 
    counts = Counter(zint)
    binsize = raw_input("Enter bin size (e.g. 500, 1000): ")
    for k,v in counts.items():
        print "%s %s|" % (k,(v/int(binsize)) * "#")
    return hist

if __name__== '__main__':
    main()
    
### ----- END OF PROGRAM ----- ####
