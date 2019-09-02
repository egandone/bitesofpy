from enum import Enum
from datetime import datetime
from collections import Counter


class DateFormat(Enum):
    DDMMYY = 0  # dd/mm/yy
    MMDDYY = 1  # mm/dd/yy
    YYMMDD = 2  # yy/mm/dd
    NONPARSABLE = -999

    @classmethod
    def get_d_parse_formats(cls, val=None):
        """ Arg:
        val(int | None) enum member value
        Returns:
        1. for val=None a list of explicit format strings 
            for all supported date formats in this enum
        2. for val=n an explicit format string for a given enum member value
        """
        d_parse_formats = ["%d/%m/%y", "%m/%d/%y", "%y/%m/%d"]
        if val is None:
            return d_parse_formats
        if 0 <= val <= len(d_parse_formats):
            return d_parse_formats[val]
        raise ValueError


class InfDateFmtError(Exception):
    """custom exception when it is not possible to infer a date format
    e.g. too many NONPARSABLE or a tie """
    pass


def _maybe_DateFormats(date_str):
    """ Args:
    date_str (str) string representing a date in unknown format
    Returns:
    a list of enum members, where each member represents
    a possible date format for the input date_str
    """
    d_parse_formats = DateFormat.get_d_parse_formats()
    maybe_formats = []
    for idx, d_parse_fmt in enumerate(d_parse_formats):
        try:
            _parsed_date = datetime.strptime(date_str, d_parse_fmt) # pylint: disable=W0612
            maybe_formats.append(DateFormat(idx))
        except ValueError:
            pass
    if len(maybe_formats) == 0:
        maybe_formats.append(DateFormat.NONPARSABLE)
    return maybe_formats

def _map_to_yyyymmdd_format(fmt, date_str):
    yyyyddmm_date = 'Invalid'
    try:
        date = datetime.strptime(date_str, fmt)
        yyyyddmm_date = f'{date:%Y-%m-%d}'
    except ValueError:
        pass
    return yyyyddmm_date

def get_dates(dates):
    """ Args:
    dates (list) list of date strings
    where each list item represents a date in unknown format
    Returns:
    list of date strings, where each list item represents
    a date in yyyy-mm-dd format. Date format of input date strings is
    inferred based on the most prevalent format in the dates list.
    Alowed/supported date formats are defined in a DF enum class.
    """
    # complete this method
    format_counter = Counter()
    for d in dates:
        format_counter.update(_maybe_DateFormats(d))
    top_formats = format_counter.most_common()
    # Pull out the top format
    top_format = top_formats[0][0]
    # And it's count
    top_format_count = top_formats[0][1]
    # If most are unparsable raise an exception
    if top_format == DateFormat.NONPARSABLE:
        raise(InfDateFmtError('Mostly NONPARSABLE dates'))
    # If there are more then one format and the counts
    # for the top two are the same the we also raise an 
    # exception because there is no way to know which format
    # to use.
    if (len(top_formats) > 1) and (top_format_count == top_formats[1][1]):
        raise(InfDateFmtError('Tie for most common format'))

    # From the class side method on DateFormat pull out the
    # date parsing string
    date_parse_fmt = DateFormat.get_d_parse_formats(top_formats[0][0].value)
    # Iterate over all the dates using the most common format
    # and then, if that worked, print it out in the standard 
    # YYYY-MM-DD format.  If the date can't be parsed then 
    # it get's mapped to 'Invalid'
    return_dates = list(map(lambda d: _map_to_yyyymmdd_format(date_parse_fmt, d), dates))
    return return_dates