How to run test:
Python3 and pip should be installed

1. install requirements.txt: pip install -r requirements.txt
2. run test from command line:
		- run the test with default parameters:
			pytest --html=report.html tests\test_routing.py
		
		- run the test with custom parameters:
			pytest --html=report.html tests\test_routing.py --parameter_name="value" --parameter_name_2="value_2" etc.
			
			list of parameters:
			    route_url - default value is 'http://localhost:9000/route/'
				stream_odd - default value is 'li-stream-odd'
				stream_even - default value is 'li-stream-even'
				kinesis_endpoint_url - 'http://localhost:4568'
				kinesis_region_name - 'none'
				aws_key_id - 'none'
				aws_secret_key - 'none'
				aws_token - 'none'
				
3. Open 'report.html' after running test 