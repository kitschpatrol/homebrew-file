#!/usr/bin/env bash


dest="./bin/brew-file"
output="$dest".tmp
echo "#!/usr/bin/env python3" > $output
grep -E "(^from|^import)" src/brew_file/*.py|grep -v "from \."| cut -d ":" -f2|sort -u >> $output
cat src/brew_file/info.py|grep -vE "(^from|^import)" >> $output
cat src/brew_file/utils.py|grep -vE "(^from|^import)" >> $output
cat src/brew_file/brew_helper.py|grep -vE "(^from|^import)" >> $output
cat src/brew_file/brew_info.py|grep -vE "(^from|^import)" >> $output
cat src/brew_file/brew_file.py|grep -vE "(^from|^import)" >> $output
cat src/brew_file/main.py|grep -vE "(^from|^import)" >> $output

black $output
isort $output
autoflake --in-place $output
autopep8 --in-place $output

diff -u $dest $output
mv $output $dest
chmod 755 $dest
