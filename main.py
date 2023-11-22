import argparse
import src.urast as urast
import src.qmap as qmap


# al, src_dir, out_dir
def main(args):
    if args.al == 'QmapID':
        qmap.qmap(args.src, args.dst)
    if args.al == 'uRAST':
        qmap.qmap(args.src, args.dst)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example script for command line argument processing")

    # Add '-a' argument
    parser.add_argument("-a", "--al", required=True, help="Specify the QmapID.")

    # Add '-f' argument
    parser.add_argument("-f", "--src", required=True, help="Specify the source file path.")

    # Add '-o' argument
    parser.add_argument("-o", "--dst", required=True, help="Specify the output directory.")

    args = parser.parse_args()

    main(args)