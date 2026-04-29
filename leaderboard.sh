#!/bin/bash

GAME_FILTER=$1
SORT_BY=$2
FILE="history.csv"

VALID_GAMES=("Overall" "TicTacToe" "Connect4" "Othello" "Catan")
VALID_SORTS=("wins" "losses" "ratio")

# ---- Validate input ----
if [[ -z "$GAME_FILTER" || -z "$SORT_BY" ]]; then
    echo "Usage: $0 [Overall|TicTacToe|Connect4|Othello|Catan] [wins|losses|ratio]"
    exit 1
fi

# Validate game
if [[ ! " ${VALID_GAMES[@]} " =~ " ${GAME_FILTER} " ]]; then
    echo "Invalid game. Use one of: ${VALID_GAMES[*]}"
    exit 1
fi

# Validate sort
if [[ ! " ${VALID_SORTS[@]} " =~ " ${SORT_BY} " ]]; then
    echo "Invalid sort. Use: wins, losses, ratio"
    exit 1
fi

# File exists?
if [[ ! -f "$FILE" ]]; then
    echo "history.csv not found"
    exit 1
fi

# ---- Temp file (safe) ----
TMP_FILE=$(mktemp)

# ---- Generate leaderboard ----
awk -F ',' -v game_filter="$GAME_FILTER" '
BEGIN {
    game_map[0] = "TicTacToe"
    game_map[1] = "Connect4"
    game_map[2] = "Othello"
    game_map[3] = "Catan"
}
NR > 1 {
    game = game_map[$3]
    p1 = $4
    p2 = $5
    result = $6 + 0   # force numeric

    if (game_filter != "Overall" && game != game_filter)
        next

    players[p1] = 1
    players[p2] = 1

    if (result == 1) {
        wins[p1]++
        losses[p2]++
    } else if (result == 2) {
        wins[p2]++
        losses[p1]++
    } else if (result == 0) {
        wins[p1] += 0.5
        losses[p1] += 0.5
        wins[p2] += 0.5
        losses[p2] += 0.5
    }
}
END {
    for (p in players) {
        w = wins[p] + 0
        l = losses[p] + 0

        if (l == 0) {
            ratio_num = 1e9
            ratio_str = "∞"
        } else {
            ratio_num = w / l
            ratio_str = sprintf("%.3f", ratio_num)
        }

        printf "%s,%.2f,%.2f,%.6f,%s\n", p, w, l, ratio_num, ratio_str
    }
}
' "$FILE" > "$TMP_FILE"

# ---- Header ----
printf "\n%-15s %-10s %-10s %-10s\n" "Player" "Wins" "Losses" "Ratio"
printf "%s\n" "----------------------------------------------------------"

# ---- Sorting ----
if [[ "$SORT_BY" == "wins" ]]; then
    sort -t ',' -k2 -nr -k3 -n "$TMP_FILE"
elif [[ "$SORT_BY" == "losses" ]]; then
    sort -t ',' -k3 -n -k2 -nr "$TMP_FILE"
else
    sort -t ',' -k4 -nr -k2 -nr "$TMP_FILE"
fi | while IFS=',' read -r player wins losses ratio_num ratio
do
    printf "%-15s %-10s %-10s %-10s\n" "$player" "$wins" "$losses" "$ratio"
done

# ---- Cleanup ----
rm "$TMP_FILE"
