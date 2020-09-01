import os
import random
from PIL import Image, ImageDraw, ImageFont


class Crossword:
    def __init__(self, size):
        self.size = size
        self.words_available = []
        self.occupied = []
        self.definitions = dict()
        self.sentences = []

        self.board = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append("#")
            self.board.append(row)

        path = "." + os.sep + "data" + os.sep + "dictionary.txt"
        with open(path) as file:
            lines = file.readlines()
            for line in lines:
                result = line.replace("\n", "").split("|")
                word = result[0]
                self.definitions[word] = result[1]
                if len(word) <= self.size:
                    self.words_available.append(word)

        self.words_available = sorted(self.words_available, key=len)

    def print_board(self):
        """
        Print board to console for debug purposes
        """
        for row in self.board:
            text = "".join(row)
            print(text)

    def is_in_range(self, x, y):
        """
        Check if coordinates are in the board
        """
        if x >= self.size or x < 0 or y >= self.size or y < 0:
            return False
        return True

    def is_valid_position(self, x, y, direction, word):
        """
        Returns whether a word, identified by its position and direction, can fit correctly into the board
        :param x: row number
        :param y: col number
        :param direction: horizontal or vertical
        :param word: the word we want to insert
        :return: True if word can correctly be inserted, False otherwise
        """
        for i in range(len(word)):
            if direction == "vertical":
                # Check if word could be inserted in this position
                if not self.is_in_range(x+i, y) or (self.board[x+i][y] != "#" and self.board[x+i][y] != word[i]):
                    return False
                # Check for correctness of position in terms of interfering with neighbors
                if self.board[x+i][y] == "#":
                    # Check top of word
                    if i == 0 and self.is_in_range(x-1, y):
                        if self.board[x-1][y] != "#":
                            return False
                    # Check bottom of word
                    if i == len(word) - 1 and self.is_in_range(x + i + 1, y):
                        if self.board[x+i+1][y] != "#":
                            return False
                    # Check sides of each letter
                    if self.is_in_range(x+i, y + 1):
                        if self.board[x+i][y + 1] != "#":
                            return False
                    if self.is_in_range(x+i, y - 1):
                        if self.board[x+i][y - 1] != "#":
                            return False

            if direction == "horizontal":
                # Check if word could be inserted in this position
                if not self.is_in_range(x, y+i) or (self.board[x][y+i] != "#" and self.board[x][y+i] != word[i]):
                    return False
                # Check for correctness of position in terms of interfering with neighbors
                if self.board[x][y+i] == "#":
                    # Check left of word
                    if i == 0 and self.is_in_range(x, y-1):
                        if self.board[x][y-1] != "#":
                            return False
                    # Check right of word
                    if i == len(word) - 1 and self.is_in_range(x, y + i + 1):
                        if self.board[x][y+i+1] != "#":
                            return False
                    # Check top/bottom of each letter
                    if self.is_in_range(x + 1, y+i):
                        if self.board[x + 1][y+i] != "#":
                            return False
                    if self.is_in_range(x - 1, y+i):
                        if self.board[x - 1][y+i] != "#":
                            return False

        # Check if word overlaps with another word in the same direction
        if direction == "horizontal":
            if self.is_in_range(x, y-1):
                if self.board[x][y-1] != "#":
                    return False
            if self.is_in_range(x, y+len(word)):
                if self.board[x][y+len(word)] != "#":
                    return False
        if direction == "vertical":
            if self.is_in_range(x-1, y):
                if self.board[x-1][y] != "#":
                    return False
            if self.is_in_range(x+len(word), y):
                if self.board[x+len(word)][y] != "#":
                    return False

        # print(f"Valid position ({x}, {y}) for '{word}' in direction {direction}")
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
        # Check if possible
        if len(self.words_available) == 0:
            return False
        # Place randomly the first word on the board
        word = self.words_available[-1]
        while True:
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            direction = "vertical" if random.randint(0, 1) == 0 else "horizontal"
            if self.is_valid_position(x, y, direction, word):
                self.place_word_on_board(x, y, direction, word)
                break

        # Try and fit words onto the board so that they match the ones already inserted
        for _ in range(3):
            for word in self.words_available[::-1]:
                done = False
                for letter in word:
                    if done:
                        break
                    for placed_word in self.occupied:
                        if letter in placed_word["word"]: # True if there is an intersection between the two words
                            direction = "vertical" if placed_word["direction"] == "horizontal" else "horizontal"
                            # Calculate position of new word
                            if direction == "vertical":
                                x = placed_word["x"] - word.index(letter)
                                y = placed_word["y"] + placed_word["word"].index(letter)
                            else:
                                x = placed_word["x"] + placed_word["word"].index(letter)
                                y = placed_word["y"] - word.index(letter)
                            # Check if can be correctly inserted
                            if self.is_valid_position(x, y, direction, word):
                                self.place_word_on_board(x, y, direction, word)
                                done = True
                                break
        return True

    def get_board_score(self):
        """
        Returns a measure of how good a board is based on occupied places
        """
        occupied_spots = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != "#":
                    occupied_spots += 1
        return occupied_spots/(self.size**2)

    def save(self, filename, hide_words=False):
        """
        Saves the crossword to an image file
        :param filename: name of file that the image will be saved to
        :param hide_words: if True, only a number identifier will be displayed, if False the whole word is displayed
        """
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
        font_smaller = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 35)
        draw = ImageDraw.Draw(img)

        count = 1
        for i in range(self.size):
            for j in range(self.size):
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.board[i][j] != "#":
                    draw.rectangle(rect, fill="white")
                    if hide_words:
                        for word in self.occupied:
                            if i == word["x"] and j == word["y"]:
                                self.sentences.append(self.definitions[word["word"]])
                                w, h = draw.textsize(str(count), font=font_smaller)
                                if word["direction"] == "vertical":
                                    draw.text(
                                        (rect[0][0] + ((interior_size - w) / 2) - cell_size/5,
                                         rect[0][1] + ((interior_size - h) / 2) - 10 + cell_size/4),
                                        str(count), fill="black", font=font_smaller
                                    )
                                else:
                                    draw.text(
                                        (rect[0][0] + ((interior_size - w) / 2 + cell_size/5),
                                         rect[0][1] + ((interior_size - h) / 2) - 10 + cell_size/8),
                                        str(count), fill="black", font=font_smaller
                                    )
                                count += 1
                    else:
                        w, h = draw.textsize(self.board[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            self.board[i][j], fill="black", font=font
                        )

        img.save(filename)
        print(self.sentences)


def main():
    size = 20
    crossword = Crossword(size)
    crossword.solve()
    print(f"Words fitted: {len(crossword.occupied)} for a score of {crossword.get_board_score()}")
    crossword.save("output.png")
    crossword.save("output-hidden.png", True)


if __name__ == "__main__":
    main()
