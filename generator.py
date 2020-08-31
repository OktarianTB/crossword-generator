import os
from time import sleep
import random
from PIL import Image, ImageDraw, ImageFont


class Crossword:
    def __init__(self, size, nb_words):
        self.size = size
        self.nb_words = nb_words
        self.words_available = []
        self.occupied = []

        self.board = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append("#")
            self.board.append(row)

        self.dictionary = []
        path = "." + os.sep + "data" + os.sep + "words.txt"
        with open(path) as file:
            lines = file.readlines()
            for line in lines:
                word = line.replace("\n", "")
                self.dictionary.append(word)

        while len(self.words_available) < nb_words*5:
            random_word = random.choice(self.dictionary)
            if random_word not in self.words_available and len(random_word) <= self.size:
                self.words_available.append(random_word)
        self.words_available = sorted(self.words_available, key=len)

    def print_board(self):
        for row in self.board:
            text = "".join(row)
            print(text)

    def is_in_range(self, x, y):
        if x >= self.size or x < 0 or y >= self.size or y < 0:
            return False
        return True

    def is_valid_position(self, x, y, direction, word):
        for i in range(len(word)):
            if direction == "vertical":
                if not self.is_in_range(x+i, y) or (self.board[x+i][y] != "#" and self.board[x+i][y] != word[i]):
                    return False
                if self.board[x+i][y] == "#":
                    if i == 0 and self.is_in_range(x-1, y):
                        if self.board[x-1][y] != "#":
                            return False
                    if i == len(word) - 1 and self.is_in_range(x + i + 1, y):
                        if self.board[x+i+1][y] != "#":
                            return False
                    if self.is_in_range(x+i, y + 1):
                        if self.board[x+i][y + 1] != "#":
                            return False
                    if self.is_in_range(x+i, y - 1):
                        if self.board[x+i][y - 1] != "#":
                            return False

            if direction == "horizontal":
                if not self.is_in_range(x, y+i) or (self.board[x][y+i] != "#" and self.board[x][y+i] != word[i]):
                    return False
                if self.board[x][y+i] == "#":
                    if i == 0 and self.is_in_range(x, y-1):
                        if self.board[x][y-1] != "#":
                            return False
                    if i == len(word) - 1 and self.is_in_range(x, y + i + 1):
                        if self.board[x][y+i+1] != "#":
                            return False
                    if self.is_in_range(x + 1, y+i):
                        if self.board[x + 1][y+i] != "#":
                            return False
                    if self.is_in_range(x - 1, y+i):
                        if self.board[x - 1][y+i] != "#":
                            return False
        print(f"Valid position ({x}, {y}) for '{word}' in direction {direction}")
        return True

    def place_word_on_board(self, x, y, direction, word):
        for j in range(len(word)):
            if direction == "vertical":
                self.board[x + j][y] = word[j]
            if direction == "horizontal":
                self.board[x][y + j] = word[j]
        self.occupied.append({"x": x, "y": y, "direction": direction, "word": word})
        self.words_available.remove(word)

    def solve(self):
        print(self.words_available)
        word = self.words_available[-1]
        while True:
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            direction = "vertical" if random.randint(0, 1) == 0 else "horizontal"
            if self.is_valid_position(x, y, direction, word):
                self.place_word_on_board(x, y, direction, word)
                break
        for _ in range(5):
            for word in self.words_available[::-1]:
                done = False
                for letter in word:
                    if done:
                        break
                    for placed_word in self.occupied:
                        if letter in placed_word["word"]:
                            direction = "vertical" if placed_word["direction"] == "horizontal" else "horizontal"
                            if direction == "vertical":
                                x = placed_word["x"] - word.index(letter)
                                y = placed_word["y"] + placed_word["word"].index(letter)
                            else:
                                x = placed_word["x"] + placed_word["word"].index(letter)
                                y = placed_word["y"] - word.index(letter)
                            if self.is_valid_position(x, y, direction, word):
                                self.place_word_on_board(x, y, direction, word)
                                done = True
                                break
                if len(self.occupied) >= self.nb_words:
                    break

    def get_word(self):
        base = random.choice(self.occupied)
        direction = "vertical" if base["direction"] == "horizontal" else "horizontal"
        word = None
        x = None
        y = None
        if direction == "vertical":
            base_x = base["x"]
            base_y = random.randint(base["y"], base["y"] + len(base["word"]) - 1)
        else:
            base_x = random.randint(base["x"], base["x"] + len(base["word"]) - 1)
            base_y = base["y"]
        while True:
            word = random.choice(self.dictionary)
            if word not in self.words and self.board[base_x][base_y] in word:
                if direction == "vertical":
                    x = base_x - word.index(self.board[base_x][base_y])
                    y = base_y
                else:
                    x = base_x
                    y = base_y - word.index(self.board[base_x][base_y])
                if self.is_valid_position(x, y, direction, word):
                    return x, y, direction, word

    def create(self):
        while True:
            print("search")
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            direction = "vertical" if random.randint(0, 1) == 0 else "horizontal"
            word = random.choice(self.dictionary)
            if word not in self.words and self.is_valid_position(x, y, direction, word):
                for j in range(len(word)):
                    if direction == "vertical":
                        self.board[x + j][y] = word[j]
                    if direction == "horizontal":
                        self.board[x][y + j] = word[j]
                self.words.append(word)
                self.occupied.append({"x": x, "y": y, "direction": direction, "word": word})
                self.print_board()
                break

        for i in range(self.nb_words-1):
            print("i: " + str(i))
            x, y, direction, word = self.get_word()
            for j in range(len(word)):
                if direction == "vertical":
                    self.board[x+j][y] = word[j]
                if direction == "horizontal":
                    self.board[x][y+j] = word[j]
            self.words.append(word)
            self.occupied.append({"x": x, "y": y, "direction": direction, "word": word})
            self.print_board()
        print("done")

    def save(self, filename):
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.size * cell_size,
             self.size * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.size):
            for j in range(self.size):
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.board[i][j]:
                    draw.rectangle(rect, fill="white")
                    if self.board[i][j] != "#":
                        draw.rectangle(rect, fill="white")
                        w, h = draw.textsize(self.board[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            self.board[i][j], fill="black", font=font
                        )

        img.save(filename)


def main():
    size = 12
    words = 12
    crossword = Crossword(size, words)
    crossword.solve()
    print("-----------------------------------")
    crossword.print_board()
    print(f"Words fitted: {len(crossword.occupied)}/{words}")
    crossword.save("output.png")


if __name__ == "__main__":
    main()