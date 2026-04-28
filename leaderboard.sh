#!/bin/bash

GAME_FILTER=$1
FILE="history.csv"

VALID_GAMES=( "Overall" "TicTacToe" "Connect4" "Othello" "Catan" )

if [[ -z "$GAME_FILTER" ]]; then
    echo "Usage: $0 [game]"
    exit 1
fi

is_valid=false
for g in "${VALID_GAMES[@]}";do
    if [[ "$GAME_FILTER" == "$g" ]]; then
        is_valid=true
        break
    fi
done

if [[ "$is_valid" == false ]]; then
    echo "Invalid game. Use one of: ${VALID_GAMES[*]}"
    exit 1
fi

if [[ ! -f "$FILE" ]]; then
    echo "history.csv not found"
    exit 1
fi

generate_leaderboard(){
awk -F ',' -v game_filter="$GAME_FILTER" '
NR > 1{
    game = $3
    p1 = $4
    p2 = $5
    result = $6
    
    if (game_filter != "Overall" && game != game_filter)
        next
    
    key1 = p1
    key2 = p2

    players[key1] = p1
    players[key2] = p2
    games[key1] = game
    games[key2] = game

    if (result == 1){
        wins[key1]++
        losses[key2]++
    } else if (result == 2){
        wins[key2]++
        losses[key1]++
    } else if (result == 0){
        wins[key1] += 0.5
        losses[key1] += 0.5
        wins[key2] += 0.5
        losses[key2] += 0.5
    }
}
END {
    for (k in players) {
        w = wins[k] + 0
        l = losses[k] + 0

        if (l == 0) {
            ratio_num = 999999
            ratio_str = "∞"
        } else {
            ratio_num = w / l
            ratio_str = sprintf("%.3f", ratio_num)
        }

        player = k

        printf "%s, %.1f, %.1f, %.6f, %s\n", player, w, l, ratio_num, ratio_str
    }
}
' "$FILE" > temp_leaderboard.csv
}

print_leaderboard(){
    SORT_BY=$1

    if [[ "$SORT_BY" == "wins" ]]; then
        SORT_COL=2
    elif [[ "$SORT_BY" == "losses" ]]; then
        SORT_COL=3
    else
        SORT_COL=4
    fi

    printf "\n%-15s %-10s %-10s %-10s\n" "Player" "Wins" "Losses" "Ratio"
    printf "%s\n" "---------------------------------------------------------------------"

    sort -t ',' -k $SORT_COL -nr -k3 -nr temp_leaderboard.csv | while IFS=',' read -r player wins losses ratio_num ratio
    do
        printf "%-15s %-10s %-10s %-10s\n" "$player" "$wins" "$losses" "$ratio"
    done
}

generate_leaderboard

current_sort="wins"
print_leaderboard "$current_sort"

while true; do
    echo ""
    read -p "Enter sort (wins/losses/ratio) or 'exit': " input

    if [[ "$input" == "exit" ]]; then
        break
    fi
    if [[ "$input" != "wins" && "$input" != "losses" && "$input" != "ratio" ]]; then
        echo "Invalid input."
        continue
    fi

    current_sort="$input"
    print_leaderboard "$current_sort"
done

rm temp_leaderboard.csv
