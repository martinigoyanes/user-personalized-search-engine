export es=https://localhost:9200
export index=enwikiquote
export esUser=elastic
export esPass=personalized-search-22
export certFile=ca.crt

cd data
echo "Grabbing certificate from ES container to interact with ES..."
export containerId=$(docker ps -aqf "name=personalized-search_es01")
docker cp $containerId:/usr/share/elasticsearch/config/certs/ca/ca.crt .

cd chunks
for file in *; do
	echo "Indexing ${file} ...."
	curl --cacert ../$certFile -u $esUser:$esPass -H "Content-Type: application/json" -XPOST "$es/$index/_bulk?pretty&refresh" --data-binary "@${file}"
done

echo "Finished! Removing certificate file and data/. Go to kibana (http://0.0.0.0:5601/) to test. Username: ${esUser} Password: ${esPass}"
rm ../$certFile
rm -rf ../../data