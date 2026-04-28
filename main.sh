log1=false
while [ "$log1" = false ]; do
    echo "First Username: "
    read user1
    if [ $(cut -d $'\t' -f1 users.tsv | grep -c "^${user1}$") -eq 1 ]; then
        echo "Enter password: "
        read -s pass1
        hash1=$(echo -n "$pass1" | sha256sum | cut -d ' ' -f1)
        if [ $(grep -c "^$user1"$'\t'"$hash1$" users.tsv) -eq 1 ]; then
            log1=true
        else
            echo "Wrong password!! Please try again..."
        fi
    else
        echo "New Username. Do you want to make a new player?(Enter "Yes" or "No")"
        read newu
        if [[ "$newu" =~ ^[Yy][Ee][Ss]$ ]]; then
		echo "Enter Password:"
                read -s pass1
                hash1=$(echo -n "$pass1" | sha256sum | cut -d ' ' -f1)
                echo -e "${user1}\t${hash1}" >> users.tsv
                echo "New account created!"
                log1=true
	elif [[ "$newu" =~ ^[Nn][Oo]$ ]]; then
                echo "Then play as another player"
                log1=false
        fi
    fi
done

log2=false
while [ "$log2" = false ]; do
    echo "Second Username: "
    read user2
    if [ $(cut -d $'\t' -f1 users.tsv | grep -c "^${user2}$") -eq 1 ]; then
        echo "Enter password: "
        read -s pass2
        hash2=$(echo -n "$pass2" | sha256sum | cut -d ' ' -f1)
        if [ $(grep -c "^$user2"$'\t'"$hash2$" users.tsv) -eq 1 ]; then
            log2=true
        else
            echo "Wrong password!! Please try again..."
        fi
    else
        echo "New Username. Do you want to make a new player?(Enter "Yes" or "No")"
        read newu
        if [[ "$newu" =~ ^[Yy][Ee][Ss]$ ]]; then
                echo "Enter Password:"
		read -s pass2
                hash2=$(echo -n "$pass2" | sha256sum | cut -d ' ' -f1)
                echo -e "${user2}\t${hash2}" >> users.tsv
                echo "New account created!"
                log2=true
	elif [[ "$newu" =~ ^[Nn][Oo]$ ]]; then
		echo "Then play as another player"
                log2=false
        fi
    fi
done

python3 gaming.py ${user1} ${user2}
