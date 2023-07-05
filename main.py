from PyQt5.QtWidgets import *
from ui_tp4 import *
import sys
from generadores.exponencial import *
from generadores.uniforme import *
from generadores.cliente import *


class AppWin(QMainWindow, Ui_MainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        self.setupUi(self)  # Se genera la interfaz llamando al metodo setupUi

    def tipoCliente(self, rnd):
        if (rnd <= 0.44):
            tipo = "ventanilla salida inmediata cercania"
        elif (rnd <= 0.49):
            tipo = "maquina expendedora salida inmediata cercania"
        elif (rnd <= 0.54):
            tipo = "maquina expendedora salida inmediata interprovincial"
        elif (rnd <= 0.79):
            tipo = "ventanilla salida inmediata interprovincial"
        elif (rnd <= 1):
            tipo = "venta anticipada"
        return tipo

    def generarExpNeg(self, reloj, media):
        rnd, exp = exponencial2(media)
        return rnd, exp, reloj+exp

    def generarUniforme(self, reloj, minimo, maximo):
        rnd, valor = uniforme2(minimo, maximo)
        return rnd, valor, reloj+valor

    def ordenarPrimero(self, val):
        return val[0]

    def determinarProximoEvento(self, proxEventos: list):
        proxEventos.sort(key=self.ordenarPrimero)
        hora, tipo = proxEventos[0]
        proxEventos.pop(0)
        return hora, tipo

    def limpiarCampos(self):

        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        
        self.lineEdit_7.setText("")
        
        self.lineEdit_16.setText("")
        self.lineEdit_19.setText("")
        self.lineEdit_18.setText("")
        # tiempoPromEsperaColas =

        self.lineEdit_20.setText("")
        self.lineEdit_21.setText("")
        self.lineEdit_22.setText("")

        self.lineEdit_3.setText("15")
        self.lineEdit_4.setText("24")
        self.lineEdit_5.setText("15")
        self.lineEdit_6.setText("6")
        self.lineEdit_8.setText("0.38")
        self.lineEdit_9.setText("1.76")
        self.lineEdit_10.setText("0.6")
        self.lineEdit_11.setText("0.75")
        self.lineEdit_12.setText("2")
        self.lineEdit_13.setText("2.4")
        self.lineEdit_14.setText("1.5")
        self.lineEdit_15.setText("2")
        self.tableWidget.setRowCount(0)

    def simulacion(self):

    
        cantSimulaciones = int(self.lineEdit.text())
        lineasAMostrar = int(self.lineEdit_2.text())
        lineasAMostrarDesde = int(self.lineEdit_7.text())
        horaInicioTraficoModerado = int(self.lineEdit_3.text())
        horaFinTraficoModerado = int(self.lineEdit_4.text())
        horaFinTraficoCritico = int(self.lineEdit_5.text())
        horaInicioTraficoCritico = int(self.lineEdit_6.text())
        llegadaPasajerosHModMinimo = float(self.lineEdit_8.text())
        llegadaPasajerosHModMaximo = float(self.lineEdit_9.text())
        llegadaPasajerosHCriticoExpNeg = float(self.lineEdit_10.text())
        finAtencionCercaniaVentanillaExpNeg = float(self.lineEdit_11.text())
        finAtencionCercaniaMaqDispExpNeg = float(self.lineEdit_12.text())
        finAtencionVentaAnticipadaVentanillaExpNeg = float(
            self.lineEdit_13.text())
        finAtencionInterprovincialVentanillaExpNeg = float(
            self.lineEdit_14.text())
        finAtencionInterprovincialMaqDispExpNeg = float(
            self.lineEdit_15.text())

        yaOcurrioFinDia = False
        indice = 0
        clientes = []
        horaLlegadaCliente = 0
        horaFinAtencionInmediataVentanilla1 = 0
        horaFinAtencionInmediataVentanilla2 = 0
        horaFinAtencionAnticipadaVentanilla1 = 0
        horaFinAtencionAnticipadaVentanilla2 = 0
        horaFinAtencionMaqDis = 0
        tipoCliente = ""

        # Eventos
        evento = "inicio"
        relojActual = 0
        relojAnterior = 0
        horaDia = 0
        proxEventos = []

        # Ventanilla venta anticipada
        colaVentaAnticipada = []
        estadoVentanillaVentaAnticipada1 = "libre"
        estadoVentanillaVentaAnticipada2 = "libre"

        # Maquina dispensadora
        colaMaquinaDispensadora = []
        estadoMaquinaDispensadora = "libre"

        # Ventanilla salida inmediata
        estadoVentanillaSalidaInmediata1 = "libre"
        estadoVentanillaSalidaInmediata2 = "libre"
        colaSalidaInmediata = []

        # contadores
        horaInicioTiempoLibreMaqDis = 0
        contadorColaSalidaInmediata = 0
        contadorColaVentaAnticipada = 0
        contadorColaMaqDisp = 0
        contadorAbandonoVentaAnticipada = 0
        contadorTotalClientes = 0
        contadorTotalVentaAnticipada = 0
        contadorClientesSimult = 0

        # ACUMULADORES
        acumuladorTiempoLibreMaquinaDispensadora = 0
        acumuladorTiempoEsperaColaSalidaInmediata = 0
        acumuladorTiempoEsperaColaVentaAnticipada = 0
        acumuladorTiempoEsperaColaMaquinaDispensadora = 0
        acumuladorTiempoEsperaColaGeneral = 0

        for j in range(cantSimulaciones):

            if (len(clientes) != 0):
                listaAuxCli = []
                listaAuxCola = []
                for i in range(len(clientes)):
                
                    if (clientes[i].estado == "en cola"):
                        espInicial = clientes[i].acumTiempoEsperaCola
                        clientes[i].calcularTiempoEspera(
                            relojActual)
                        acumuladorTiempoEsperaColaGeneral += clientes[i].acumTiempoEsperaCola - espInicial
                        if (clientes[i].tipo != "venta anticipada" or clientes[i].acumTiempoEsperaCola < 20):
                            listaAuxCli.append(clientes[i])
                        else:
                            contadorAbandonoVentaAnticipada += 1
                    else:
                        listaAuxCli.append(clientes[i])
                clientes = listaAuxCli 

                for i in range(len(colaVentaAnticipada)):
                    if colaVentaAnticipada[i].acumTiempoEsperaCola < 20:
                        listaAuxCola.append(colaVentaAnticipada[i])
                colaVentaAnticipada = listaAuxCola
                   
            if (estadoMaquinaDispensadora == "libre"):
                acumuladorTiempoLibreMaquinaDispensadora += relojActual - relojAnterior

            if (horaDia >= horaFinTraficoCritico * 60):
                estadoVentanillaSalidaInmediata2 = "deshabilitado"

            if (evento == "inicio"):
                estadoVentanillaSalidaInmediata2 = "libre"
                yaOcurrioFinDia = False
                horaDia = horaInicioTraficoCritico * 60
                rndHora, exp, horaLlegadaCliente = self.generarExpNeg(
                    relojActual, llegadaPasajerosHCriticoExpNeg)
                proxEventos.append((horaLlegadaCliente, "llegada cliente"))
                if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                    self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, rndHora, exp, horaLlegadaCliente, "", "", "", "", "", "", "", "", "", "", "", "", "", str(len(colaSalidaInmediata)), estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, str(len(colaVentaAnticipada)), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                # cambia los datos para la siguiente iteracion
                #relojActual, evento = self.determinarProximoEvento(proxEventos)

            elif (evento == "llegada cliente"):

                rndTipoCliente = random.random()
                tipoCliente = self.tipoCliente(rndTipoCliente)
                cli = Cliente(tipoCliente, "", relojActual, 0)
                horaDia += relojActual - relojAnterior
                if (tipoCliente == "ventanilla salida inmediata cercania" or tipoCliente == "ventanilla salida inmediata interprovincial"):
                    if (estadoVentanillaSalidaInmediata1 == "libre"):
                        cli.estado = "siendo atendido ventanilla inmediata 1"

                        if (tipoCliente == "ventanilla salida inmediata cercania"):

                            estadoVentanillaSalidaInmediata1 = "cercania"
                            rndHora, exp1, horaFinAtencionInmediataVentanilla1 = self.generarExpNeg(
                                relojActual, finAtencionCercaniaVentanillaExpNeg)
                            proxEventos.append(
                                (horaFinAtencionInmediataVentanilla1, "fin atencion inmediata en ventanilla"))

                        else:
                            estadoVentanillaSalidaInmediata1 = "interprovincial"
                            rndHora, exp1, horaFinAtencionInmediataVentanilla1 = self.generarExpNeg(
                                relojActual, finAtencionInterprovincialVentanillaExpNeg)
                            proxEventos.append(
                                (horaFinAtencionInmediataVentanilla1, "fin atencion inmediata en ventanilla"))

                        if (horaDia <= horaFinTraficoCritico * 60):
                            rndLlegada, exp, horaLlegadaCliente = self.generarExpNeg(
                                relojActual, llegadaPasajerosHCriticoExpNeg)
                        else:
                            rndLlegada, exp, horaLlegadaCliente = self.generarUniforme(
                                relojActual, llegadaPasajerosHModMinimo, llegadaPasajerosHModMaximo)

                        proxEventos.append(
                            (horaLlegadaCliente, "llegada cliente"))
                        clientes.append(cli)
                        contadorTotalClientes += 1

                        if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                            self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, rndLlegada, exp, horaLlegadaCliente, rndTipoCliente, tipoCliente, rndHora, exp1, horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                        "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                            colaSalidaInmediata),
                                        estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                            len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                        str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                    elif (estadoVentanillaSalidaInmediata2 == "libre"):
                        cli.estado = "siendo atendido ventanilla inmediata 2"

                        if (tipoCliente == "ventanilla salida inmediata cercania"):
                            estadoVentanillaSalidaInmediata2 = "cercania"
                            rndHora, exp1, horaFinAtencionInmediataVentanilla2 = self.generarExpNeg(
                                relojActual, finAtencionCercaniaVentanillaExpNeg)
                            proxEventos.append(
                                (horaFinAtencionInmediataVentanilla2, "fin atencion inmediata en ventanilla"))

                        else:
                            estadoVentanillaSalidaInmediata2 == "interprovincial"
                            rndHora, exp1, horaFinAtencionInmediataVentanilla2 = self.generarExpNeg(
                                relojActual, finAtencionInterprovincialVentanillaExpNeg)
                            proxEventos.append(
                                (horaFinAtencionInmediataVentanilla2, "fin atencion inmediata en ventanilla"))

                        if (horaDia <= horaFinTraficoCritico * 60):
                            rndLlegada, exp, horaLlegadaCliente = self.generarExpNeg(
                                relojActual, llegadaPasajerosHCriticoExpNeg)
                        else:
                            rndLlegada, exp, horaLlegadaCliente = self.generarUniforme(
                                relojActual, llegadaPasajerosHModMinimo, llegadaPasajerosHModMaximo)

                        proxEventos.append(
                            (horaLlegadaCliente, "llegada cliente"))
                        clientes.append(cli)
                        contadorTotalClientes += 1

                        if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                            self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, rndLlegada, exp, horaLlegadaCliente, rndTipoCliente, tipoCliente, rndHora, exp1, horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                        "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                            colaSalidaInmediata),
                                        estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                            len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                        str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                    else:
                        cli.estado = "en cola"
                        colaSalidaInmediata.append(cli)
                        if (contadorColaSalidaInmediata < len(colaSalidaInmediata)):
                            contadorColaSalidaInmediata = len(
                                colaSalidaInmediata)

                        if (horaDia <= horaFinTraficoCritico * 60):
                            rndLlegada, exp, horaLlegadaCliente = self.generarExpNeg(
                                relojActual, llegadaPasajerosHCriticoExpNeg)
                        else:
                            rndLlegada, exp, horaLlegadaCliente = self.generarUniforme(
                                relojActual, llegadaPasajerosHModMinimo, llegadaPasajerosHModMaximo)

                        proxEventos.append(
                            (horaLlegadaCliente, "llegada cliente"))
                        clientes.append(cli)
                        contadorTotalClientes += 1
                        if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                            self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, rndLlegada, exp, horaLlegadaCliente, rndTipoCliente, tipoCliente, "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                        "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                            colaSalidaInmediata),
                                        estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                            len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                        str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                elif (tipoCliente == "venta anticipada"):
                    contadorTotalVentaAnticipada += 1
                    if (estadoVentanillaVentaAnticipada1 == "libre"):
                        cli.estado = "siendo atendido ventanilla anticipada 1"
                        estadoVentanillaVentaAnticipada1 = "ocupado"
                        rndHora, exp1, horaFinAtencionAnticipadaVentanilla1 = self.generarExpNeg(
                            relojActual, finAtencionVentaAnticipadaVentanillaExpNeg)
                        proxEventos.append(
                            (horaFinAtencionAnticipadaVentanilla1, "fin atencion venta anticipada"))

                        if (horaDia <= horaFinTraficoCritico * 60):
                            rndLlegada, exp, horaLlegadaCliente = self.generarExpNeg(
                                relojActual, llegadaPasajerosHCriticoExpNeg)
                        else:
                            rndLlegada, exp, horaLlegadaCliente = self.generarUniforme(
                                relojActual, llegadaPasajerosHModMinimo, llegadaPasajerosHModMaximo)

                        proxEventos.append(
                            (horaLlegadaCliente, "llegada cliente"))
                        clientes.append(cli)
                        contadorTotalClientes += 1
                        if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                            self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, rndLlegada, exp, horaLlegadaCliente, rndTipoCliente, tipoCliente, "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                        "", "", horaFinAtencionMaqDis, rndHora, exp1, horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                            colaSalidaInmediata),
                                        estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                            len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                        str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                    elif (estadoVentanillaVentaAnticipada2 == "libre"):
                        cli.estado = "siendo atendido ventanilla anticipada 2"
                        estadoVentanillaVentaAnticipada2 = "ocupado"
                        rndHora, exp1, horaFinAtencionAnticipadaVentanilla2 = self.generarExpNeg(
                            relojActual, finAtencionVentaAnticipadaVentanillaExpNeg)
                        proxEventos.append(
                            (horaFinAtencionAnticipadaVentanilla2, "fin atencion venta anticipada"))

                        if (horaDia <= horaFinTraficoCritico * 60):
                            rndLlegada, exp, horaLlegadaCliente = self.generarExpNeg(
                                relojActual, llegadaPasajerosHCriticoExpNeg)
                        else:
                            rndLlegada, exp, horaLlegadaCliente = self.generarUniforme(
                                relojActual, llegadaPasajerosHModMinimo, llegadaPasajerosHModMaximo)

                        proxEventos.append(
                            (horaLlegadaCliente, "llegada cliente"))
                        clientes.append(cli)
                        contadorTotalClientes += 1

                        if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                            self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, rndLlegada, exp, horaLlegadaCliente, rndTipoCliente, tipoCliente, "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                        "", "", horaFinAtencionMaqDis, rndHora, exp1, horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                            colaSalidaInmediata),
                                        estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                            len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                        str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                    else:
                        cli.estado = "en cola"
                        colaVentaAnticipada.append(cli)
                        if (contadorColaVentaAnticipada < len(colaVentaAnticipada)):
                            contadorColaVentaAnticipada = len(
                                colaVentaAnticipada)

                        if (horaDia <= horaFinTraficoCritico * 60):
                            rndLlegada, exp, horaLlegadaCliente = self.generarExpNeg(
                                relojActual, llegadaPasajerosHCriticoExpNeg)
                        else:
                            rndLlegada, exp, horaLlegadaCliente = self.generarUniforme(
                                relojActual, llegadaPasajerosHModMinimo, llegadaPasajerosHModMaximo)

                        proxEventos.append(
                            (horaLlegadaCliente, "llegada cliente"))
                        clientes.append(cli)
                        contadorTotalClientes += 1
                        if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                            self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, rndLlegada, exp, horaLlegadaCliente, rndTipoCliente, tipoCliente, "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                        "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                            colaSalidaInmediata),
                                        estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                            len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                        str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                elif (tipoCliente == "maquina expendedora salida inmediata cercania" or tipoCliente == "maquina expendedora salida inmediata interprovincial"):
                    if (estadoMaquinaDispensadora == "libre"):
                        cli.estado = "siendo atendido maquina dispensadora"
                        estadoMaquinaDispensadora = "ocupado"
                        rndHora, exp1, horaFinAtencionMaqDis = self.generarExpNeg(
                            relojActual, finAtencionInterprovincialMaqDispExpNeg)
                        proxEventos.append(
                            (horaFinAtencionMaqDis, "fin atencion inmediata en maquina dispensadora"))

                        if (horaDia <= horaFinTraficoCritico * 60):
                            rndLlegada, exp, horaLlegadaCliente = self.generarExpNeg(
                                relojActual, llegadaPasajerosHCriticoExpNeg)
                        else:
                            rndLlegada, exp, horaLlegadaCliente = self.generarUniforme(
                                relojActual, llegadaPasajerosHModMinimo, llegadaPasajerosHModMaximo)
                        proxEventos.append(
                            (horaLlegadaCliente, "llegada cliente"))
                        clientes.append(cli)
                        contadorTotalClientes += 1

                        if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                            self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, rndLlegada, exp, horaLlegadaCliente, rndTipoCliente, tipoCliente, "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                        rndHora, exp1, horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                            colaSalidaInmediata),
                                        estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                            len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                        str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                    else:
                        cli.estado = "en cola"
                        colaMaquinaDispensadora.append(cli)
                        if (contadorColaMaqDisp < len(colaMaquinaDispensadora)):
                            contadorColaMaqDisp = len(colaMaquinaDispensadora)

                        if (horaDia <= horaFinTraficoCritico * 60):
                            rndLlegada, exp, horaLlegadaCliente = self.generarExpNeg(
                                relojActual, llegadaPasajerosHCriticoExpNeg)
                        else:
                            rndLlegada, exp, horaLlegadaCliente = self.generarUniforme(
                                relojActual, llegadaPasajerosHModMinimo, llegadaPasajerosHModMaximo)

                        proxEventos.append(
                            (horaLlegadaCliente, "llegada cliente"))
                        clientes.append(cli)
                        contadorTotalClientes += 1

                        if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                            self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, rndLlegada, exp, horaLlegadaCliente, rndTipoCliente, tipoCliente, "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                        "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                            colaSalidaInmediata),
                                        estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                            len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                        str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

            elif (evento == "fin atencion inmediata en ventanilla"):

                for i in range(len(clientes)):
                    if (horaFinAtencionInmediataVentanilla1 == relojActual):
                        if (clientes[i].estado == "siendo atendido ventanilla inmediata 1"):
                            indiceClienteABorrar = i

                    else:
                        if (clientes[i].estado == "siendo atendido ventanilla inmediata 2"):
                            # clientes.pop(i)
                            indiceClienteABorrar = i

                clientes.pop(indiceClienteABorrar)

                if (len(colaSalidaInmediata) == 0):
                    if (horaFinAtencionInmediataVentanilla1 == relojActual):
                        estadoVentanillaSalidaInmediata1 = "libre"
                        horaFinAtencionInmediataVentanilla1 = ""
                    else:
                        estadoVentanillaSalidaInmediata2 = "libre"
                        horaFinAtencionInmediataVentanilla2 = ""

                    if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                        self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, "", "", horaLlegadaCliente, "", "", "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                    "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                        colaSalidaInmediata),
                                    estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                        len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                    str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                else:
                    cliente = colaSalidaInmediata.pop(0)

                    if (horaFinAtencionInmediataVentanilla1 == relojActual):
                        cliente.estado = "siendo atendido ventanilla inmediata 1"
                        if (cliente.tipo == "ventanilla salida inmediata cercania"):
                            estadoVentanillaSalidaInmediata1 = "cercania"
                            rndHora, exp1, horaFinAtencionInmediataVentanilla1 = self.generarExpNeg(
                                relojActual, finAtencionCercaniaVentanillaExpNeg)

                        else:
                            estadoVentanillaSalidaInmediata1 = "interprovincial"
                            rndHora, exp1, horaFinAtencionInmediataVentanilla1 = self.generarExpNeg(
                                relojActual, finAtencionInterprovincialVentanillaExpNeg)

                        proxEventos.append(
                            (horaFinAtencionInmediataVentanilla1, "fin atencion inmediata en ventanilla"))
                    elif (estadoVentanillaSalidaInmediata2 == "deshabilitado"):
                        pass

                    else:
                        cliente.estado = "siendo atendido ventanilla inmediata 2"
                        if (cliente.tipo == "ventanilla salida inmediata cercania"):
                            estadoVentanillaSalidaInmediata2 = "cercania"
                            rndHora, exp1, horaFinAtencionInmediataVentanilla2 = self.generarExpNeg(
                                relojActual, finAtencionCercaniaVentanillaExpNeg)
                        else:
                            estadoVentanillaSalidaInmediata2 = "interprovincial"
                            rndHora, exp1, horaFinAtencionInmediataVentanilla2 = self.generarExpNeg(
                                relojActual, finAtencionInterprovincialVentanillaExpNeg)

                        proxEventos.append(
                            (horaFinAtencionInmediataVentanilla2, "fin atencion inmediata en ventanilla"))

                    if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                        self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, "", "", horaLlegadaCliente, "", "", rndHora, exp1, horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                    "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                        colaSalidaInmediata),
                                    estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                        len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                    str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

            elif (evento == "fin atencion inmediata en maquina dispensadora"):
                for i in range(len(clientes)):
                    if (clientes[i].estado == "siendo atendido maquina dispensadora"):
                        # clientes.pop(i)
                        indiceClienteABorrar = i
                clientes.pop(indiceClienteABorrar)

                if (len(colaMaquinaDispensadora) == 0):
                    estadoMaquinaDispensadora = "libre"
                    horaFinAtencionMaqDis = ""
                    if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                        self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, "", "", horaLlegadaCliente, "", "", "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                    "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                        colaSalidaInmediata),
                                    estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                        len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                    str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                else:
                    cliente = colaMaquinaDispensadora.pop(0)

                    cliente.estado = "siendo atendido maquina dispensadora"
                    if (cliente.tipo == "maquina expendedora salida inmediata cercania"):
                        rndHora, exp1, horaFinAtencionMaqDis = self.generarExpNeg(
                            relojActual, finAtencionCercaniaMaqDispExpNeg)
                    else:
                        rndHora, exp1, horaFinAtencionMaqDis = self.generarExpNeg(
                            relojActual, finAtencionInterprovincialMaqDispExpNeg)

                    proxEventos.append(
                        (horaFinAtencionMaqDis, "fin atencion inmediata en maquina dispensadora"))

                    if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                        self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, "", "", horaLlegadaCliente, "", "", "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                    rndHora, exp1, horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                        colaSalidaInmediata),
                                    estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                        len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                    str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

            elif (evento == "fin atencion venta anticipada"):
                for i in range(len(clientes)):
                    if (horaFinAtencionAnticipadaVentanilla1 == relojActual):
                        if (clientes[i].estado == "siendo atendido ventanilla anticipada 1"):
                            # clientes.pop(i)
                            indiceClienteABorrar = i

                    else:
                        if (clientes[i].estado == "siendo atendido ventanilla anticipada 2"):
                            # clientes.pop(i)
                            indiceClienteABorrar = i

                clientes.pop(indiceClienteABorrar)
                if (len(colaVentaAnticipada) == 0):
                    if (horaFinAtencionAnticipadaVentanilla1 == relojActual):
                        estadoVentanillaVentaAnticipada1 = "libre"
                        horaFinAtencionAnticipadaVentanilla1 = ""
                    else:
                        estadoVentanillaVentaAnticipada2 = "libre"
                        horaFinAtencionAnticipadaVentanilla2 = ""

                    if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                        self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, "", "", horaLlegadaCliente, "", "", "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                    "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                        colaSalidaInmediata),
                                    estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                        len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                    str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

                else:
                    cliente = colaVentaAnticipada.pop(0)

                    if (horaFinAtencionAnticipadaVentanilla1 == relojActual):
                        cliente.estado = "siendo atendido ventanilla anticipada 1"

                        rndHora, exp1, horaFinAtencionAnticipadaVentanilla1 = self.generarExpNeg(
                            relojActual, finAtencionVentaAnticipadaVentanillaExpNeg)

                        proxEventos.append(
                            (horaFinAtencionAnticipadaVentanilla1, "fin atencion venta anticipada"))

                    else:
                        cliente.estado = "siendo atendido ventanilla anticipada 2"

                        rndHora, exp1, horaFinAtencionAnticipadaVentanilla2 = self.generarExpNeg(
                            relojActual, finAtencionVentaAnticipadaVentanillaExpNeg)

                        proxEventos.append(
                            (horaFinAtencionAnticipadaVentanilla2, "fin atencion venta anticipada"))

                    if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                        self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, "", "", horaLlegadaCliente, "", "", "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                    "", "", horaFinAtencionMaqDis, rndHora, exp1, horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                        colaSalidaInmediata),
                                    estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                        len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                    str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

            elif (evento == "fin dia"):
                colaMaquinaDispensadora.clear()
                colaSalidaInmediata.clear()
                colaVentaAnticipada.clear()

                listaAuxClientes = []
                listaAuxEventos = []

                for i in range(len(clientes)):
                    if (clientes[i].estado != "en cola"):
                        listaAuxClientes.append(clientes[i])

                clientes = listaAuxClientes

                for i in range(len(proxEventos)):
                    hora, tipoEvento = proxEventos[i]
                    if (tipoEvento != "llegada cliente"):
                        listaAuxEventos.append(proxEventos[i])

                proxEventos = listaAuxEventos

                horaLlegadaCliente = ""
                relojUltimo, a = proxEventos[-1]
                proxEventos.append((relojUltimo + 0.01, "inicio"))
                if (lineasAMostrarDesde <= indice and indice <= lineasAMostrarDesde + lineasAMostrar):
                    self.cargar(indice - lineasAMostrarDesde, j, evento, relojActual, horaDia, "", "", "", "", "", "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                                "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                                    colaSalidaInmediata),
                                estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                                    len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                                str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

            elif (evento == "inicio dia"):
                horaDia = horaInicioTraficoCritico * 60
                rndLlegada, exp, horaLlegadaCliente = self.generarExpNeg(
                    relojActual, llegadaPasajerosHCriticoExpNeg)
                proxEventos.append((horaLlegadaCliente, "llegada cliente"))
                yaOcurrioFinDia = False

            if (horaDia > horaFinTraficoModerado * 60 and not yaOcurrioFinDia):
                proxEventos.append((relojActual, "fin dia"))
                yaOcurrioFinDia = True

            indice += 1
            # print(indice)
            # print(evento)
            # print(tipoCliente)
            # print(relojActual)
            # if (j > 1):
            #     print(cli.estado)
            # print(len(colaMaquinaDispensadora))
            # print(len(colaSalidaInmediata))
            # print(len(colaVentaAnticipada))
            # print()
            relojAnterior = relojActual
            relojActual, evento = self.determinarProximoEvento(proxEventos)

            # if (contadorClientesSimult < len(clientes)):
            #     contadorClientesSimult = len(clientes)
            # print(contadorClientesSimult)

        # FIN DE SIMULACION
        self.cargar(self.tableWidget.rowCount(), j, "FIN SIMULACION", relojActual, horaDia, rndLlegada, exp, horaLlegadaCliente, rndTipoCliente, tipoCliente, "", "", horaFinAtencionInmediataVentanilla1, horaFinAtencionInmediataVentanilla2,
                    "", "", horaFinAtencionMaqDis, "", "", horaFinAtencionAnticipadaVentanilla1, horaFinAtencionAnticipadaVentanilla2, len(
                        colaSalidaInmediata),
                    estadoVentanillaSalidaInmediata1, estadoVentanillaSalidaInmediata2, len(colaVentaAnticipada), estadoVentanillaVentaAnticipada1, estadoVentanillaVentaAnticipada2, str(
                        len(colaMaquinaDispensadora)), estadoMaquinaDispensadora, str(horaInicioTiempoLibreMaqDis),
                    str(contadorColaSalidaInmediata), str(contadorColaVentaAnticipada), str(contadorColaMaqDisp), str(contadorTotalClientes), str(contadorTotalVentaAnticipada), str(contadorAbandonoVentaAnticipada), str(acumuladorTiempoLibreMaquinaDispensadora), str(acumuladorTiempoEsperaColaGeneral), clientes)

        tiempoPromedioEsperaCola = acumuladorTiempoEsperaColaGeneral / contadorTotalClientes

        # MODIFICAR LA UI, PONER LABEL Y LINEEDIT PARA CADA COLA
        cantMaxClientesColaInmediata = contadorColaSalidaInmediata
        cantMaxClientesColaAnticipada = contadorColaVentaAnticipada
        cantMaxClientesColaMaqDisp = contadorColaMaqDisp

        porcentajeAbandonoVentaAnticipada = contadorAbandonoVentaAnticipada / \
            contadorTotalVentaAnticipada * 100

        porcentajeTiempoLibreMaquinaDispensadora = acumuladorTiempoLibreMaquinaDispensadora / relojActual * 100

        self.lineEdit_16.setText(str(tiempoPromedioEsperaCola))
        self.lineEdit_19.setText(str(porcentajeTiempoLibreMaquinaDispensadora))
        self.lineEdit_18.setText(str(porcentajeAbandonoVentaAnticipada))
        # tiempoPromEsperaColas =

        self.lineEdit_20.setText(str(cantMaxClientesColaInmediata))
        self.lineEdit_21.setText(str(cantMaxClientesColaAnticipada))
        self.lineEdit_22.setText(str(cantMaxClientesColaMaqDisp))

    
        

    def cargar(self, indice, iteracion, evento, reloj, horaDia, rndLlegada, tiempoLlegada, horaLlegadaProxPasajero, rndTipoCliente, tipoCliente, rndFinAtencionInmediataEnVentanilla, tiempoFinAtencionInmediataVent, finAtencionInmediataVent1, finAtencionInmediataVent2, RNDFinAtencionInmediataMaqDis, tiempoFinAtencionInmediataMaqDis,
               finAtencionInmediataMaqDis, rndFinAtencionVentaAnticipadaVentanilla, tiempoFinAtencionVentaAnticipadaVentanilla, finAtencionVentaAnticipadaVentanilla1, finAtencionVentaAnticipadaVentanilla2,
               colaVentanillaSalidaInmediata, estadoVentanillaInmediata1, estadoVentanillaInmediata2, colaVentanillaAnticipada, estadoVentanillaAnticipada1, estadoVentanillaAnticipada2, colaMaqDis, estadoMaqDis, horaInicioTiempoLibreMaqDis,
               maxColaSalidaInmediata, maxColaVentaAnticipada, maxColaMaqDis, contadorTotalClientes, contadorTotalClientesVentaAnticipada, contadorTotalAbandonoVtaAnticipada, acumTiempoLibreMaqDis, acumTiempoEsperaCola, clientes):
        # clientes
        self.tableWidget.insertRow(indice)
        self.tableWidget.setItem(
            indice, 0, QtWidgets.QTableWidgetItem(str(iteracion)))
        self.tableWidget.setItem(
            indice, 1, QtWidgets.QTableWidgetItem(str(evento)))
        self.tableWidget.setItem(
            indice, 2, QtWidgets.QTableWidgetItem(str(reloj)))
        self.tableWidget.setItem(
            indice, 3, QtWidgets.QTableWidgetItem(str(horaDia / 60)))
        self.tableWidget.setItem(
            indice, 4, QtWidgets.QTableWidgetItem(str(rndLlegada)))
        self.tableWidget.setItem(
            indice, 5, QtWidgets.QTableWidgetItem(str(tiempoLlegada)))
        self.tableWidget.setItem(
            indice, 6, QtWidgets.QTableWidgetItem(str(horaLlegadaProxPasajero)))
        self.tableWidget.setItem(
            indice, 7, QtWidgets.QTableWidgetItem(str(rndTipoCliente)))
        self.tableWidget.setItem(
            indice, 8, QtWidgets.QTableWidgetItem(str(tipoCliente)))
        self.tableWidget.setItem(indice, 9, QtWidgets.QTableWidgetItem(
            str(rndFinAtencionInmediataEnVentanilla)))
        self.tableWidget.setItem(indice, 10, QtWidgets.QTableWidgetItem(
            str(tiempoFinAtencionInmediataVent)))
        self.tableWidget.setItem(indice, 11, QtWidgets.QTableWidgetItem(
            str(finAtencionInmediataVent1)))
        self.tableWidget.setItem(indice, 12, QtWidgets.QTableWidgetItem(
            str(finAtencionInmediataVent2)))
        self.tableWidget.setItem(indice, 13, QtWidgets.QTableWidgetItem(
            str(RNDFinAtencionInmediataMaqDis)))
        self.tableWidget.setItem(indice, 14, QtWidgets.QTableWidgetItem(
            str(tiempoFinAtencionInmediataMaqDis)))
        self.tableWidget.setItem(indice, 15, QtWidgets.QTableWidgetItem(
            str(finAtencionInmediataMaqDis)))
        self.tableWidget.setItem(indice, 16, QtWidgets.QTableWidgetItem(
            str(rndFinAtencionVentaAnticipadaVentanilla)))
        self.tableWidget.setItem(indice, 17, QtWidgets.QTableWidgetItem(
            str(tiempoFinAtencionVentaAnticipadaVentanilla)))
        self.tableWidget.setItem(indice, 18, QtWidgets.QTableWidgetItem(
            str(finAtencionVentaAnticipadaVentanilla1)))
        self.tableWidget.setItem(indice, 19, QtWidgets.QTableWidgetItem(
            str(finAtencionVentaAnticipadaVentanilla2)))
        self.tableWidget.setItem(indice, 20, QtWidgets.QTableWidgetItem(
            str(colaVentanillaSalidaInmediata)))
        self.tableWidget.setItem(indice, 21, QtWidgets.QTableWidgetItem(
            str(estadoVentanillaInmediata1)))
        self.tableWidget.setItem(indice, 22, QtWidgets.QTableWidgetItem(
            str(estadoVentanillaInmediata2)))
        self.tableWidget.setItem(
            indice, 23, QtWidgets.QTableWidgetItem(str(colaVentanillaAnticipada)))
        self.tableWidget.setItem(indice, 24, QtWidgets.QTableWidgetItem(
            str(estadoVentanillaAnticipada1)))
        self.tableWidget.setItem(indice, 25, QtWidgets.QTableWidgetItem(
            str(estadoVentanillaAnticipada2)))
        self.tableWidget.setItem(
            indice, 26, QtWidgets.QTableWidgetItem(str(colaMaqDis)))
        self.tableWidget.setItem(
            indice, 27, QtWidgets.QTableWidgetItem(str(estadoMaqDis)))
        self.tableWidget.setItem(indice, 28, QtWidgets.QTableWidgetItem(
            str(horaInicioTiempoLibreMaqDis)))
        self.tableWidget.setItem(
            indice, 29, QtWidgets.QTableWidgetItem(str(maxColaSalidaInmediata)))
        self.tableWidget.setItem(
            indice, 30, QtWidgets.QTableWidgetItem(str(maxColaVentaAnticipada)))
        self.tableWidget.setItem(
            indice, 31, QtWidgets.QTableWidgetItem(str(maxColaMaqDis)))
        self.tableWidget.setItem(
            indice, 32, QtWidgets.QTableWidgetItem(str(contadorTotalClientes)))
        self.tableWidget.setItem(indice, 33, QtWidgets.QTableWidgetItem(
            str(contadorTotalClientesVentaAnticipada)))
        self.tableWidget.setItem(indice, 34, QtWidgets.QTableWidgetItem(
            str(contadorTotalAbandonoVtaAnticipada)))
        self.tableWidget.setItem(
            indice, 35, QtWidgets.QTableWidgetItem(str(acumTiempoLibreMaqDis)))
        self.tableWidget.setItem(indice, 36, QtWidgets.QTableWidgetItem(
            str(acumTiempoEsperaCola)))

        for i in range(5):
            if (i <= len(clientes)-1):
                self.tableWidget.setItem(
                    indice, 37+i*4, QtWidgets.QTableWidgetItem(str(clientes[i].tipo)))
                self.tableWidget.setItem(
                    indice, 38+i*4, QtWidgets.QTableWidgetItem(str(clientes[i].estado)))
                self.tableWidget.setItem(
                    indice, 39+i*4, QtWidgets.QTableWidgetItem(str(clientes[i].horaLlegada)))
                self.tableWidget.setItem(
                    indice, 40+i*4, QtWidgets.QTableWidgetItem(str(clientes[i].acumTiempoEsperaCola)))


if __name__ == '__main__':
    app = QApplication(sys.argv)  # create an instance of the application
    appWin = AppWin()  # create an instance of a window
    appWin.show()  # to make the window visible
    app.exec()  # to start up the event loop
    app = QApplication(sys.argv)  # create an instance of the application
    appWin = AppWin()  # create an instance of a window
    appWin.show()  # to make the window visible
    app.exec()  # to start up the event loop
