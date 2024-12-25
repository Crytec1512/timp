import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# Алгоритмы
def modular_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Обратное число для {a} по модулю {m} не существует")

def hill_encrypt(message, key):
    message = message.upper().replace(" ", "")
    message_nums = [ord(char) - ord('A') for char in message]

    if len(message_nums) % 2 != 0:
        message_nums.append(0)  # Дополняем 'A'

    blocks = [message_nums[i:i+2] for i in range(0, len(message_nums), 2)]
    encrypted_blocks = []
    for block in blocks:
        block = np.array(block)
        encrypted_block = np.dot(key, block) % 26
        encrypted_blocks.append(encrypted_block)
    
    encrypted_message = ''.join(chr(num + ord('A')) for block in encrypted_blocks for num in block)
    return encrypted_message

def hill_decrypt(ciphertext, key):
    ciphertext = ciphertext.upper().replace(" ", "")
    cipher_nums = [ord(char) - ord('A') for char in ciphertext]

    det = int(np.round(np.linalg.det(key))) % 26
    det_inv = modular_inverse(det, 26)
    adjugate = np.array([[key[1, 1], -key[0, 1]], [-key[1, 0], key[0, 0]]]) % 26
    key_inverse = (det_inv * adjugate) % 26
    
    blocks = [cipher_nums[i:i+2] for i in range(0, len(cipher_nums), 2)]
    decrypted_blocks = []
    for block in blocks:
        block = np.array(block)
        decrypted_block = np.dot(key_inverse, block) % 26
        decrypted_blocks.append(decrypted_block)
    
    decrypted_message = ''.join(chr(int(num) + ord('A')) for block in decrypted_blocks for num in block)
    return decrypted_message.strip('A')

def magic_square_encrypt(message, square):
    message = message.upper().replace(" ", "")
    n = len(square)
    while len(message) < n:
        message += 'X'
    encrypted = ''.join(message[square[i] - 1] for i in range(n))
    return encrypted

def magic_square_decrypt(ciphertext, square):
    n = len(square)
    decrypted = [''] * n
    for i, pos in enumerate(square):
        decrypted[pos - 1] = ciphertext[i]
    return ''.join(decrypted).rstrip('X')

# GUI функции
def get_hill_key():
    try:
        k11 = int(entry_k11.get())
        k12 = int(entry_k12.get())
        k21 = int(entry_k21.get())
        k22 = int(entry_k22.get())
        key = np.array([[k11, k12], [k21, k22]])
        det = int(np.round(np.linalg.det(key))) % 26
        if det == 0 or modular_inverse(det, 26) is None:
            raise ValueError("Матрица должна быть обратимой по модулю 26!")
        return key
    except Exception as e:
        messagebox.showerror("Ошибка", f"Некорректная матрица: {e}")
        return None

def get_magic_square():
    try:
        square = [int(entry.get()) for entry in magic_square_entries]
        if len(square) != 9 or sorted(square) != list(range(1, 10)):
            raise ValueError("Магический квадрат должен содержать числа от 1 до 9.")
        return square
    except Exception as e:
        messagebox.showerror("Ошибка", f"Некорректный магический квадрат: {e}")
        return None

def encrypt_message():
    algorithm = notebook.index(notebook.select())
    if algorithm == 0:  # Hill cipher
        plaintext = hill_input_text.get("1.0", tk.END).strip()
        if not plaintext:
            messagebox.showwarning("Ошибка", "Введите текст для шифрования!")
            return
        key = get_hill_key()
        if key is None:
            return
        encrypted = hill_encrypt(plaintext, key)
    elif algorithm == 1:  # Magic Square cipher
        plaintext = magic_input_text.get("1.0", tk.END).strip()
        if not plaintext:
            messagebox.showwarning("Ошибка", "Введите текст для шифрования!")
            return
        square = get_magic_square()
        if square is None:
            return
        encrypted = magic_square_encrypt(plaintext, square)
    else:
        messagebox.showerror("Ошибка", "Неизвестный алгоритм")
        return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, encrypted)

def decrypt_message():
    algorithm = notebook.index(notebook.select())
    if algorithm == 0:  # Hill cipher
        ciphertext = hill_input_text.get("1.0", tk.END).strip()
        if not ciphertext:
            messagebox.showwarning("Ошибка", "Введите текст для расшифровки!")
            return
        key = get_hill_key()
        if key is None:
            return
        decrypted = hill_decrypt(ciphertext, key)
    elif algorithm == 1:  # Magic Square cipher
        ciphertext = magic_input_text.get("1.0", tk.END).strip()
        if not ciphertext:
            messagebox.showwarning("Ошибка", "Введите текст для расшифровки!")
            return
        square = get_magic_square()
        if square is None:
            return
        decrypted = magic_square_decrypt(ciphertext, square)
    else:
        messagebox.showerror("Ошибка", "Неизвестный алгоритм")
        return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, decrypted)

# GUI
app = tk.Tk()
app.title("Шифрование")

notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill='both')

# Hill Cipher Tab
hill_frame = ttk.Frame(notebook)
notebook.add(hill_frame, text="Шифр Хилла")

ttk.Label(hill_frame, text="Введите сообщение:").pack()
hill_input_text = tk.Text(hill_frame, height=5, width=50)
hill_input_text.pack()

ttk.Label(hill_frame, text="Матрица для шифра Хилла (2x2):").pack()
matrix_frame = ttk.Frame(hill_frame)
matrix_frame.pack()
entry_k11 = ttk.Entry(matrix_frame, width=5)
entry_k11.grid(row=0, column=0)
entry_k12 = ttk.Entry(matrix_frame, width=5)
entry_k12.grid(row=0, column=1)
entry_k21 = ttk.Entry(matrix_frame, width=5)
entry_k21.grid(row=1, column=0)
entry_k22 = ttk.Entry(matrix_frame, width=5)
entry_k22.grid(row=1, column=1)

ttk.Label(hill_frame, text="* Матрица должна быть обратимой по модулю 26").pack()

# Magic Square Tab
magic_square_frame = ttk.Frame(notebook)
notebook.add(magic_square_frame, text="Магический квадрат")

ttk.Label(magic_square_frame, text="Введите сообщение:").pack()
magic_input_text = tk.Text(magic_square_frame, height=5, width=50)
magic_input_text.pack()

ttk.Label(magic_square_frame, text="Матрица магического квадрата:").pack()
magic_square_entries = []
magic_matrix_frame = ttk.Frame(magic_square_frame)
magic_matrix_frame.pack()
for i in range(3):
    for j in range(3):
        entry = ttk.Entry(magic_matrix_frame, width=5)
        entry.grid(row=i, column=j)
        magic_square_entries.append(entry)

ttk.Label(magic_square_frame, text="* Введите числа от 1 до 9, каждое ровно один раз.").pack()

# Общие кнопки
button_frame = ttk.Frame(app)
button_frame.pack()
encrypt_button = ttk.Button(button_frame, text="Зашифровать", command=encrypt_message)
encrypt_button.pack(side=tk.LEFT, padx=5)
decrypt_button = ttk.Button(button_frame, text="Расшифровать", command=decrypt_message)
decrypt_button.pack(side=tk.LEFT, padx=5)

# Результат
ttk.Label(app, text="Результат:").pack()
output_text = tk.Text(app, height=5, width=50)
output_text.pack()

app.mainloop()
