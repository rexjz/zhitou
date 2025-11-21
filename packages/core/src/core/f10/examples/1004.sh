curl --location --request POST 'https://dz-f10.cf69.com/f10/api/' \
--header 'Accept-Language: zh-CN' \
--header 'Org-key: dz' \
--header 'User-Agent: Apifox/1.0.0 (https://apifox.com)' \
--header 'Content-Type: application/json' \
--header 'Accept: */*' \
--header 'Host: dz-f10.cf69.com' \
--header 'Connection: keep-alive' \
--data-raw '{
  "trade_market": "SHMK",
  "mode_code": "1004",
  "body": {
    "stk_id": "600000",
    "max_date": "2020-01-01",
    "order_by_date": "asc",
    "page_num": 1,
    "page_size": 10
  }
}'