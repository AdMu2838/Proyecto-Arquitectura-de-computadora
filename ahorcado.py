from tkinter import *

class JuegoTk:

    def __init__(self):
        self.EstamosJugando=False

    def JuegoNuevo(self):
        self.EstamosJugando=True
        self.ObjetoJuego.nuevojuego()
        self.EntradaTexto.focus_set()
        self.__ActualizarVista()

    def BotonEnviar(self):
        if self.EstamosJugando:
            self.ObjetoJuego.jugar(self.EntradaTexto.get())
            if self.ObjetoJuego.getVictoria() or not(self.ObjetoJuego.getJugadorEstaVivo()):
                self.EstamosJugando=False
            self.__ActualizarVista()
        else:
            self.JuegoNuevo()
        self.EntradaTexto.delete(0,"end")    

    def __ActualizarVista(self):
        if self.EstamosJugando:
            letrero=""
            for x in self.ObjetoJuego.getLetrero(): letrero+=x+" "
            self.Texto1.set(letrero)
            mensaje="Tus jugadas: "
            for x in self.ObjetoJuego.getLetrasUsadas():mensaje+=x
            self.Texto2.set(mensaje)
        else:
            if self.ObjetoJuego.getVictoria():
                self.Texto1.set("¡Felicidades Has ganado! :) ")
                self.Texto2.set("La palabra es "+self.ObjetoJuego.getPalabra())
            else:
                self.Texto1.set("Lo siento, perdiste :( ")
                self.Texto2.set("La palabra era "+self.ObjetoJuego.getPalabra())
        self.__Dibujo()        

    def __Dibujo(self, canvas, oportunidades):
        if self.EstamosJugando:
            if oportunidades==1:
                canvas.delete("all")
                canvas.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                canvas.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                canvas.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                canvas.create_line(150,110,150,190,width=5,fill="white")#torso
                canvas.create_line(150,120,110,180,width=5,fill="white")#brazo1
                canvas.create_line(150,120,190,180,width=5,fill="white")#brazo2
                canvas.create_line(150,190,110,250,width=5,fill="white")#pierna1
            elif oportunidades==2:
                canvas.delete("all")
                canvas.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                canvas.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                canvas.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                canvas.create_line(150,110,150,190,width=5,fill="white")#torso
                canvas.create_line(150,120,110,180,width=5,fill="white")#brazo1
                canvas.create_line(150,120,190,180,width=5,fill="white")#brazo2
            elif oportunidades==3:
                canvas.delete("all")
                canvas.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                canvas.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                canvas.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                canvas.create_line(150,110,150,190,width=5,fill="white")#torso
                canvas.create_line(150,120,110,180,width=5,fill="white")#brazo1
            elif oportunidades==4:
                canvas.delete("all")
                canvas.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                canvas.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                canvas.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                canvas.create_line(150,110,150,190,width=5,fill="white")#torso
            elif oportunidades==5:
                canvas.delete("all")
                canvas.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                canvas.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                canvas.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
            else:
                canvas.delete("all")
                canvas.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                canvas.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
 
        else:
            if self.ObjetoJuego.getVictoria():
                canvas.delete("all")
                canvas.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                canvas.create_line(150,110,150,190,width=5,fill="white")#torso
                canvas.create_line(150,130,100,80,width=5,fill="white")#brazo1
                canvas.create_line(150,130,200,80,width=5,fill="white")#brazo2
                canvas.create_line(150,190,110,250,width=5,fill="white")#pierna1
                canvas.create_line(150,190,190,250,width=5,fill="white")#pierna2
            else:
                canvas.delete("all")
                canvas.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                canvas.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                canvas.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                canvas.create_line(150,110,150,190,width=5,fill="white")#torso
                canvas.create_line(150,120,110,180,width=5,fill="white")#brazo1
                canvas.create_line(150,120,190,180,width=5,fill="white")#brazo2
                canvas.create_line(150,190,110,250,width=5,fill="white")#pierna1
                canvas.create_line(150,190,190,250,width=5,fill="white")#pierna2



if __name__=="__main__":a=JuegoTk()