#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import spidev #importa��o da biblioteca spi para uso de circuitos integrados no sistema
import time   #importa��o da biblioteca de tempo para controle de ciclos
import urllib3 #chamando a biblioteca urllib3 para comunica��o HTTP IoT com THINGSPEAK
from gpiozero import MCP3008 #importando MCP3008 Biblioteca de controle do Circuito Integrado

chave = '6WY5EI84DOSZS7XU' #defini��o fixa da chave API para leitura e envio de dados via THINGSPEAK 
url = 'https://api.thingspeak.com/update?api_key={}&field1={}&field2={}' #defini��o de url com string

#instancia a classe que usaremos
spi = spidev.SpiDev() #chamada a classe biblioteca spi para uso de circuitos externos
#abre e seta valores ao objeto
spi.open(0, 0)
spi.max_speed_hz=1000000

#metodo que le o valor recebido no CI MCP3008
def leradc(adcnum):
# le o dado do SPI do MCP3008, que devera estar no intervalo de 8 digitos
# 0 a 7 
    if adcnum > 7 or adcnum < 0: #intervalo de 0 a 8 bits
        return -1 #caso n�o esteja em intervalo zera.

#etapa que faz a conversao dos dados lidos de analogico para digital
    r = spi.xfer2([1, 8 + adcnum << 4, 0]) #etapa espec�fica da classe spidev
    adc_saida = ((r[1] & 3) << 8) + r[2]
    return adc_saida #fechamento de ciclo p�s leitura


while True:
    #chama o metodo ler ADC no pino 0 (temos 8 pinos)
    #e atribui o retorno a variavel valor
    valor = leradc(0) #pino ADC vai de 0 a 7, sendo 8 pinos dispon�veis no CI
    #verifica a quantos volts equivale a leitura do conversor
    #sendo 0v = 0 ohms, zero porcento de g�s, zero graus celcius, zero absoluto para a medida usada
    #e 3.3v = 100 graus celcius, 100ohms , 100mpa de press�o
    volts = (valor * 3.3) / 1024
    #converte o valor em volts calculado em temperatura, graus, resist�ncia
    resistencia = volts / (10.0 / 10000)
    
    urllib3.PoolManager().request('GET',url.format(chave,volts,resistencia))  #chamando o link API do THINGSPEAK por string, para limpeza do c�digo

    #print ("Valor da leitura%4d/1023 => Volts %5.3f V => resist�ncia %4.1f °C" % (valor, volts, temperatura))
    print("---------------------------")
    print ("Valor da leitura%4d/1023" % (valor))
    print ("Volts %5.3f V" % (volts))
    print ("resistencia %4.1f ohms" % (resistencia))
    

    time.sleep(15)
