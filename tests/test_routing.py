import pytest
from utils import base_utils as ut

no_records = "bad request, no records"
odd = "odd"
even = "even"


@pytest.mark.parametrize('seed, exp_stream', [(1, odd), (2, even), (0, even), (-1, odd),
                                              (2222, even), (-8986757653, odd)])
def test_positive_routing(route_url, kinesis_client, get_stream_shard_iterator_odd,
                          get_stream_shard_iterator_even, seed, exp_stream):
    transaction_id = ut.get_request(route_url, seed)

    record_odd = ut.get_record_data(kinesis_client, get_stream_shard_iterator_odd)
    record_even = ut.get_record_data(kinesis_client, get_stream_shard_iterator_even)

    if exp_stream == odd:
        expected_record, unexpected_record = record_odd, record_even
    else:
        expected_record, unexpected_record = record_even, record_odd

    assert ut.find_record(expected_record, transaction_id, seed), \
        f"Record doesn't contain 'uuid' and/or 'seed' of GET request! GET request with seed: " \
        f"{seed} should be in record of the {exp_stream}"

    assert not ut.find_record(unexpected_record, transaction_id, seed), \
        f"Record was routed to the wrong stream! GET request with seed: {seed} was sent to unexepected stream"


@pytest.mark.parametrize('seed, result', [('wewe', no_records), (0.1, no_records), ("", no_records),
                                          ("[]", no_records)])
def test_negative_incorrect_seed_format(route_url, kinesis_client, get_stream_shard_iterator_odd,
                                        get_stream_shard_iterator_even, seed, result):
    ut.get_request(route_url, seed)
