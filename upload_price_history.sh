today=$(date +"%Y-%m-%d")
curl -X GET https://api.covalenthq.com/v1/pricing/historical_by_addresses_v2/56/USD/0x26193c7fa4354ae49ec53ea2cebc513dc39a10aa/\?quote-currency\=USD\&format\=JSON\&from\=2021-12-16\&to\=$today\&key\=ckey_docs  | jq '.data[0]' > sea-token-price-history.json
aws s3 cp sea-token-price-history.json s3://gametaverse-daily/starsharks/sea-token-price-history.json --profile default
