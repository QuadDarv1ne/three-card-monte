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
            tooltip_window.title("Подсказка")

            message = (
                "Добро пожаловать в игру: «🎴Три карты Монте»\n\n"
                "Ваша задача - найти даму червей после перемешивания карт.\n\n"
                "Каждая карта в стандартной колоде карт имеет масть и достоинство.\n\n"
                "В данной игре используются четыре масти:\n"
                "♥ Червы (Hearts) - Изображены красными сердечками.\n"
                "♦ Бубны (Diamonds) - Изображены красными ромбами.\n"
                "♠ Пики (Spades) - Изображены черными лопатками.\n"
                "♣ Трефы (Clubs) - Изображены черными треугольниками.\n\n"
                "Нажмите \"OK\", чтобы начать."
            )

            text = tk.Text(tooltip_window, wrap="word", font=("Arial", 12), height=15, width=58)
            text.insert("1.0", message)
            text.tag_configure('hearts', foreground='red')
            text.tag_configure('diamonds', foreground='red')
            text.tag_configure('spades', foreground='black')
            text.tag_configure('clubs', foreground='black')

            text.tag_add('hearts', '8.0', '8.17')
            text.tag_add('diamonds', '9.0', '9.18')
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
        self.root.withdraw()  # Скрыть основное окно
        self.tooltip_window = TooltipWindow(self.root, self.start_game)
        self.continue_game = True

    def reset_game(self):
        self.continue_game = True
        self.tooltip_window.tooltip_shown = False

    def display_cards(self, cards):
        """
        Отображает карты из списка cards кортежей (достоинство, масть).
        """
        rows = ['', '', '', '', '']  # Содержит текст для вывода на экран.

        for _ in range(5):
            row = ''
            for i, card in enumerate(cards):
                rank, suit = card  # card представляет собой структуру данных — кортеж.
                if _ == 0:
                    row += ' ___ '  # Выводим верхнюю линию карты.
                elif _ == 1:
                    row += '|{} | '.format(rank.ljust(2))
                elif _ == 2:
                    row += '| {} | '.format(suit)
                elif _ == 3:
                    row += '|_{}| '.format(rank.rjust(2, '_'))
            rows[_] = row

        # Построчно выводим на экран:
        for row in rows:
            print(row)

    def get_random_card(self):
        """
        Возвращает случайную карту — НЕ даму червей.
        """
        while True:  # Подбираем карты, пока получим НЕ даму червей.
            rank = random.choice(list('23456789JQKA') + ['10'])
            suit = random.choice(['♥', '♦', '♠', '♣'])

            # Возвращаем карту, если это не дама червей:
            if rank != 'Q' and suit != '♥':
                return rank, suit

    def start_game(self):
        self.tooltip_window.tooltip_shown = False

        while self.continue_game:
            print('\n' * 8)  # Очистка консоли (печать 10 пустых строк)
            print('🎴 Три карты Монте.\n💼 Автор: Максим Дуплей\n📧 Почта: maksimqwe42@mail.ru\n')
            print('Найдите даму червей.')
            print('Обратите внимание, как двигаются карты.\n')

            # Отображаем исходную раскладку карт:
            cards = [('Q', '♥'), self.get_random_card(), self.get_random_card()]
            random.shuffle(cards)  # Помещаем даму червей в случайное место.
            print('Вот карты:')
            self.display_cards(cards)
            input('Нажмите Enter, когда будете готовы начать ...')

            # Отображаем на экране перетасовки карт:
            for _ in range(17):
                swap = random.choice(['l-m', 'm-r', 'l-r', 'm-l', 'r-m', 'r-l'])

                if swap == 'l-m':
                    print('○ перестановка левой и средней')
                    cards[0], cards[1] = cards[1], cards[0]
                elif swap == 'm-r':
                    print('○ перестановка средней и правой')
                    cards[1], cards[2] = cards[2], cards[1]
                elif swap == 'l-r':
                    print('○ перестановка левой и правой')
                    cards[0], cards[2] = cards[2], cards[0]
                elif swap == 'm-l':
                    print('○ перестановка средней и левой')
                    cards[1], cards[0] = cards[0], cards[1]
                elif swap == 'r-m':
                    print('○ перестановка правой и средней')
                    cards[2], cards[1] = cards[1], cards[2]
                elif swap == 'r-l':
                    print('○ перестановка правой и левой')
                    cards[2], cards[0] = cards[0], cards[2]

                time.sleep(0.7)

            # Просим пользователя найти даму червей:
            while True:
                print('Под какой картой находится дама червей? (LEFT MIDDLE RIGHT)')
                guess = input('> ').upper()

                # Находим индекс в cards введенной пользователем позиции:
                if guess in ['LEFT', 'MIDDLE', 'RIGHT']:
                    guess_index = ['LEFT', 'MIDDLE', 'RIGHT'].index(guess)
                    break

                self.display_cards(cards)  # Отображаем все карты.

            # Проверяем, выиграл ли игрок:
            if cards[guess_index] == ('Q', '♥'):
                print('Вы выиграли')
            else:
                print('Вы проиграли')

            # Спрашиваем пользователя о продолжении игры:
            response = input('\nХотите сыграть еще раз? (да/нет): ').lower()
            if response == 'нет':
                print('Спасибо за игру :D')
                self.continue_game = False
                self.root.destroy()  # Закрытие основного окна Tkinter


if __name__ == "__main__":
    game = ThreeCardMonteGame()
    game.tooltip_window.show_tooltip()
    game.root.mainloop()  # Запуск Tkinter mainloop

# 🗓️ Дата: 01.12.2023