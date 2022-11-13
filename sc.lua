-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header

wrk.method = "GET"
wrk.body   = '{ "date": "31.1.2021", "periods": 4, "amount": 10000, "rate": 6 }'
wrk.headers["Content-Type"] = "application/json"

