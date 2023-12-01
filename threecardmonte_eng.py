import os
import random
import time
import tkinter as tk
from tkinter import messagebox


class TooltipWindow:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.tooltip_shown = False

    def show_tooltip(self):
        if not self.tooltip_shown:
            tooltip_window = tk.Toplevel(self.master)
            tooltip_window.title("Hint")

            message = (
                "Welcome to the game: '🎴Three Card Monte'\n\n"
                "Your task is to find the Queen of Hearts after shuffling the cards.\n\n"
                "Each card in a standard deck has a suit and a rank.\n\n"
                "Four suits are used in this game:\n"
                "♥ Hearts - Represented by red hearts.\n"
                "♦ Diamonds - Represented by red diamonds.\n"
                "♠ Spades - Represented by black spades.\n"
                "♣ Clubs - Represented by black clubs.\n\n"
                "Press 'OK' to start."
            )

            text = tk.Text(tooltip_window, wrap="word", font=("Arial", 12), height=15, width=58)
            text.insert("1.0", message)
            text.tag_configure('hearts', foreground='red')
            text.tag_configure('diamonds', foreground='red')
            text.tag_configure('spades', foreground='black')
            text.tag_configure('clubs', foreground='black')

            text.tag_add('hearts', '8.0', '8.8')
            text.tag_add('diamonds', '9.0', '9.10')
            text.tag_add('spades', '11.0', '12.0')
            text.tag_add('clubs', '13.0', '14.0')

            text.config(state=tk.DISABLED)
            text.pack()

            tooltip_window.resizable(width=False, height=False)
            tooltip_window.attributes('-topmost', 1)
            tooltip_window.transient()

            ok_button = tk.Button(tooltip_window, text="OK", command=lambda: [tooltip_window.destroy(), self.callback()])
            ok_button.pack()

            self.tooltip_shown = True


class ThreeCardMonteGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        self.tooltip_window = TooltipWindow(self.root, self.start_game)
        self.continue_game = True

    def reset_game(self):
        self.continue_game = True
        self.tooltip_window.tooltip_shown = False

    def display_cards(self, cards):
        """
        Display cards from the list of card tuples (rank, suit).
        """
        rows = ['', '', '', '', '']  # Contains text to print on the screen.

        for _ in range(5):
            row = ''
            for i, card in enumerate(cards):
                rank, suit = card  # card is a tuple.
                if _ == 0:
                    row += ' ___ '  # Print the top line of the card.
                elif _ == 1:
                    row += '|{} | '.format(rank.ljust(2))
                elif _ == 2:
                    row += '| {} | '.format(suit)
                elif _ == 3:
                    row += '|_{}| '.format(rank.rjust(2, '_'))
            rows[_] = row

        # Print line by line:
        for row in rows:
            print(row)

    def get_random_card(self):
        """
        Return a random card that is NOT the Queen of Hearts.
        """
        while True:  # Keep picking cards until we get a card that is NOT the Queen of Hearts.
            rank = random.choice(list('23456789JQKA') + ['10'])
            suit = random.choice(['♥', '♦', '♠', '♣'])

            # Return the card if it is NOT the Queen of Hearts:
            if rank != 'Q' and suit != '♥':
                return rank, suit

    def start_game(self):
        self.tooltip_window.tooltip_shown = False

        while self.continue_game:
            print('\n' * 8)  # Clear the console (print 10 empty lines)
            print('🎴 Three Card Monte.\n💼 Author: Maxim Duplay\n📧 Email: maksimqwe42@mail.ru\n')
            print('Find the Queen of Hearts.')
            print('Notice how the cards move.\n')

            # Display the initial card layout:
            cards = [('Q', '♥'), self.get_random_card(), self.get_random_card()]
            random.shuffle(cards)  # Place the Queen of Hearts in a random position.
            print('Here are the cards:')
            self.display_cards(cards)
            input('Press Enter when you are ready to start ...')

            # Display card shuffling on the screen:
            for _ in range(17):
                swap = random.choice(['l-m', 'm-r', 'l-r', 'm-l', 'r-m', 'r-l'])

                if swap == 'l-m':
                    print('○ swapping left and middle')
                    cards[0], cards[1] = cards[1], cards[0]
                elif swap == 'm-r':
                    print('○ swapping middle and right')
                    cards[1], cards[2] = cards[2], cards[1]
                elif swap == 'l-r':
                    print('○ swapping left and right')
                    cards[0], cards[2] = cards[2], cards[0]
                elif swap == 'm-l':
                    print('○ swapping middle and left')
                    cards[1], cards[0] = cards[0], cards[1]
                elif swap == 'r-m':
                    print('○ swapping right and middle')
                    cards[2], cards[1] = cards[1], cards[2]
                elif swap == 'r-l':
                    print('○ swapping right and left')
                    cards[2], cards[0] = cards[0], cards[2]

                time.sleep(0.7)

            # Ask the user to find the Queen of Hearts:
            while True:
                print('Which card is the Queen of Hearts under? (LEFT MIDDLE RIGHT)')
                guess = input('> ').upper()

                # Find the index in cards of the user-entered position:
                if guess in ['LEFT', 'MIDDLE', 'RIGHT']:
                    guess_index = ['LEFT', 'MIDDLE', 'RIGHT'].index(guess)
                    break

                self.display_cards(cards)  # Display all cards.

            # Check if the player won:
            if cards[guess_index] == ('Q', '♥'):
                print('You won!')
            else:
                print('You lost')

            # Ask the user if they want to play again:
            response = input('\nDo you want to play again? (yes/no): ').lower()
            if response == 'no':
                print('Thanks for playing :D')
                self.continue_game = False
                self.root.destroy()  # Close the Tkinter main window


if __name__ == "__main__":
    game = ThreeCardMonteGame()
    game.tooltip_window.show_tooltip()
    game.root.mainloop()  # Run Tkinter mainloop

# 🗓️ Дата: 01.12.2023