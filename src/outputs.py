import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, FILE_OUTPUT, PRETTY_OUTPUT, RESULTS_DIRNAME

SAVE_SUCCESS_MSG = 'Файл с результатами был сохранён: {file_path}'


def default_output(results, cli_args):
    """Выводит результаты построчно в стандартный поток вывода."""
    for row in results:
        print(*row)


def pretty_output(results, cli_args):
    """Выводит результаты в виде форматированной таблицы PrettyTable."""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    """Сохраняет результаты в CSV-файл в директорию results/."""
    results_dir = BASE_DIR / RESULTS_DIRNAME
    results_dir.mkdir(exist_ok=True)
    now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{cli_args.mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        csv.writer(f, dialect=csv.unix_dialect).writerows(results)
    logging.info(SAVE_SUCCESS_MSG.format(file_path=file_path))


OUTPUT_FUNCTIONS = {
    PRETTY_OUTPUT: pretty_output,
    FILE_OUTPUT: file_output,
    None: default_output,
}


def control_output(results, cli_args):
    """Направляет результаты в нужный канал вывода по значению --output."""
    OUTPUT_FUNCTIONS[cli_args.output](results, cli_args)
