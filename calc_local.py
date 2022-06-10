# Created with Pyto

import pyto_ui as ui
logger = ui.Label()
logger.size = (380,40)
logger.font = ui.Font.bold_system_font_of_size(20)
logger.text_color = ui.COLOR_SYSTEM_GRAY4

disp = ui.Label()
disp.text_alignment = ui.TEXT_ALIGNMENT_RIGHT
disp.size = (380,80)
disp.font = ui.Font.bold_system_font_of_size(50)
disp.text_color = ui.COLOR_SYSTEM_GRAY6

digits = ["0","1","2","3","4","5","6","7","8","9"]
operators = ["+","−","×","÷"] 
                #minus character

#note that the "minus" character is used in key strings (button labels) and in this script generally, but the "en dash" character (like on a standard keyboard) is used in python as a minus/negative operator
#the difference is visible in the app but not in the script

x = None #first number
y = None #second number
op = None #string representation of operator like "+"
r = None #result

clear_result = False #indicates that the last key was "="
                     #some inputs should clear previous data
                     #other inputs should use that result

def send(_key):
    global x,y,op,r,clear_result

    if clear_result: #previous key was "="
        #handle various special cases
        if _key == "=": 
            #repeat op with r as x and y is the same y 
            if op == None or disp.text == "": 
                return
            logger.text = sstr(x)+" "+op+" "+sstr(y)+" ="
            calc_result()
            disp.text = sstr(r)
            return
        if _key == "+/−":
            if disp.text[0] == '−': #minus character
                disp.text = disp.text[1:]
            else:
                disp.text = '−' + disp.text
            r = 0 - r
            x = r
            logger.text = sstr(x)
            return   
        if _key == "⌫": 
            disp.text = disp.text[:-1]
            r = ffloat(disp.text)
            x = r
            logger.text = disp.text
            return
            #in each case above, clear_result remains True
        
        clear_result = False    
        
        if _key in operators:
            #keep taking input
            op = _key
            logger.text = sstr(x)+" "+op
            disp.text = ""
            return
        if _key in digits or _key == ".":
            #clear everything then process the key below
            print("CLEAR RESULT on " + _key)
            clear()
            return
            
    #thats all the special cases for clear_result
    #so these are the normal cases
    
    if _key == "=":
        if op == None or disp.text == "": 
            return
        #do op
        y = ffloat(disp.text)
        logger.text = sstr(x)+" "+op+" "+sstr(y)+" ="
        #does the calculation the usual way
        calc_result()
        clear_result = True
        disp.text = sstr(r)
        return   
    if _key in digits:
        disp.text += _key
        return
    if _key in operators:
        if not disp.text == "":
            if not op == None:
                #do old op and process the new one
                y = ffloat(disp.text)
                calc_result()
                #clear_result remains False
                disp.text = sstr(r)
            x = ffloat(disp.text)
        op = _key
        logger.text = sstr(x) + " " + op
        disp.text = ""
        return
    if _key == "." and not "." in disp.text:
        disp.text += _key
        return
    if _key == "⌫": 
        disp.text = disp.text[:-1]
        return
    if _key == "C":
        clear()
        return
    if _key == "+/−":
        if disp.text == "": 
            disp.text = "−"
            return
        if disp.text[0] == '−': #minus character
            disp.text = disp.text[1:]
        else:
            disp.text = '−' + disp.text
        return   

def calc_result():
    global x,y,op,r
    if not x or not op or not y:
        clear()
        return
    if op == "+":
        r = x+y
    elif op == "−": 
        r = x-y
    elif op == "×": 
        r = x*y
    elif op == "÷": 
        if y == 0:
            r = None
        else: r = x/y
    print (sstr(x) + " " + op + " " + sstr(y) + " =")
    print (sstr(r) +"\n")
    x = r

def clear():
    global x,y,op,r
    x = None
    y = None
    op = None
    r = None
    disp.text = ""
    logger.text = ""

def ffloat(str):
    if str == "": 
        return 0.0
    if str == "ERR":
        return None
    return float(str.replace('−','-')) #dash replaces minus

def sstr(n):
    if n == None:
        return "ERR"
    sign = ("" if n >= 0 else "−") #minus not dash
    #show integer representation if no fractional part 
    if (n%1 ==0):
        return sign+str(abs(int(n)))
    else:
        return sign+str(round(abs(n),10))
        #note that this will preserve/compound rounding errors
            
def Button(_title,_colors)-> ui.Button:
    #build a button for use with the send() function
    button = ui.Button(title=_title)
    button.size = (100, 90)
    button.corner_radius = 4
    font = ui.Font.bold_system_font_of_size(57)
    button.font = font
    button.action = lambda: send(_title)
    button.background_color = _colors[0]
    button.title_color =_colors[1]
    return button

class Row(ui.HorizontalStackView):
    #build a row of calculator buttons
    def __init__(self,titles,cols):
        def col(char):
            if (char == '1'):
                return (ui.COLOR_SYSTEM_YELLOW,
                        ui.COLOR_SYSTEM_PINK)
            if (char == '2'):
                return (ui.COLOR_SYSTEM_GRAY5,
                        ui.COLOR_SYSTEM_GRAY)
            if (char == '3'):
                return (ui.COLOR_SYSTEM_GRAY,
                        ui.COLOR_SYSTEM_GRAY6)
            if (char == '4'):
                return (ui.COLOR_SYSTEM_BLUE,
                        ui.COLOR_SYSTEM_TEAL)
            return None
        
        super().__init__()
        self.add_subview(Button(titles[0],col(cols[0])))
        self.add_subview(Button(titles[1],col(cols[1])))
        self.add_subview(Button(titles[2],col(cols[2])))
        self.add_subview(Button(titles[3],col(cols[3])))

def Spacer(_size)-> ui.View:
    #build some empty space
    sp = ui.View()
    sp.size = (_size,_size)
    return sp

class Calc(ui.VerticalStackView):
    def __init__(self):
        #build the calculator window
        super().__init__()       
        self.size = (500,750)
        self.border_color = ui.COLOR_SYSTEM_FILL
        self.border_width = 7
        self.corner_radius = 20
        self.title="calculator"
               
        head = ui.VerticalStackView()
        head.size = (425,130)
        head.corner_radius = 15
        head.background_color = ui.COLOR_SYSTEM_GRAY2
        head.border_color = ui.COLOR_SYSTEM_FILL
        head.border_width = 5
        head.add_subview(logger)
        head.add_subview(disp)
        head = ui.VerticalStackView()
        head.size = (425,130)
        head.corner_radius = 15
        head.background_color = ui.COLOR_SYSTEM_GRAY2
        head.border_color = ui.COLOR_SYSTEM_FILL
        head.border_width = 5
        head.add_subview(logger)
        head.add_subview(disp)
        
        self.add_subview(Spacer(5))
        self.add_subview(head)
        self.add_subview(Spacer(1))
        self.add_subview(Row(["...","+/−","C","⌫"],"2224"))
        self.add_subview(Row(["1","2","3","÷"],"2221"))
        self.add_subview(Row(["4","5","6","×"],"2221"))
        self.add_subview(Row(["7","8","9","−"],"2221"))
        self.add_subview(Row(["0",".","=","+"],"2241"))
        self.add_subview(Spacer(5))

calc = Calc()
ui.show_view(calc, ui.PRESENTATION_MODE_SHEET)