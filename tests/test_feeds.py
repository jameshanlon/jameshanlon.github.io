from datetime import datetime
from zoneinfo import ZoneInfo

from ssg.feeds import entry_id


def test_entry_id_uses_the_tag_uri_scheme():
    date = datetime(2026, 9, 15, tzinfo=ZoneInfo("Europe/Paris"))
    link = "https://jameswhanlon.com/benchmarking-slang-netlist.html"
    assert entry_id(link, date) == (
        "tag:jameswhanlon.com,2026-09-15:/benchmarking-slang-netlist.html"
    )
