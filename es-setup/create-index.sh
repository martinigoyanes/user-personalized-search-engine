export es=https://localhost:9200
export site=en.wikipedia.org
export wikiIndex=enwikiquote
export usersIndex=users
export queriesIndex=queries
export esUser=elastic
export esPass=personalized-search-22
export certFile=ca.crt
export dumpUrl="https://dumps.wikimedia.org/other/cirrussearch/20220328/enwikiquote-20220328-cirrussearch-content.json.gz"


echo "Creating dir to store data (data/) and downloading english wikipedia quotes into it ..."
mkdir data
cd data
wget $dumpUrl

export containerId=$(docker ps -aqf "name=personalized-search_es01")
docker cp $containerId:/usr/share/elasticsearch/config/certs/ca/ca.crt .

echo "If index $usersIndex alreayd exists, deleting it...."
curl --cacert $certFile -u $esUser:$esPass -XDELETE $es/$usersIndex?pretty

echo "Creating $usersIndex index ...."
curl --cacert $certFile -u $esUser:$esPass -H 'Content-Type: application/json' -XPUT $es/$usersIndex?pretty -d '{
  "mappings": {
    "properties": {
      "username": { "type": "text" },
      "password": { "type": "text" }
    }
  }
}'

echo "If index $queriesIndex alreayd exists, deleting it...."
curl --cacert $certFile -u $esUser:$esPass -XDELETE $es/$queriesIndex?pretty


echo "Creating $queriesIndex index ...."
curl --cacert $certFile -u $esUser:$esPass -H 'Content-Type: application/json' -XPUT $es/$queriesIndex?pretty -d '{
  "mappings": {
    "properties": {
      "search": { "type": "text" },
      "username": { "type": "keyword" },
      "timestamp": { "type": "date" }
    }
  }
}'

echo "If index $wikiIndex alreayd exists, deleting it...."
curl --cacert $certFile -u $esUser:$esPass -XDELETE $es/$wikiIndex?pretty

echo "Creating $wikiIndex index with no mappings...."
curl --cacert $certFile -u $esUser:$esPass -H 'Content-Type: application/json' -XPUT $es/$wikiIndex?pretty 

echo "Finished! Removing certificate file"
rm $certFile