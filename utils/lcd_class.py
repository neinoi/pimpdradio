#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# $Id: lcd_class.py,v 1.22 2014/08/29 10:25:14 bob Exp $
# Raspberry Pi Internet Radio
# using an HD44780 LCD display
#
# Copyright Julien Bellion 2014 (https://github.com/neinoi)
#
# Original author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# From original LCD routines : Matt Hawkins
# Site   : http://www.raspberrypi-spy.co.uk
#
# Expanded to use 4 x 20  display
#
# This program uses  Music Player Daemon 'mpd'and it's client 'mpc'
# See http://mpd.wikia.com/wiki/Music_Player_Daemon_Wiki
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#             The authors shall not be liable for any loss or damage however caused.
#


import threading
import time
import RPi.GPIO as GPIO


# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4_21 = 21    # Rev 1 Board
LCD_D4_27 = 27    # Rev 2 Board
LCD_D5 = 22
LCD_D6 = 23
LCD_D7 = 24

# Define LCD device constants
LCD_WIDTH = 20    # Default characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

# Some LCDs use different addresses (16 x 4 line LCDs)
# Comment out the above two lines and uncomment the two lines below
# LCD_LINE_3 = 0x90 # LCD RAM address for the 3rd line
# LCD_LINE_4 = 0xD0 # LCD RAM address for the 4th line

# If using a 4 x 16 display also amend the lcd.setWidth(<width>) statement in rradio4.py

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def interrupt():
    return False

# Lcd Class
class Lcd:
    width = LCD_WIDTH
    # If display can support umlauts set to True else False
    displayUmlauts = True
    RawMode = False         # Test only
    lcd_d4 = LCD_D4_27    # Default for revision 2 boards

    lcd_p1 = lcd_p2 = lcd_p3 = lcd_p4 = 0

    lcd_line1 = lcd_line2 = lcd_line3 = lcd_line4 = ""
    new_line1 = new_line2 = new_line3 = new_line4 = ""

    timerRefresh = None

    def __init__(self):
        return

    # Initialise for either revision 1 or 2 boards
    def init(self,revision,tempo = 0.5):
        # LED outputs
        if revision == 1:
            self.lcd_d4 = LCD_D4_21

        GPIO.setwarnings(False)            # Disable warnings
        GPIO.setmode(GPIO.BCM)            # Use BCM GPIO numbers
        GPIO.setup(LCD_E, GPIO.OUT)        # E
        GPIO.setup(LCD_RS, GPIO.OUT)    # RS
        GPIO.setup(self.lcd_d4, GPIO.OUT) # DB4
        GPIO.setup(LCD_D5, GPIO.OUT)    # DB5
        GPIO.setup(LCD_D6, GPIO.OUT)    # DB6
        GPIO.setup(LCD_D7, GPIO.OUT)    # DB7

        self._byte_out(0x33,LCD_CMD)
        self._byte_out(0x32,LCD_CMD)
        self._byte_out(0x28,LCD_CMD)
        self._byte_out(0x0C,LCD_CMD)
        self._byte_out(0x06,LCD_CMD)
        self._byte_out(0x01,LCD_CMD)
        time.sleep(1)

        self.timerRefresh = threading.Timer(tempo, self._refresh, [tempo])
        self.timerRefresh.start()

        return


    # Set the display width
    def setWidth(self,width):
        self.width = width
        return


    def setLine1(self,text):
        self.new_line1 = text
        self.lcd_p1 = 0
        
        #self._refresh()
        return


    def setLine2(self,text):
        self.new_line2 = text
        self.lcd_p2 = 0
        
        #self._refresh()
        return


    def setLine3(self,text):
        self.new_line3 = text
        self.lcd_p3 = 0
        
        #self._refresh()
        return


    def setLine4(self,text):
        self.new_line4 = text
        self.lcd_p4 = 0
        
        #self._refresh()
        return


    def _refresh(self,tempo = 0.5):
        #         if timerRefresh is not None:
        #             try:
        #                 timerRefresh.cancel()
        #             except:
        #                 pass
        
        if self.new_line1 != self.lcd_line1 or len(self.lcd_line1) > LCD_WIDTH:
            self.lcd_line1 = self.new_line1
            self.lcd_p1 = self._affLine(LCD_LINE_1,self.lcd_line1,self.lcd_p1)
            
        if self.new_line2 != self.lcd_line2 or len(self.lcd_line2) > LCD_WIDTH:
            self.lcd_line2 = self.new_line2
            self.lcd_p2 = self._affLine(LCD_LINE_2,self.lcd_line2,self.lcd_p2)
            
        if self.new_line3 != self.lcd_line3 or len(self.lcd_line3) > LCD_WIDTH:
            self.lcd_line3 = self.new_line3
            self.lcd_p3 = self._affLine(LCD_LINE_3,self.lcd_line3,self.lcd_p3)
            
        if self.new_line4 != self.lcd_line4 or len(self.lcd_line4) > LCD_WIDTH:
            self.lcd_line4 = self.new_line4
            self.lcd_p4 = self._affLine(LCD_LINE_4,self.lcd_line4,self.lcd_p4)

        if self.lcd_p1 < 0 and self.lcd_p2 < 0 and self.lcd_p3 < 0 and self.lcd_p4 < 0:
            self.lcd_p1 = 0
            self.lcd_p2 = 0
            self.lcd_p3 = 0
            self.lcd_p4 = 0

        if self.lcd_p1 == 0 and self.lcd_p2 == 0 and self.lcd_p3 == 0 and self.lcd_p4 == 0:
            self.timerRefresh = threading.Timer(tempo*5, self._refresh, [tempo])
            self.timerRefresh.start()
        else:
            self.timerRefresh = threading.Timer(tempo, self._refresh, [tempo])
            self.timerRefresh.start()

        return


    def clear(self):
        self.lcd_p1 = self.lcd_p2 = self.lcd_p3 = self.lcd_p4 = 0
    
        self.lcd_line1 = self.lcd_line2 = self.lcd_line3 = self.lcd_line4 = ""
        self.new_line1 = self.new_line2 = self.new_line3 = self.new_line4 = ""
        

    def _affLine(self,lcd_line,text,pos):
        ret = pos

        if len(text) > 0 and len(text) <= self.width:
            if pos==0:
                ret = -2
                self._byte_out(lcd_line, LCD_CMD)
                self._string(text)
        else:
            if pos >= 0:
                t = text[pos:pos+self.width]
                ret = ret +1

                self._byte_out(lcd_line, LCD_CMD)
                if len(t) < self.width:
                    t = text[0:self.width+1]
                    ret = -1

                self._string(t)

        return ret

    # Send string to display
    def _string(self,message):
        s = message.ljust(self.width," ")
        if not self.RawMode:
            s = self.translateSpecialChars(s)
        for i in range(self.width):
            self._byte_out(ord(s[i]),LCD_CHR)
        return

    # Output byte to Led  mode = Command or Data
    def _byte_out(self,bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command
        GPIO.output(LCD_RS, mode) # RS

        # High bits
        GPIO.output(self.lcd_d4, False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.lcd_d4, True)
        if bits&0x20==0x20:
            GPIO.output(LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(LCD_D7, True)

        # Toggle 'Enable' pin
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, True)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, False)
        time.sleep(E_DELAY)

        # Low bits
        GPIO.output(self.lcd_d4, False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if bits&0x01==0x01:
            GPIO.output(self.lcd_d4, True)
        if bits&0x02==0x02:
            GPIO.output(LCD_D5, True)
        if bits&0x04==0x04:
            GPIO.output(LCD_D6, True)
        if bits&0x08==0x08:
            GPIO.output(LCD_D7, True)

        # Toggle 'Enable' pin
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, True)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, False)
        time.sleep(E_DELAY)
        return

    # Set raw mode on (No translation)
    def setRawMode(self,value):
        self.RawMode = value
        return

    # Display umlats if tro elese oe ae etc
    def displayUmlauts(self,value):
        self.displayUmlauts = value
        return

    # Translate special characters (umlautes etc) to LCD values
    # See standard character patterns for LCD display
    def translateSpecialChars(self,sp):
        s = sp

        # Currency
        s = s.replace(chr(156), '#')       # Pound by hash
        s = s.replace(chr(169), '(c)')     # Copyright

        # Spanish french
        s = s.replace(chr(241), 'n')       # Small tilde n
        s = s.replace(chr(191), '?')       # Small u acute to u
        s = s.replace(chr(224), 'a')       # Small a grave to a
        s = s.replace(chr(225), 'a')       # Small a acute to a
        s = s.replace(chr(226), 'a')       # Small a circumflex to a
        s = s.replace(chr(232), 'e')       # Small e grave to e
        s = s.replace(chr(233), 'e')       # Small e acute to e
        s = s.replace(chr(234), 'e')       # Small e circumflex to e
        s = s.replace(chr(237), 'i')       # Small i acute to i
        s = s.replace(chr(238), 'i')       # Small i circumflex to i
        s = s.replace(chr(243), 'o')       # Small o acute to o
        s = s.replace(chr(244), 'o')       # Small o circumflex to o
        s = s.replace(chr(250), 'u')       # Small u acute to u
        s = s.replace(chr(193), 'A')       # Capital A acute to A
        s = s.replace(chr(201), 'E')       # Capital E acute to E
        s = s.replace(chr(205), 'I')       # Capital I acute to I
        s = s.replace(chr(209), 'N')       # Capital N acute to N
        s = s.replace(chr(211), 'O')       # Capital O acute to O
        s = s.replace(chr(218), 'U')       # Capital U acute to U
        s = s.replace(chr(220), 'U')       # Capital U umlaut to U
        s = s.replace(chr(231), 'c')       # Small c Cedilla
        s = s.replace(chr(199), 'C')       # Capital C Cedilla

        # German
        s = s.replace(chr(196), "Ae")           # A umlaut
        s = s.replace(chr(214), "Oe")           # O umlaut
        s = s.replace(chr(220), "Ue")           # U umlaut

        if self.displayUmlauts:
            s = s.replace(chr(223), chr(226))       # Sharp s
            s = s.replace(chr(246), chr(239))       # o umlaut
            s = s.replace(chr(228), chr(225))       # a umlaut
            s = s.replace(chr(252), chr(245))       # u umlaut
        else:
            s = s.replace(chr(228), "ae")           # a umlaut
            s = s.replace(chr(223), "ss")           # Sharp s
            s = s.replace(chr(246), "oe")           # o umlaut
            s = s.replace(chr(252), "ue")           # u umlaut
        return s


# End of Lcd class
