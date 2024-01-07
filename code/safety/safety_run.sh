#!/bin/bash

index=0
prev_package=""
found=1
counter=0

json_array=()

while [ $found -eq 1 ]; do
  echolist=""
  found=0

  while read line; do
    package_name=$(echo $line | awk -F'==' '{print $1}')
    # find first package
    if [ "$prev_package" != "$package_name" ]; then
      counter=0
      prev_package=$package_name
    fi
    # find appropriate version
    if [ $counter -eq $index ]; then
      echolist+="$line\n"
      found=1
    fi
    # skip over left-over packages
    ((counter += 1))
  done < subset_requirements.txt
  ((index += 1))
  counter=0

  # save results to a variable
  result=$(echo -e $echolist | safety check --stdin --output json)
  # add to final array
  json_array+=$result

  # used for monitoring progress of the run and saving temporary results in case errors occur
  # echo -e $echolist
  # echo $result >> tempresults.json

done

# save into an almost json formatted array
merged="${json_array[*]}"

# replace }{ with },{ to make it fully json format
formatted_json="[$(echo "$merged" | sed -e 's/}{/},{/g' -e 's/} {/},{/g')]"

# save to file
echo "$formatted_json" > safety_set.json
