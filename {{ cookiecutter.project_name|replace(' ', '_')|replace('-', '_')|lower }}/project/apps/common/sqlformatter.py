import sqlparse

from django.utils.log import ServerFormatter
from pygments import formatters, highlight, lexers

TIME_CRIT = 0.2
TIME_WARN = 0.05
TIME_FORMAT = u'\x1b[0;30;{bgcolor}m {duration:.3f}s \x1b[0m\n{msg}'

LEXER = lexers.SqlLexer()
FORMATTER = formatters.Terminal256Formatter(style='monokai')


class SqlFormatter(ServerFormatter):
    def format(self, record):

        try:
            sql = record.sql.strip()
            duration = record.duration
        except AttributeError:
            return super(SqlFormatter, self).format(record)

        sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
        bg_color = 41 if duration > TIME_CRIT else 43 if duration > TIME_WARN else 42

        return TIME_FORMAT.format(bgcolor=bg_color,
                                  duration=duration,
                                  msg=highlight(sql, LEXER, FORMATTER))
