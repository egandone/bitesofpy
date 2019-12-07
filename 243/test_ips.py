import os
from pathlib import Path
from ipaddress import IPv4Network
from urllib.request import urlretrieve

import pytest

from ips import (ServiceIPRange, parse_ipv4_service_ranges,
                 get_aws_service_range)

URL = "https://bites-data.s3.us-east-2.amazonaws.com/ip-ranges.json"
TMP = os.getenv("TMP", r'C:\WUTemp')
PATH = Path(TMP, "ip-ranges.json")
IP = IPv4Network('192.0.2.8/29')


@pytest.fixture(scope='module')
def json_file():
    """Import data into tmp folder"""
    urlretrieve(URL, PATH)
    return PATH


# write your pytest code ...
def test_basic_test_file(json_file):
    ranges = parse_ipv4_service_ranges(json_file)
    assert ranges != None, "Test file should parse to something"
    assert len(ranges) == 1886, "Test file should have 1886 IPv4 addresses"


def test_get_aws_service_range(json_file):
    ranges = parse_ipv4_service_ranges(json_file)
    aws_ranges = get_aws_service_range('54.238.0.0', ranges)
    assert aws_ranges != None, "Should find 54.238.0.0 in test file"
    assert len(
        aws_ranges) == 2, "Should find 2 instances of 54.238.0.0 in test file"

    services = {range.service for range in aws_ranges}
    assert services == {'AMAZON', 'EC2'}

    regions = {range.region for range in aws_ranges}
    assert regions == {'ap-northeast-1'}

    cidrs = {str(range.cidr.network_address) for range in aws_ranges}
    assert cidrs == {'54.238.0.0'}

    range_strs = [str(range) for range in aws_ranges if range.service == 'EC2']
    assert range_strs[0] == '54.238.0.0/16 is allocated to the EC2 service in the ap-northeast-1 region'


def test_edge_conditions(json_file):
    ranges = parse_ipv4_service_ranges(json_file)

    with pytest.raises(ValueError, match='Address must be a valid IPv4 address') as ve:
        get_aws_service_range('not.a.gootd.address', ranges)

    aws_ranges = get_aws_service_range('54.238.0.0', [])
    assert len(aws_ranges) == 0

    aws_ranges = get_aws_service_range('192.168.0.0', ranges)
    assert len(aws_ranges) == 0
