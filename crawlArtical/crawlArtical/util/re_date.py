import re

# birthday = "xxx出生于1991年1月5日"
# birthday = "xxx出生于1991-1-5"
# birthday = "xxx出生于1991-01-05"
# birthday = "xxx出生于1991/1/5"
# birthday = "xxx出生于1991/01/05"
birthday = "xxx出生于1991.01.05"
# birthday = "xxx出生于1991-01"
# birthday = "xxx出生于1991年01月"

regex_str = ".*出生于(\d{4}[年/.-]\d{1,2}([月/.-]\d{1,2}日|$|[月/.-]$|[月/.-]\d{1,2}))"
# regex_str = ".*出生于(\d{4}[.年/-]\d{1,2}([.月/-]\d{1,2}日|$|[.月/-]$|[.月/-]\d{1,2}))"
match_obj = re.match(regex_str,birthday)
if match_obj:
    print(match_obj.group(1))