class Reporte:

    def __init__ (self, point, miss, letter):
        self.point = point
        self.miss = miss
        self.letter = letter

    def __str__(self):
        percent = self.point/(self.point + self.miss)
        percent = percent*100
        return f"Al realizar la letra {self.letter} obtuvo un {percent}% de éxito"

