#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import spidev #importação da biblioteca spi para uso de circuitos integrados no sistema
import time   #importação da biblioteca de tempo para controle de ciclos
import urllib3 #chamando a biblioteca urllib3 para comunicação HTTP IoT com THINGSPEAK
from gpiozero import MCP3008 #importando MCP3008 Biblioteca de controle do Circuito Integrado

chave = '6WY5EI84DOSZS7XU' #definição fixa da chave API para leitura e envio de dados via THINGSPEAK 
url = 'https://api.thingspeak.com/update?api_key={}&field1={}&field2={}' #definição de url com string

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
        return -1 #caso não esteja em intervalo zera.

#etapa que faz a conversao dos dados lidos de analogico para digital
    r = spi.xfer2([1, 8 + adcnum << 4, 0]) #etapa específica da classe spidev
    adc_saida = ((r[1] & 3) << 8) + r[2]
    return adc_saida #fechamento de ciclo pós leitura


while True:
    #chama o metodo ler ADC no pino 0 (temos 8 pinos)
    #e atribui o retorno a variavel valor
    valor = leradc(0) #pino ADC vai de 0 a 7, sendo 8 pinos disponíveis no CI
    #verifica a quantos volts equivale a leitura do conversor
    #sendo 0v = 0 ohms, zero porcento de gás, zero graus celcius, zero absoluto para a medida usada
    #e 3.3v = 100 graus celcius, 100ohms , 100mpa de pressão
    volts = (valor * 3.3) / 1024
    #converte o valor em volts calculado em temperatura, graus, resistência
    resistencia = volts / (10.0 / 10000)
    
    urllib3.PoolManager().request('GET',url.format(chave,volts,resistencia))  #chamando o link API do THINGSPEAK por string, para limpeza do código

    #print ("Valor da leitura%4d/1023 => Volts %5.3f V => resistência %4.1f Â°C" % (valor, volts, temperatura))
    print("---------------------------")
    print ("Valor da leitura%4d/1023" % (valor))
    print ("Volts %5.3f V" % (volts))
    print ("resistencia %4.1f ohms" % (resistencia))
    

    time.sleep(15)
