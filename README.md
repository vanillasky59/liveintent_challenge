# QA-Challenge

Requirements:

* Python 3
* Pip

## Setup

```sh
pip install -r requirements.txt
```

## Run

```sh
pytest --html=report.html tests\test_routing.py
```

Open `report.html`

## Run with custom parameters

```sh
pytest --html=report.html tests\test_routing.py --parameter_name="value" --parameter_name_2="value_2" etc.
```

Available parameters:

* `route_url` - default value is `http://localhost:9000/route/`
* `stream_odd` - default value is `li-stream-odd`
* `stream_even` - default value is `li-stream-even`
* `kinesis_endpoint_url` - `http://localhost:4568`
* `kinesis_region_name` - `none`
* `aws_key_id` - `none`
* `aws_secret_key` - `none`
* `aws_token` - `none`
