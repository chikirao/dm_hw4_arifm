from decimal import Decimal, getcontext

getcontext().prec = 150

class ArithmeticCoder:
    def __init__(self, text):
        self.text = text
        self.segments = self.calculate_segments(text)
    
    def calculate_segments(self, text):
        frequency = {}
        for char in text:
            frequency[char] = frequency.get(char, 0) + 1

        total = Decimal(len(text))
        probabilities = {char: Decimal(freq) / total for char, freq in frequency.items()}
        segments = {}
        current_left = Decimal('0')

        for char in sorted(probabilities.keys()):
            prob = probabilities[char]
            segments[char] = {
                'left': current_left,
                'right': current_left + prob
            }
            current_left += prob

        print("\nИнформация про символы:")
        print("Символ\tЧастота\tВероятность\tЛевая\tПравая")
        for char, segment in segments.items():
            print(f"{char}\t{frequency[char]}\t{probabilities[char]:.5f}\t\t{segment['left']:.5f}\t{segment['right']:.5f}")
        
        return segments

    def encode(self):
        left = Decimal('0')
        right = Decimal('1')
        interval_history = []

        for char in self.text:
            segment = self.segments[char]
            range_width = right - left
            new_left = left + range_width * segment['left']
            new_right = left + range_width * segment['right']
            
            interval_history.append((char, new_left, new_right))
            left, right = new_left, new_right

        code = (left + right) / 2
        return code, interval_history

    def encode_binary(self, code):
        result = []
        while code > 0 and len(result) < 100:
            code *= 2
            if code >= 1:
                result.append('1')
                code -= 1
            else:
                result.append('0')
        return ''.join(result)

def main():
    text = input("Введите кодируемый текст: ").strip()
    
    if not text:
        print("Ошибка: пустая строка.")
        return
    
    coder = ArithmeticCoder(text)
    code, history = coder.encode()

    print("\nТаблица кодирования:")
    print("Символ\tЛевая граница\tПравая граница")
    for char, left, right in history:
        print(f"{char}\t{left:.15f}\t{right:.15f}")

    print(f"\nКод в виде десятичного числа: {code:.50f}")
    binary_code = coder.encode_binary(code)
    print(f"Код в виде двоичного числа: {binary_code}")

if __name__ == "__main__":
    main()
