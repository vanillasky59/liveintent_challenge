import pytest
import boto3
from utils import base_utils as ut
import config as cfg


def pytest_addoption(parser):
    parser.addoption("--route_url", action="store", default=cfg.route_url, help="Route URL")
    parser.addoption("--stream_odd", action="store", default=cfg.streams["odd"], help="Kinesis stream odd")
    parser.addoption("--stream_even", action="store", default=cfg.streams["even"], help="Kinesis stream even")
    parser.addoption("--kinesis_endpoint_url", action="store",
                     default=cfg.kinesis_params["kinesis_endpoint_url"],
                     help="URL and port where Kinesis is running")
    parser.addoption("--region_name", action="store", default=cfg.kinesis_params["region_name"],
                     help="Kinesis region name")
    parser.addoption("--aws_key_id", action="store", default=cfg.kinesis_params["aws_key_id"],
                     help="Kinesis AWS access key ID")
    parser.addoption("--aws_secret_key", action="store", default=cfg.kinesis_params["aws_secret_key"],
                     help="Kinesis AWS secret access key")
    parser.addoption("--aws_token", action="store", default=cfg.kinesis_params["aws_token"],
                     help="Kinesis AWS session token")


@pytest.fixture(scope="module")
def kinesis_client(kinesis_endpoint_url, region_name, aws_key_id, aws_secret_key, aws_token):
    kinesis = boto3.client(
        'kinesis',
        endpoint_url=kinesis_endpoint_url,
        region_name=region_name,
        aws_access_key_id=aws_key_id,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=aws_token
    )
    return kinesis


@pytest.fixture(scope="function")
def route_url(request):
    return request.config.getoption("--route_url")


@pytest.fixture(scope="function")
def get_stream_shard_iterator_odd(kinesis_client, stream_odd):
    return ut.get_stream_shard_iterator(kinesis_client, stream_odd)


@pytest.fixture(scope="function")
def get_stream_shard_iterator_even(kinesis_client, stream_even):
    return ut.get_stream_shard_iterator(kinesis_client, stream_even)


@pytest.fixture(scope="module")
def stream_odd(request):
    return request.config.getoption("--stream_odd")


@pytest.fixture(scope="module")
def stream_even(request):
    return request.config.getoption("--stream_even")


@pytest.fixture(scope="module")
def kinesis_endpoint_url(request):
    return request.config.getoption("--kinesis_endpoint_url")


@pytest.fixture(scope="module")
def region_name(request):
    return request.config.getoption("--region_name")


@pytest.fixture(scope="module")
def aws_key_id(request):
    return request.config.getoption("--aws_key_id")


@pytest.fixture(scope="module")
def aws_secret_key(request):
    return request.config.getoption("--aws_secret_key")


@pytest.fixture(scope="module")
def aws_token(request):
    return request.config.getoption("--aws_token")
