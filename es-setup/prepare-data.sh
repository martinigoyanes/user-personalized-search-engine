export dump=data/enwikiquote-20220328-cirrussearch-content.json.gz
export index=enwikiquote

echo "Creating chunks/ for the to store data chunks"
cd data
mkdir chunks
cd chunks

echo "Splitting data into 250 document chunks per json file...."
gunzip -c ../../$dump | gsplit -d -a3 --additional-suffix=.json -l 500 - $index

echo "Cleaning json formatting of files so they are readable by ES Bulk API..."
for file in *; do
	sed "s/\"_type\":\"page\",//g" $file > "clean-${file}"
	rm $file
	echo "${file} cleaned, deleting it"
done
echo "Finished! Removing dump: ${dump}"
rm ../../$dump