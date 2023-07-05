class Cliente:
    def __init__(self, tipo, estado, horaLlegada, acumTiempoEsperaCola):
        self.tipo = tipo
        self.estado = estado
        self.horaLlegada = horaLlegada
        self.acumTiempoEsperaCola = acumTiempoEsperaCola

    def calcularTiempoEspera(self, horaActual):
        self.acumTiempoEsperaCola = horaActual - self.horaLlegada
