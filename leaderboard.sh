#!/bin/bash

GAME_FILTER=$1
SORT_BY=$2
FILE="history.csv"

VALID_GAMES=("Overall" "TicTacToe" "Connect4" "Othello" "Catan")
VALID_SORTS=("wins" "losses" "ratio")

# Check arguments
if [[ -z "$GAME_FILTER" || -z "$SORT_BY" ]]; then
    echo "Usage: $0 [game] [wins|losses|ratio]"
    exit 1
fi

# Validate game
is_valid=false
for g in "${VALID_GAMES[@]}"; do
    if [[ "$GAME_FILTER" == "$g" ]]; then
        is_valid=true
        break
    fi
done

if [[ "$is_valid" == false ]]; then
    echo "Invalid game. Use one of: ${VALID_GAMES[*]}"
    exit 1
fi

# Validate sort
is_valid_sort=false
for s in "${VALID_SORTS[@]}"; do
    if [[ "$SORT_BY" == "$s" ]]; then
        is_valid_sort=true
        break
    fi
done

if [[ "$is_valid_sort" == false ]]; then
    echo "Invalid sort. Use: wins, losses, ratio"
    exit 1
fi

# File check
if [[ ! -f "$FILE" ]]; then
    echo "history.csv not found"
    exit 1
fi

# Generate leaderboard
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

        printf "%s,%.1f,%.1f,%.6f,%s\n", k, w, l, ratio_num, ratio_str
    }
}
' "$FILE" > temp_leaderboard.csv

# Decide sort column
if [[ "$SORT_BY" == "wins" ]]; then
    SORT_COL=2
elif [[ "$SORT_BY" == "losses" ]]; then
    SORT_COL=3
else
    SORT_COL=4
fi

# Print leaderboard
printf "\n%-15s %-10s %-10s %-10s\n" "Player" "Wins" "Losses" "Ratio"
printf "%s\n" "----------------------------------------------------------"

sort -t ',' -k $SORT_COL -nr -k2 -nr temp_leaderboard.csv | while IFS=',' read -r player wins losses ratio_num ratio
do
    printf "%-15s %-10s %-10s %-10s\n" "$player" "$wins" "$losses" "$ratio"
done

rm temp_leaderboard.csv
