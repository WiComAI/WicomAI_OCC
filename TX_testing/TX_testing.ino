
int values[] = {0,0,0,0, 200, 70, 100, 200, 100, 70, 150, 200, 150, 200, 70, 150, 200, 100, 150, 200, 100, 70, 150, 200, 200, 150, 70, 100,200, 100, 150, 70, 200, 150, 100, 200, 150, 70, 150, 200, 100, 150, 70, 200, 70, 200, 150, 150, 100, 200, 70, 100, 150, 200, 100, 150, 70, 200, 100, 150, 200, 70, 150, 200, 150, 100, 200, 70, 150, 200, 70, 100, 150, 200, 200, 70, 100, 150, 200, 150, 100, 70, 150, 200, 150, 200, 100, 70, 150, 200, 100, 150, 70, 200, 70, 100, 150, 200, 150, 200, 100, 70, 80, 150, 200, 0,0,0,0,0,0,0,0, 200, 150, 150, 70, 150, 100, 200, 70, 70, 150, 100, 200, 200, 200, 200, 200, 100, 150, 150, 100, 100, 70, 200, 100, 70, 100, 200, 70, 70, 70, 200, 100, 150, 150, 100, 150, 200, 200, 150, 200, 150, 150, 100, 70, 100, 200, 100, 150, 200, 150, 100, 150, 200, 200, 70, 200, 150, 70, 150, 150, 200, 200, 70, 70, 200, 200, 70, 100, 100, 200, 200, 150, 150, 200, 150, 200, 100, 150, 150, 150, 200, 200, 150, 150, 70, 100, 150, 100, 200, 150, 70, 100, 70, 100, 70, 200, 70, 150, 70, 150, 
0,0,0,0,0,0,0,0, 200, 200, 100, 100, 100, 100, 150, 200, 150, 150, 70, 100, 150, 150, 200, 200, 150, 100, 200, 200, 150, 200, 100, 200, 150, 200, 200, 150, 150, 70, 150, 150, 200, 70, 200, 70, 200, 150, 100, 200, 200, 150, 150, 150, 70, 70, 100, 150, 200, 150, 150, 150, 200, 70, 150, 100, 70, 100, 200, 200, 70, 150, 100, 100, 100, 200, 100, 100, 150, 70, 150, 100, 100, 70, 200, 70, 100, 70, 70, 150, 200, 150, 70, 150, 200, 200, 70, 70, 70, 150, 200, 200, 200, 200, 100, 150, 70, 150, 70, 200, 0,0,0,0};

int repeatCount = 1;  // Jumlah pengulangan untuk setiap nilai
int ledPin = 9; // PWM pin (dapat menggunakan pin 3, 5, 6, 9, 10, atau 11)

void setup() {
  
  // Set LED pin sebagai outputqq
  pinMode(ledPin, OUTPUT);

  // Set Timer 1 ke 16kHz
  TCCR1B = (TCCR1B & 0b11111000) | 0x01;  // Set prescaler ke 1, 16 MHz / 1 = 16kHz
}

void loop() {
  // Iterate over the values array
  for (int i = 0; i < sizeof(values) / sizeof(values[0]); i++) {
    // Ulangi setiap nilai 10 kali
    for (int j = 0; j < repeatCount; j++) {
      analogWrite(ledPin, values[i]);  // Kirim nilai PWM ke LED
      //delayMicroseconds(197); //delay untuk FLIR //~197 Delay kecil antara update /100/30//66/66+33/99/132/165/197/230/263
    delayMicroseconds(205); //200 //210/20
    }
  }

  // Matikan LED setelah loop
  analogWrite(ledPin, 0);  // Set kecerahan LED ke 0 (mati)

  // Delay agar LED tetap mati sejenak sebelum mengulang
  //delayMicroseconds(1000000);
  //delayMicroseconds(1000);
  delay(5); //6 //2 //3
}
