from asistente import AsistenteVoz


class Aprendizaje(AsistenteVoz):

    def __init__(self):
        # Llama al constructor de la clase base (AsistenteVoz)
        super().__init__()
        print("...probando aprendizaje")

    def ejecutar(self):
        print("Hola mundo")
        self.texto_a_audio("Hola mundo")
        #self.capturar_voz();




#Para ejecutar sin necesidad de usar project.py
prueba = Aprendizaje()
prueba.ejecutar()