#!/bin/bash

SORT_BY=$1

if [[ -z "$SORT_BY" ]]; then
    SORT_BY="wins"
fi

if [[ "$SORT_BY" != "wins" && "$SORT_BY" != "losses" && "$SORT_BY" != "ratio" ]]; then
    echo "Invalid sort metric. Use: wins | losses | ratio"
    exit 1
fi

FILE="history.csv"

if [[ ! -f "$FILE" ]]; then
    echo "history.csv not found!"
    exit 1
fi

# Skip header and process
awk -F',' '
NR > 1 {
    p1 = $3
    p2 = $4
    game = $5
    result = $6

    key1 = game ":" p1
    key2 = game ":" p2

    players[key1] = p1
    players[key2] = p2
    games[key1] = game
    games[key2] = game

    if (result == 1) {
        wins[key1]++
        losses[key2]++
    } else if (result == 2) {
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

        split(k, arr, ":")
        game = arr[1]
        player = arr[2]

        printf "%s,%s,%.1f,%.1f,%.6f,%s\n", game, player, w, l, ratio_num, ratio_str
    }
}
' "$FILE" > temp_leaderboard.csv

# Decide sort column
if [[ "$SORT_BY" == "wins" ]]; then
    SORT_COL=3
elif [[ "$SORT_BY" == "losses" ]]; then
    SORT_COL=4
else
    SORT_COL=5
fi

# Print formatted table
printf "\n%-15s %-15s %-10s %-10s %-10s\n" "Game" "Player" "Wins" "Losses" "Ratio"
printf "%s\n" "---------------------------------------------------------------------"

sort -t',' -k$SORT_COL -nr -k3 -nr temp_leaderboard.csv | while IFS=',' read -r game player wins losses ratio_num ratio
do
    printf "%-15s %-15s %-10s %-10s %-10s\n" "$game" "$player" "$wins" "$losses" "$ratio"
done

rm temp_leaderboard.csv
