import argparse

def create_parser():
    prog_name           = '''TODO: write'''
    prog_description    = '''TODO: write'''
    prog_epilog         = '''TODO: write'''
    
    parser = argparse.ArgumentParser(
        prog=prog_name,
        usage='%(prog)s [options]',
        description=prog_description,
        epilog=prog_epilog
    )
    
    parser.add_argument(
        "--rankby",
        type = "string",
        choices = ['popularity', 'random'],
        default = "popularity", 
    )
    
    parser.add_argument(
        "--rankcount", 
        type = "int",
        default = 10
    )