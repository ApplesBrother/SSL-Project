echo "First Username: "
read user1
if awk -F '\t' -v u="$user1" '$1 == u {found=1} END {exit !found}' users.tsv
then
  echo "Username exists"
else
  echo "Username not found"
fi
