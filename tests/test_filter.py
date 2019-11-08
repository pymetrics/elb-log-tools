from io import StringIO
from itertools import chain, repeat
from elb_log_tools import filter


class Opts:
    def __init__(self, logs, exclude_statuses=None, include_statuses=None):
        self.exclude_statuses = exclude_statuses or []
        self.include_statuses = include_statuses or []
        self.input_stream = logs
        self.output_stream = StringIO()

    @property
    def output(self):
        self.output_stream.seek(0)
        return list(self.output_stream.readlines())


def test_filter_logs_exclude_statuses(log_factory):
    logs = [log_factory(status_code=s) for s in chain(repeat(200, 5), repeat(400, 3))]
    opts = Opts(logs, exclude_statuses=[400])
    filter.filter_logs(opts)
    assert len(opts.output) == 5


def test_filter_logs_include_statuses(log_factory):
    logs = [
        log_factory(status_code=s)
        for s in chain(repeat(200, 5), repeat(400, 3), repeat(302, 3))
    ]
    opts = Opts(logs, include_statuses=[400])
    filter.filter_logs(opts)
    assert len(opts.output) == 3
