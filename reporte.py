class Reporte:

    def __init__ (self, point, miss, letter):
        self.point = point
        self.miss = miss
        self.letter = letter
        if self.point + self.miss == 0:
            self.res = 0
        else:
            self.res = round(((self.point/(self.point + self.miss))*100), 2)

    def result(self):
        return self.res 

    def __str__(self):
        return f"Al realizar la letra {self.letter} obtuvo un {self.res}% de precision"

