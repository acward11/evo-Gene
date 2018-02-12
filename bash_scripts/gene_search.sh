#/bin/bash

BLAST=""
HMMR=""

while read -r line
do

	if [[ $line = "PATH_TO_BLAST"* ]]; then
		BLAST=$line
	fi

	if [[ $line = "PATH_TO_HMMR"* ]]; then
		HMMR=$line
	fi
done < ../configure 

echo $BLAST
echo $HMMR
