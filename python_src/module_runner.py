import argparse

from modules.mint.current_month import main as run_mint_main
# from routines.clean_downloads import main as run_clean_downloads


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Program for running Python helper scripts')
    parser.add_argument('--mint', action='store_true', help='Run program for filtering Mint transactions by month')
    parser.add_argument('--clean-downloads', '-cd', action='store_true', help='Run routine to clean Downloads directory')
    return parser


if __name__ == '__main__':
    main_parser = create_parser()
    args = main_parser.parse_args()
    if args.mint:
        print('Running mint ...')
        run_mint_main()
    if args.clean_downloads:
        print('cleaning downloads')
        # run_clean_downloads()
    else:
        print('No arguments entered. Exiting ...')
