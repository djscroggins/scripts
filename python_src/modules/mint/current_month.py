import calendar
import datetime
import subprocess


def get_current_year() -> int:
    return datetime.datetime.now().year


def get_first_day(year: int, month: int) -> str:
    return datetime.date(year, month, 1).strftime('%m-%d-%Y')


def get_last_day(year: int, month: int):
    _, num_days = calendar.monthrange(year, month)
    return datetime.date(year, month, num_days).strftime('%m-%d-%Y')


def open_mint(start_date: str, end_date: str) -> None:
    mint_base_url = 'https://mint.intuit.com/transaction.event'
    mint_open_url = f'{mint_base_url}?startDate={start_date}&endDate={end_date}'
    subprocess.run(['open', mint_open_url])


def main() -> None:
    prompt = 'Enter current month as integer: '
    accepted_range = set([i for i in range(1, 13)])
    while True:
        try:
            response = input(prompt)
            selected_month = int(response)
            if selected_month not in accepted_range:
                raise ValueError
            current_year = get_current_year()
            first_day = get_first_day(current_year, selected_month)
            last_day = get_last_day(current_year, selected_month)
            open_mint(first_day, last_day)
            break
        except ValueError:
            prompt = 'Make sure to enter month as valid integer between 1 and 12: '


if __name__ == '__main__':
    main()
