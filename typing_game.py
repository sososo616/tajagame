import tkinter as tk
import random

EASY_WORDS = [
    'cat', 'dog', 'sun', 'hat', 'pen', 'cup', 'book', 'fish', 'milk', 'star',
    'map', 'fan', 'bed', 'egg', 'leaf', 'run', 'ball', 'tree', 'box', 'toy',
    'frog', 'duck', 'sock', 'ring', 'boat', 'cake', 'jump', 'sand', 'snow', 'rain'
]
MEDIUM_WORDS = [
    'apple', 'grape', 'melon', 'peach', 'hello', 'candy', 'world', 'bread', 'water', 'cloud',
    'lemon', 'plant', 'smile', 'green', 'house', 'zebra', 'piano', 'river', 'mouse', 'music',
    'friend', 'ticket', 'bubble', 'school', 'orange', 'banana', 'market', 'animal', 'flower', 'jungle'
]
HARD_WORDS = [
    'cherry', 'python', 'typing', 'strawberry', 'elephant', 'mountain', 'language', 'umbrella', 'sandwich', 'calendar',
    'airplane', 'computer', 'keyboard', 'solution', 'activity', 'chocolate', 'magazine', 'hospital', 'invisible', 'algorithm',
    'awkward', 'rhythm', 'subtlety', 'acquaintance', 'bureaucracy', 'unbelievable', 'pronunciation', 'entrepreneur',
    'miscellaneous', 'conscientious', 'acknowledgment', 'characteristic', 'psychologist', 'indispensable', 'catastrophic',
    'consequence', 'recommendation', 'architectural', 'interpretation', 'communication'
]



class TypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("타이핑 게임")
        self.root.geometry("400x400")

        self.score = 0
        self.word_count = 0
        self.max_words = 10
        self.time_limit = 5
        self.remaining_time = 0
        self.used_words = []
        self.current_word = ""
        self.word_list = MEDIUM_WORDS

        # === 난이도 선택 ===
        difficulty_frame = tk.Frame(root)
        difficulty_frame.grid(row=0, column=0, columnspan=3, pady=10)

        tk.Label(difficulty_frame, text="난이도 선택:").grid(row=0, column=0, padx=5)
        tk.Button(difficulty_frame, text="쉬움", width=8,
                  command=lambda: self.set_difficulty("easy")).grid(row=0, column=1, padx=5)
        tk.Button(difficulty_frame, text="보통", width=8,
                  command=lambda: self.set_difficulty("medium")).grid(row=0, column=2, padx=5)
        tk.Button(difficulty_frame, text="어려움", width=8,
                  command=lambda: self.set_difficulty("hard")).grid(row=0, column=3, padx=5)

        self.difficulty_label = tk.Label(root, text="현재 난이도: 보통")
        self.difficulty_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        # === 게임 영역 ===
        self.word_label = tk.Label(root, text="", font=("Arial", 24))
        self.word_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.entry = tk.Entry(root, font=("Arial", 18))
        self.entry.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
        self.entry.bind("<Return>", self.check_word)

        self.score_label = tk.Label(root, text="점수: 0 / 0", font=("Arial", 14))
        self.score_label.grid(row=4, column=0, columnspan=3)

        self.timer_label = tk.Label(root, text="남은 시간: 0초", font=("Arial", 12))
        self.timer_label.grid(row=5, column=0, columnspan=3, pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.grid(row=6, column=0, columnspan=3)

        self.start_button = tk.Button(root, text="게임 시작", font=("Arial", 12), command=self.start_game)
        self.start_button.grid(row=7, column=0, columnspan=3, pady=10)

    def set_difficulty(self, level):
        if level == "easy":
            self.word_list = EASY_WORDS
            self.time_limit = 8
            self.difficulty_label.config(text="현재 난이도: 쉬움")
        elif level == "medium":
            self.word_list = MEDIUM_WORDS
            self.time_limit = 8
            self.difficulty_label.config(text="현재 난이도: 보통")
        elif level == "hard":
            self.word_list = HARD_WORDS
            self.time_limit = 8 
            self.difficulty_label.config(text="현재 난이도: 어려움")

    def start_game(self):
        self.score = 0
        self.word_count = 0
        self.used_words = []
        self.score_label.config(text=f"점수: 0 / {self.max_words}")
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.next_word()

    def next_word(self):
        if self.word_count >= self.max_words:
            self.word_label.config(text="")
            self.result_label.config(text=f"게임 종료! 최종 점수: {self.score} / {self.max_words}")
            self.timer_label.config(text="")
            return

        available_words = list(set(self.word_list) - set(self.used_words))
        if not available_words:
            self.word_label.config(text="")
            self.result_label.config(text="모든 단어 사용 완료!")
            self.timer_label.config(text="")
            return

        self.current_word = random.choice(available_words)
        self.used_words.append(self.current_word)
        self.word_label.config(text=self.current_word)
        self.word_count += 1

        self.remaining_time = self.time_limit
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.config(text=f"남은 시간: {self.remaining_time}초")
            self.remaining_time -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.result_label.config(text=f"시간 초과! 정답은: {self.current_word}")
            self.entry.delete(0, tk.END)
            self.update_score_label()
            self.next_word()

    def check_word(self, event):
        typed = self.entry.get().strip()
        self.root.after_cancel(self.timer_id)

        if typed == self.current_word:
            self.score += 1
            self.result_label.config(text="정답!")
        else:
            self.result_label.config(text=f"오답! 정답은: {self.current_word}")

        self.update_score_label()
        self.entry.delete(0, tk.END)
        self.next_word()

    def update_score_label(self):
        self.score_label.config(text=f"점수: {self.score} / {self.max_words}")

# 메인 실행
if __name__ == "__main__":
    root = tk.Tk()
    game = TypingGame(root)
    root.mainloop()
