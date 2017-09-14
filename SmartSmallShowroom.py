import RPi.GPIO as io
import pygame
import time 
from time import sleep
import smbus
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

      
    
#------------------------------------#End Define Display
lcd_init()
io.setmode(io.BCM)
pygame.mixer.init()
LedControl = 23 #1pin
MotorOutput = [26,5,6,13,19] #5pin en A0 A1 A2 A3 
MotorControl = [17,4,14,15] #4pin

ROW = [21,20,16,12] 
COL = [11,9,10]

MATRIX = [[1,2,3],
           [4,5,6],
           [7,8,9],
           [11,0,12]]

ItemNumber = ""
try:
  for j in range(3):
    io.setup(COL[j], io.OUT)
    io.output(COL[j], 1)

  for i in range (4):
    io.setup(ROW[i], io.IN)

  for k in range(len(MotorControl)):
    io.setup(MotorControl[k], io.OUT)

  for l in range(len(MotorOutput)):
    io.setup(MotorOutput[l], io.OUT)
except KeyboardInterupt:
  io.cleanup()

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

ItemRef = ["7","79","08","8888","8080","8000","0008","0088","8008"]
def Mapping(ItemNumber):
  if(ItemNumber == ItemRef[0]):
    Stepper_output(0,0,0,0)#y0
    print("y0")
    
  elif(ItemNumber == ItemRef[1]):
    Stepper_output(0,0,0,1)#y1
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
        
        
    except :
        pygame.mixer.music.stop()
        print("no music"+str(Position)+".mp3")
        lcd_string("no music"+str(Position)+".mp3",LCD_LINE_1)
        lcd_string("Try Again",LCD_LINE_2)
        sleep(2)
        
        pass
    


io.output(MotorOutput[0],1)    
while True:
    Stepper_control()

    for j in range (3):
        io.output(COL[j],0)
        for i in range(4):
            if io.input (ROW[i]) == 0:
                if(MATRIX[i][j]  != 12 and MATRIX[i][j] !=11):
                  if(len(ItemNumber)<4):
                    ItemNumber+= str(MATRIX[i][j])
                  lcd_string(str(ItemNumber),LCD_LINE_1)
                  lcd_string("",LCD_LINE_2)
                  print(ItemNumber)

                elif (MATRIX[i][j] == 11):
                  ItemNumber = ItemNumber.replace(' ','')[:-1].upper()
                  lcd_string(str(ItemNumber),LCD_LINE_1)
                  lcd_string("",LCD_LINE_2)
                  print(ItemNumber)

                elif (MATRIX[i][j] == 12):
                  lcd_clear()
                  Mapping(ItemNumber)
                  play_music(ItemNumber)
                  ItemNumber=""
                  
                time.sleep(0.1)
                while (io.input(ROW[i]) == 0):
                    pass
        io.output(COL[j],1)
  
    
    
    if(pygame.mixer.music.get_busy()!=True and ItemNumber == ""):
      lcd_string("Enter ItemNumber",LCD_LINE_1)
      lcd_string("",LCD_LINE_2)
      io.output(MotorOutput[0],1)
      
     

      
       
      
      

   

   
    
    
        

    
