import pytest
from utils import base_utils as ut


@pytest.mark.parametrize('seed', [1, 2, 0, -1, 2222, -8986757653])
def test_positive_routing(route_url, kinesis_client, get_stream_shard_iterator_odd,
                          get_stream_shard_iterator_even, seed):
    transaction_id = ut.get_request(route_url, seed)

    record_odd = ut.get_record_data(kinesis_client, get_stream_shard_iterator_odd)
    record_even = ut.get_record_data(kinesis_client, get_stream_shard_iterator_even)

    if seed % 2 != 0:
        expected_record, unexpected_record = record_odd, record_even
    else:
        expected_record, unexpected_record = record_even, record_odd

    assert expected_record is not None, \
        f"Record is not exist! GET request with seed: {seed} wasn't sent to exepected stream"
    assert expected_record["uuid"] == transaction_id and expected_record["seed"] == int(seed), \
        f"Record doesn't contain 'uuid' and/or 'seed' of GET request! " \
        "GET request with seed: {seed}"
    assert unexpected_record is None, \
        f"Record was routed to the wrong stream! GET request with seed: {seed} was sent to unexepected stream"


@pytest.mark.parametrize('seed', ['wewe', 0.1, "", "[]"])
def test_negative_incorrect_seed_format(route_url, kinesis_client, get_stream_shard_iterator_odd,
                                        get_stream_shard_iterator_even, seed):
    ut.get_request(route_url, seed)

    record_odd = ut.get_record_data(kinesis_client, get_stream_shard_iterator_odd)
    record_even = ut.get_record_data(kinesis_client, get_stream_shard_iterator_even)

    assert record_odd is None and record_even is None, \
        "Record was routed! GET request with seed: " + seed + " was sent to li-stream-odd or/and li-stream-even"
