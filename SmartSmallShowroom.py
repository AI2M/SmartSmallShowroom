import RPi.GPIO as io
import pygame
import time 
from time import sleep
import smbus



io.setmode(io.BCM)
pygame.mixer.init()

#------------------------------------#Start Define Display
# Define some device parameters
I2C_ADDR  = 0x3f # I2C device address, if any error, change this address to 0x27
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
def lcd_clear():
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
def lcd_string_slide(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    if(line>15):
      lcd_byte(ord(message[i-15]),LCD_CHR-5)
      
    
#------------------------------------#End Define Display

Btn = [12,16,20,21] #4pin D C B A
Btn2 = [8,7] #2pin A B
LEDOutput = [11,9,10,22,27] #5pin 
LedControl = 23 #1pin
MotorOutput = [26,5,6,13,19] #5pin en A0 A1 A2 A3 
MotorControl = [17,4,14,15] #4pin
Sensor = 18 #1pin 
#total = 22 pin 
#free = 4 pin


stateButton = 0
last_stateButton = 1
stateButton2 = 0
last_stateButton2 = 1
stateMusic =-1
ItemNumber = ""
ItemRef = ["0","8","08","8888","8080","8000","0008","0088","8008"]
lcd_init()

for i in range(len(Btn)):
    io.setup(Btn[i], io.IN)

for j in range(len(Btn2)):
    io.setup(Btn2[j], io.IN)

for k in range(len(MotorControl)):
  io.setup(MotorControl[k], io.OUT)

for l in range(len(MotorOutput)):
  io.setup(MotorOutput[l], io.OUT)


def Stepper_control():
  
  io.output(MotorControl[0],1)
  io.output(MotorControl[1],1)
  io.output(MotorControl[2],0)
  io.output(MotorControl[3],0)
  sleep(0.003)
  io.output(MotorControl[0],0)
  io.output(MotorControl[1],1)
  io.output(MotorControl[2],1)
  io.output(MotorControl[3],0)
  sleep(0.003)
  io.output(MotorControl[0],0)
  io.output(MotorControl[1],0)
  io.output(MotorControl[2],1)
  io.output(MotorControl[3],1)
  sleep(0.003)
  io.output(MotorControl[0],1)
  io.output(MotorControl[1],0)
  io.output(MotorControl[2],0)
  io.output(MotorControl[3],1)
  sleep(0.003)

def Stepper_output(a,b,c,d):
    io.output(MotorOutput[0],0)
    io.output(MotorOutput[1],a)
    io.output(MotorOutput[2],b)
    io.output(MotorOutput[3],c)
    io.output(MotorOutput[4],d)

#ItemRef = ["0","8","08","8888","8080","8000","0008","0088","8008"]
def Mapping(ItemNumber):
  if(ItemNumber == ItemRef[0]):
    Stepper_output(0,0,0,0)#y0
    print("y0")
    
  elif(ItemNumber == ItemRef[1]):
    Stepper_output(0,0,0,1)#y130
    print("y1")
    
  elif(ItemNumber == ItemRef[2]):
    Stepper_output(0,0,1,0)#y2
    print("y2")
    
  elif(ItemNumber == ItemRef[3]):
    Stepper_output(0,0,1,1)#y3
    print("y3")
      
  elif(ItemNumber == ItemRef[4]):
    Stepper_output(0,1,0,0)#y4
    print("y4")
      
  elif(ItemNumber == ItemRef[5]):
    Stepper_output(0,1,0,1)#y5
    print("y5")
      
  elif(ItemNumber == ItemRef[6]):
    Stepper_output(0,1,1,0)#y6
    print("y6")
      
  elif(ItemNumber == ItemRef[7]):
    Stepper_output(0,1,1,1)#y7
    print("y7")
      
  elif(ItemNumber == ItemRef[8]):
    Stepper_output(1,0,0,0)#y8
    print("y8")
      
  else:
    io.output(MotorOutput[0],1)
    
 
def play_music(Position):
    try:
        pygame.mixer.music.load("music"+str(Position)+".mp3")
        pygame.mixer.music.play()
        print("now, playing music"+str(Position)+".mp3")
        lcd_string("Playing",LCD_LINE_1)
        lcd_string("music"+str(Position)+".mp3",LCD_LINE_2)
        motoron = 1
        
    except :
        pygame.mixer.music.stop()
        print("no music"+str(Position)+".mp3")
        lcd_string("no music"+str(Position)+".mp3",LCD_LINE_1)
        lcd_string("Try Again",LCD_LINE_2)
        sleep(2)
        motoron = 0
        pass
    stateButton = 1


io.output(MotorOutput[0],1)    
while True:
    
    inputBi = ""
    input2Bi = ""
    Stepper_control()
    for i in range(len(Btn)):
        inputBi +=(str(io.input(Btn[i])))
    for j in range(len(Btn2)):
        input2Bi +=(str(io.input(Btn2[j])))
        
    inputDec = 14-int(inputBi,2)
    input2Dec = 11-int(input2Bi,2)

    if(inputDec !=-1 and stateButton==0):
        if(len(ItemNumber)<4):
            ItemNumber += str(inputDec)
            print(ItemNumber)
            lcd_string(str(ItemNumber),LCD_LINE_1)
            lcd_string("",LCD_LINE_2)
            sleep(0.5)
            stateButton = 1
        
    
        
    if(input2Dec == 9 and stateButton2==0):
        if(len(ItemNumber)<4):
            ItemNumber += str(input2Dec)
            print(ItemNumber)
            lcd_string(str(ItemNumber),LCD_LINE_1)
            lcd_string("",LCD_LINE_2)
            sleep(0.5)
            stateButton2 = 1
        

    if(input2Dec == 10 and stateButton2==0):
        ItemNumber = ItemNumber.replace(' ','')[:-1].upper()
        print(ItemNumber)
        lcd_string(str(ItemNumber),LCD_LINE_1)
        lcd_string("",LCD_LINE_2)
        sleep(0.5)
        stateButton2 = 1

    if(input2Dec == 11 and stateButton2==0 and ItemNumber !=""):
        print("ok")
        lcd_clear()
        sleep(0.5)
        Mapping(ItemNumber)
        play_music(ItemNumber)
        ItemNumber = ""
        stateButton2 = 1
        
        

    if(inputDec == -1 and input2Dec == 8):
        stateButton = 0
        stateButton2 = 0
        
    if(pygame.mixer.music.get_busy()!=True):
      lcd_string_slide("Enter ItemNumber",LCD_LINE_1+5)
      
     

      
       
      
      
              

     

    #print(inputBi + " Btn")
    #print(str(inputDec) + " Btn")
    #print(input2Bi + " Btn2")
    #print(str(input2Dec) + " Btn2")
    #print("-----")
    #sleep(1)
   

   
    
    
        

    
