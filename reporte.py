class Reporte:

    def __init__ (self, times, letter):
        self.times = times
        self.letter = letter

    def __str__(self):
        percent = self.times/10
        percent = percent*100
        return f"Al realizar la letra {self.letter} obtuvo un {percent}% de éxito"

r = Reporte(10, "A")
print(r)
