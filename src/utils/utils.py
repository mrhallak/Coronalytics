from io import StringIO, TextIOBase
from csv import DictReader, QUOTE_ALL
from dateutil import parser
from datetime import datetime
from typing import Optional, Any, Iterator


# https://stackoverflow.com/a/12604375/2000875
class StringIteratorIO(TextIOBase):
    def __init__(self, iter: Iterator[str]):
        self._iter = iter
        self._buff = ''

    def readable(self) -> bool:
        return True

    def _read1(self, n: Optional[int] = None) -> str:
        while not self._buff:
            try:
                self._buff = next(self._iter)
            except StopIteration:
                break
        
        ret = self._buff[:n]
        self._buff = self._buff[len(ret):]
        return ret

    def read(self, n: Optional[int] = None) -> str:
        line = []

        if n is None or n < 0:
            while True:
                m = self._read1()

                if not m:
                    break

                line.append(m)
        else:
            while n > 0:
                m = self._read1(n)

                if not m:
                    break

                n -= len(m)
                line.append(m)
    
        return ''.join(line)


def file_to_iterable(file_path: str, fields: tuple, current_execution_date: str, delimiter: str = ',') -> StringIO:
    current_execution_date = datetime.strptime(current_execution_date, '%Y-%m-%d').date()
    data = DictReader(open(file_path), fieldnames=fields, delimiter=delimiter, quoting=QUOTE_ALL)

    print(current_execution_date)
    next(data)
    # Skip header row
    print(parser.parse((next(data)['last_update'])).date())

    file_iterator = StringIteratorIO(
        (
            delimiter.join(
                map(
                    clean_csv_value, (
                        row['province'],
                        row['country'],
                        row['last_update'],
                        row['confirmed'],
                        row['deaths'],
                        row['recovered'],
                        row['latitude'],
                        row['longitude'],
                    )
                )
            ) + '\n'
            for row in data if parser.parse(row['last_update']).date() == current_execution_date
        )
    )

    return file_iterator

def clean_csv_value(value: Optional[Any]) -> str:
    if value is None or value == '':
        return r'\N'

    return str(value).replace('\n', '\\n').replace(',', '')