import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os


class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.geometry("800x600")

        self.bg_image = Image.open("background.png")
        self.bg_image = self.bg_image.resize((800, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=800, height=600)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.word_frame = tk.Frame(self.canvas)
        self.word_frame.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.word_labels = []

        self.attempts_label = tk.Label(self.canvas, text="Attempts left: ", font=("Arial", 14), bg="white")
        self.attempts_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.canvas.create_text(400, 550, text="Hangman Game", font=("Arial", 20), fill="white")

        self.canvas.create_rectangle(100, 50, 700, 550, outline="white")

        self.canvas.create_text(400, 575, text="© 2024", font=("Arial", 10), fill="white")

        self.create_game()

        self.load_images()

        self.display_image()

        self.create_alphabet()

    def create_game(self):
        self.words = ["apple", "banana", "orange", "grape", "pineapple", "strawberry", "kiwi", "watermelon", "peach"]
        self.word = random.choice(self.words)
        self.guessed_letters = []
        self.attempts = 6

        for letter in self.word:
            label = tk.Label(self.word_frame, text="_", font=("Arial", 24), bg="white")
            label.pack(side=tk.LEFT)
            self.word_labels.append(label)

        self.attempts_label.config(text="Attempts left: {}".format(self.attempts))

    def load_images(self):
        self.images = []
        for i in range(self.attempts + 1):
            image_path = os.path.join("images", f"hangman_{i}.png")
            image = Image.open(image_path)
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)
            self.images.append(photo)

    def display_image(self):
        self.canvas.delete("hangman")
        self.canvas.create_image(50, 50, anchor=tk.NW, image=self.images[self.attempts], tags="hangman")

    def display_word(self):
        for i, letter in enumerate(self.word):
            if letter in self.guessed_letters:
                self.word_labels[i].config(text=letter)
            else:
                self.word_labels[i].config(text="_")

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            messagebox.showwarning("Duplicate Guess", "You've already guessed that letter.")
            return

        self.guessed_letters.append(letter)
        if letter not in self.word:
            self.attempts -= 1
            self.attempts_label.config(text="Attempts left: {}".format(self.attempts))
            if self.attempts == 0:
                messagebox.showinfo("Game Over", "You lose! The word was: {}".format(self.word))
                self.master.destroy()
                return
            else:
                self.display_image()
        else:
            self.display_word()
            if all(letter in self.guessed_letters for letter in self.word):
                messagebox.showinfo("Congratulations", "You guessed the word: {}".format(self.word))
                self.master.destroy()
                return

        self.update_alphabet(letter)

    def create_alphabet(self):
        self.alphabet_frame = tk.Frame(self.canvas)
        self.alphabet_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.alphabet_buttons = []
        for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
            row = i // 13
            col = i % 13
            button = tk.Button(self.alphabet_frame, text=letter.upper(), font=("Comic Sans MS", 14), bg=None,
                               command=lambda l=letter: self.guess_letter(l))
            button.grid(row=row, column=col, padx=5, pady=5)
            self.alphabet_buttons.append(button)

    def update_alphabet(self, letter):
        for button in self.alphabet_buttons:
            if button.cget("text").lower() == letter:
                button.config(state="disabled")


def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
