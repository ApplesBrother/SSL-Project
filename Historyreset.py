import csv
import os
with open("history.csv", "w",newline="") as history:
    append = csv.writer(history)
    append.writerow(["Idx", "Time", "Game", "Player 1","Player 2", "Result"])
with open("Serial.txt", "w") as history:
    history.write("0")
with open("SavedGames.txt", "w") as history:
    history.write("")