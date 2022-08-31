echo "Creating docker containers for ES cluster to live in"
docker-compose up -d

echo "##############################################"
echo "## Creating index enwikiquote in ES cluster ##"
echo "##############################################"
./create-index.sh

echo "#####################################"
echo "## Preparing data to index into ES ##"
echo "#####################################"
./prepare-data.sh

echo "##########################################"
echo "## Indexing data into enwikiquote index ##"
echo "##########################################"
./index-data.sh


echo "###########"
echo "## Done! ##"
echo "###########"

echo "To shut down ES cluster: cd es-setup && docker-compose down"
echo "To start up ES cluster again: cd es-setup && docker-compose up -d"