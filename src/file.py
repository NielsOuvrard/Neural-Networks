import sys
from arguments import Arguments, handle_arguments, print_usage

def main(argv):
    args = Arguments()

    if handle_arguments(argv, args) == 84:
        return 84
    elif args.help:
        return 0

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
