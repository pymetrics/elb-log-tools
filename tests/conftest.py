import random
from datetime import datetime

import pytest
from faker import Faker


fake = Faker()


class Log:
    def __init__(self, status_code=200, method="GET", path="/"):
        self.timestamp = f"{datetime.now().isoformat()}Z"
        self.elb = "test-elb"
        self.client = f"{fake.ipv4()}:80"
        self.backend = f"{fake.ipv4()}:80"
        self.request_processing_time = round(random.random(), ndigits=3) / 1000
        self.backend_processing_time = round(random.paretovariate(4), ndigits=5)
        self.response_processing_time = round(random.random(), ndigits=3) / 1000
        self.elb_status_code = status_code
        self.backend_status_code = status_code
        self.received_bytes = 0
        self.sent_bytes = 100
        self.request = f"{method} https://example.com:443{path} HTTP/1.1"
        self.user_agent = fake.user_agent()
        self.ssl_cipher = "ECDHE-RSA-AES128-GCM-SHA256"
        self.ssl_protocol = "TLSv1.2"

    def __str__(self):
        return " ".join(
            [
                self.timestamp,
                self.elb,
                self.client,
                self.backend,
                str(self.request_processing_time),
                str(self.backend_processing_time),
                str(self.response_processing_time),
                str(self.elb_status_code),
                str(self.backend_status_code),
                str(self.received_bytes),
                str(self.sent_bytes),
                f'"{self.request}"',
                self.user_agent,
                self.ssl_cipher,
                self.ssl_protocol,
            ]
        )


@pytest.fixture
def log_factory():
    def wrapped(*args, **kwargs):
        return str(Log(*args, **kwargs))

    return wrapped
