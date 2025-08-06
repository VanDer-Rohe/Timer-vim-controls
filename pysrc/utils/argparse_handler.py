import argparse


def parse_arguments():
    """Parse command line arguments for the timer application."""
    parser = argparse.ArgumentParser(description='Countdown Timer')
    parser.add_argument('--time', '-t', type=str, help='Timer duration (MM:SS or HH:MM:SS)')
    parser.add_argument('--hide', action='store_true', help='Start timer hidden')
    
    return parser.parse_args()
