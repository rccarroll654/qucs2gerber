from qucs2gerber.qucs2gerber import Qucs2Gerber
import argparse
import os

if __name__ == "__main__":
    # Start
    g = Qucs2Gerber()

    # Parse command line inputs
    parser = argparse.ArgumentParser(description="Converts a QUCS microstrip schematic or netlist to a gerber file.")
    parser.add_argument("-s", default=None, help='QUCS schematic file (Required)')
    parser.add_argument("-i", default='netlist.txt', help='QUCS netlist file')
    parser.add_argument("-o", default='qucs_layout.gbr', help='Output gerber file')
    parser.add_argument("-u", default='mm', help='Units of gerber file {mm,in}')
    parser.add_argument("-d", default='5', help='Number of decimals in coordinates')
    parser.add_argument("-l", default='3', help='Number of leading integers in coordinates')
    parser.add_argument("-v", default='gerbv', help='Gerber file viewer')

    args = parser.parse_args()

    # Apply command line arguments
    if args.s:
        # generate netlist from schematic
        cmd = "qucs -n -i {} -o {}".format(args.s, args.i)
        g.fprint(cmd)
        fh_p = os.system(cmd)
        g.fprint(fh_p)
        g.ReadNetlist(args.i)
        g.OpenOutpuFile(args.o)
        g.SetUnits(args.u)
        g.SetDecimals(args.d, leading=args.l)

        # Convert
        g.fprint("Converting to gerber file...", force=True)
        g.GenerateHeader()
        g.ProcessNetlist()
        g.Finish()
        g.fprint("Finished!", force=True)
        
        # Run the gerber viewer program
        os.system("{} {} &".format(args.v, args.o))
    else:
        g.fprint("Error: -s (Schematic Name) option is required.", force=True)
    g.kill()

    
