import time
from picamera import PiCamera
import RPi.GPIO as GPIO
from gpiozero  import LED
from time import sleep #Импортирование библиотек 

led1 = LED(25)
led2 = LED(24) #Инициализация двух объектов — диодов, которые связаны с GPIO 24 и 25

led1.on()
led2.on() #Включение двух диодов
sleep(0.5) #Пауза 0.5 секунды

GPIO.setmode(GPIO.BCM) #Выбор нумерации GPIO через BCM

camera = PiCamera() #Инициализация объекта камеры
camera.resolution = (640,640) #Установка разрешения (640*640 пикселей)
sleep(0.5) #Пауза 0.5 секунды
camera.start_preview() #Запуск камеры
camera.start_recording('/home/pi/Desktop/cube.h264') #Начало записи, сохранение видеоролика в папке

ControlPin = [7, 11, 13, 15] #Инициализация портов GPIO, к которым подключён шаговый моторчик в массиве

for pin in ControlPin: #Создание цикла в массиве
    GPIO.setup(pin, GPIO.OUT) #Установка порта, в качестве выхода
    GPIO.output(pin, 0) #Установка значения вывода порта на 0 (False) 

seq = [ [1, 0, 0, 0], #Инициализация двойного массива, состоящего из нулей и единиц. 
        [1, 1, 0, 0], #1 — истина, 0 — ложь. Когда значение равное истине, 
        [0, 1, 0, 0], #включается одна из 16 магнитных катушек.
        [0, 1, 1, 0], #Поочередное включение и выключение магнитных катушек 
        [0, 0, 1, 0], #создает вращательное движение мотора
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1]
    ]

for i in range(512): #Запуск цикла на полный оборот (8*64=512)
    for halfstep in range(8):
        for pin in range(4):
            GPIO.output(ControlPin[pin], seq[halfstep][pin]) #Включение магнитных катушек.
        time.sleep(0.005) #Установка скорости вращения за счёт пауз

GPIO.cleanup() #Завершение работы 

camera.stop_recording() #Остановка записи
camera.stop_preview() #Остановка работы камеры


