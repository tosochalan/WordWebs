import matplotlib.pyplot as plt
from scripts import utils

class Zipf:
    def __init__(self):
        self.frequencies = {}

    def plot(self):
        if len(self.frequencies) == 0:
            print("Empty data")
            return
        
        x = list(range(len(self.frequencies)))
        y = sorted(self.frequencies.values(), reverse=True)
        print(sorted(self.frequencies.items(), key=lambda x: x[1], reverse=True))

        plt.plot(x, y, marker="o")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Poradie slova")
        plt.ylabel("Frekvencia slova")
        plt.title("Závislosť frekvencie slov od poradia (Zipfov zákon)")
        plt.show()

    def read(self, file):
        self.frequencies = {}
        file = open(file, encoding="utf-8")
        words = file.read().split()
        file.close()
        for word in words:
            token = utils.strip_word(word)[0]
            self.frequencies[token] = self.frequencies.get(token, 0) + 1

if __name__ == "__main__":
    z = Zipf()

    z.read("text_files/ww2.txt")
    z.plot()