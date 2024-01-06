#!/bin/bash

mkdir temp 2> /dev/null
mkdir results 2> /dev/null

function moveToFolderAndScan (){
  first_folder=$(ls -d -t */ | head -n 1)
  # skip folder if name is incorrect
  if [ -n "$first_folder" ]; then
    # move into the folder if extraction was successful
    cd $first_folder
    # run bandit
    bandit -r . -f csv | tail -n +2 >> ../../results/$1.csv
    cd ..
  fi
}
# for every line in subset_requirements.txt
while read line; do
  echo "$line"
  cd temp
  # download the tar.gz to temp
  pip download $line
  file=$(find . -type f -name "*.tar.gz" | head -n 1)
  file2=$(find . -type f -name "*.whl" | head -n 1)
  if [ -n "$file" ]; then
    echo $file
    # extract if the tar.gz exists
    tar -xzvf "$file"
  elif [ -n "$file2" ] ; then
    mv $file2 archive.zip
  fi
  file3=$(find . -type f -name "*.zip" | head -n 1)
  if [ -n "$file3" ]; then
    mkdir archive
    unzip -d archive $file3
  fi
  # after extracting the folder, move into the folder and run the scan
  moveToFolderAndScan $line
  # go back to temp and empty out folder by removing it and recreating it
  cd ..
  rm -r -f temp
  sleep 5
  mkdir temp
done < subset_requirements.txt