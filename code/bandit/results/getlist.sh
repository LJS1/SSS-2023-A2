while read line; do
  echo "$line"
  file=$(find . -type f -name "$line.csv")
  if [ -n "$file" ]; then
    echo "exists"
  else
    echo "$line" >> redo.txt
  fi
done < ../subset_requirements_new.txt
