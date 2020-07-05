import requests
import json


def get_stream_shard_iterator(kinesis_client, stream_name):
    kinesis_stream = kinesis_client.describe_stream(StreamName=stream_name)

    shards = kinesis_stream['StreamDescription']['Shards']
    shard_ids = [shard['ShardId'] for shard in shards]

    iters_response = [kinesis_client.get_shard_iterator(StreamName=stream_name, ShardId=shard_id,
                                                        ShardIteratorType="LATEST") for shard_id in shard_ids]

    return [iter_response['ShardIterator'] for iter_response in iters_response]


def get_request(route_url, seed):
    url = route_url + str(seed)
    get_reqst = requests.get(url)
    transaction_id = get_reqst.headers.get('X-Transaction-Id')
    if isinstance(seed, int):
        assert get_reqst.status_code == 200, "Unexpected error: GET request " + url + " response code is not 200"
        assert transaction_id, "Unexpected error: GET request " + url + \
                               ". Response header doesn't contain 'X-Transaction-Id'"
    else:
        assert get_reqst.status_code == 400 or get_reqst.status_code == 404, \
            "Unexpected error: GET request " + url + " response code is not 400 or 404"
        assert transaction_id is None, "Unexpected error: GET request " + url + \
                                       ". Response header contain 'X-Transaction-Id'"

    print(get_reqst.status_code)
    print(get_reqst.headers.get('X-Transaction-Id'))
    return transaction_id


def get_record_data(kinesis_client, iterators):
    records = [kinesis_client.get_records(ShardIterator=iterator, Limit=200) for iterator in iterators]
    data = []
    for record in records:
        for record_data in record["Records"]:
            if "Data" in record_data:
                data.append(json.loads(record_data["Data"]))
    return data


def find_record(records, transaction_id, seed):
    return any(record["uuid"] == transaction_id and record["seed"] == int(seed) for record in records)
