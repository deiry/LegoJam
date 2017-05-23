from BrickPi import *
import curses,time
import threading

BrickPiSetup()
#B motor izquierdo
B = PORT_B
#D motor derecho
D = PORT_D
#C disparar
C = PORT_C
#s1 sensor
S1 = PORT_1

BrickPi.MotorEnable[D] = 1
BrickPi.MotorEnable[B] = 1
BrickPi.MotorEnable[C] = 1
BrickPi.SensorType[S1] = TYPE_SENSOR_EV3_COLOR_M2
#BrickPi.SensorType[S1] = TYPE_SENSOR_COLOR_FULL

def main():
   
st = curses.initscr()
  curses.cbreak()
  st.keypad(1)
  key =' '

  while key != ord('q'):
   
  key = st.getch()
  BrickPi.MotorSpeed[D] = 0
  BrickPi.MotorSpeed[B] = 0
  BrickPi.MotorSpeed[C] = 0
  st.refresh()

  #tecla flecha izquierda - el robot gira a la izquierda
  if key == curses.KEY_LEFT :
  print "izq"
  BrickPi.MotorSpeed[D] = 80
  BrickPi.MotorSpeed[B] = -30

  #tecla flecha derecha - el robot gira a la derecha
  if key == curses.KEY_RIGHT :
  print "dere"
  BrickPi.MotorSpeed[D] = -30
  BrickPi.MotorSpeed[B] = 80

  #tecla flecha arriba - el robot se mueve hacia adelante
  if key == curses.KEY_UP :
  BrickPi.MotorSpeed[D] = 120
  BrickPi.MotorSpeed[B] = 120

  #tecla flecha abajo - el robot se mueve en reversa
  if key == curses.KEY_DOWN :
  print "Atras"
  BrickPi.MotorSpeed[D] = -100
  BrickPi.MotorSpeed[B] = -100

  #tecla borrar - el robot entra en modo automatico  
  if key == curses.KEY_BACKSPACE:
  print("Presionno automatico")
  modoAutomatico()

  #tecla d - el robot entra en modo disparo
  if key == ord('d'):
  print ("Modo disparo")
  modoDisparo()
   
  time.sleep(0.01)
  BrickPiUpdateValues()

#funcion de python para el modo disparo
def modoDisparo():
  print ("Modo disparo")
  st = curses.initscr()
  curses.cbreak()
  st.keypad(1)
  key =' '
  while key != ord('q'):
   
  key = st.getch()
  BrickPi.MotorSpeed[D] = 0
  BrickPi.MotorSpeed[B] = 0
  BrickPi.MotorSpeed[C] = 0
  st.refresh()  
   
  #tecla flecha izquierda - el robot gira a la izquierda
  if key == curses.KEY_LEFT :
  print "izq"
  BrickPi.MotorSpeed[D] = 20
  BrickPi.MotorSpeed[B] = -20

  #tecla flecha derecha - el robot gira a la derecha
  if key == curses.KEY_RIGHT :
  print "dere"
  BrickPi.MotorSpeed[D] = -20
  BrickPi.MotorSpeed[B] = 20

  #tecla flecha arriba - el robot se mueve hacia adelante  
  if key == curses.KEY_UP :
  BrickPi.MotorSpeed[D] = 20
  BrickPi.MotorSpeed[B] = 20

  #tecla flecha atras - el robot se mueve en reversa
  if key == curses.KEY_DOWN :
  print "Atras"
  BrickPi.MotorSpeed[D] = -20
  BrickPi.MotorSpeed[B] = -20

  #tecla borrar - el robot dispara  
  if key == curses.KEY_BACKSPACE:
  BrickPi.MotorSpeed[C] = 110

   
  time.sleep(0.01)
  BrickPiUpdateValues()

#función modo Automático
def modoAutomatico():
  print("Entro automatico")
  BrickPiSetupSensors()
  control = True
  rango = 20
  ciclo = True
  while ciclo:
   
  BrickPiUpdateValues()
  color_sensor = BrickPi.Sensor[S1]
  contador = 0
  print(color_sensor)
  ciclo = validarColorRojo(color_sensor)
   
  #si detecta negro pone los motores a 80 de velocidad  
  if( color_sensor ==1):
  BrickPi.MotorSpeed[D] = 80
  BrickPi.MotorSpeed[B] = 80
  rango=20
   
  if(color_sensor != 1):
  if( color_sensor != 1 and control == True):
  while contador < 50:
  BrickPi.MotorSpeed[D] = -rango
  BrickPi.MotorSpeed[B] = rango
  #print (control)
  contador = contador +1
  time.sleep(0.01)
  BrickPiUpdateValues()
  color_sensor = BrickPi.Sensor[S1]
  if (contador%13 == 0):
  rango = rango +5
  if(color_sensor==1):
  contador=50
  ciclo = validarColorRojo(color_sensor)
  control = False
   
   
  else:
  while contador < 50:
  BrickPi.MotorSpeed[D] = rango
  BrickPi.MotorSpeed[B] = -rango  
  contador = contador +1
  time.sleep(0.01)
  BrickPiUpdateValues()
  color_sensor = BrickPi.Sensor[S1]
  if (contador%13 == 0):
  rango = rango +5
  if(color_sensor==1):
  contador=50
  ciclo = validarColorRojo(color_sensor)
  control = True


  time.sleep(0.008)
  
 	BrickPiUpdateValues() 
 time.sleep(.01)
  
def validarColorRojo(color):
  print(color)
  if (color == 5):
  BrickPi.MotorSpeed[D] = 0
 	BrickPi.MotorSpeed[B] = 0
  return False
  else:
  return True

if _name_ == "__main__":
  main()
