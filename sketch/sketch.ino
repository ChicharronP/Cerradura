// C++ code
//
#include <Keypad.h>
#include <Servo.h>

const int pin_led_rojo = 4;
const int pin_led_verde = 2;
const int pin_buzzer = 5;

//cosas del keypad
const byte ROWS = 4;
const byte COLS = 3;
char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},  
  {'7','8','9'},
  {'*','0','#'}
};

byte rowPins[ROWS] = {13, 12, 11, 10};
byte colPins[COLS]= {9, 8, 7};

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// cosas del servo
const int pin_servo = 3;
Servo miServo;
const int posicion_inicial = 0;
const int segundos_de_apertura = 5000; 


// variable donde guardare el numero recibido del Keypad
String cadena_caracteres = "";

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(pin_led_rojo, OUTPUT);
  pinMode(pin_led_verde, OUTPUT);
  pinMode(pin_buzzer, OUTPUT);
  pinMode(pin_servo, OUTPUT);
  
  Serial.begin(9600);
  
  miServo.attach(pin_servo);
  miServo.write(posicion_inicial);
}

void loop()
{
 // recibiendo datos del numpad
 char tecla = keypad.getKey();
  
  if( tecla != NO_KEY){
 	//enviar contrasena a la computadora
    if( tecla == '#'){
      if(cadena_caracteres != ""){
      	enviar_cadena(cadena_caracteres);
      }
    }
    else if (tecla != '*'){
      // Agregar a lista de caracteres
      agregar_a_lista(tecla);
    }
  }
  
  // En cada ciclo espera a que la computadora envie un 0 o un 1.
  buscar_respuesta();
}

void agregar_a_lista(char tecla){
 cadena_caracteres = cadena_caracteres + tecla; 
 digitalWrite(pin_buzzer, HIGH);
 delay(20);
  digitalWrite(pin_buzzer, LOW);
}

void abrir_puerta()
{
  miServo.write(posicion_inicial + 90);
  
  delay(segundos_de_apertura);
  
  miServo.write(posicion_inicial);
}

void contrasena_correcta()
{
 digitalWrite(pin_led_verde, HIGH);
 abrir_puerta();
 digitalWrite(pin_led_verde, LOW);
}

void contrasena_incorrecta() {
 // Activar el LED rojo y el buzzer
  digitalWrite(pin_led_rojo, HIGH);
  digitalWrite(pin_buzzer, HIGH);

  // Mantener activos por el tiempo especificado
  delay(500);
  digitalWrite(pin_buzzer, LOW);
  delay(100);
  digitalWrite(pin_buzzer,HIGH);
  delay(500);
  
  // Desactivar el LED y el buzzer
  digitalWrite(pin_led_rojo, LOW);
  digitalWrite(pin_buzzer, LOW);
}

void enviar_cadena(String cadena) {
  // Enviar la cadena por el puerto serial
  Serial.println(cadena_caracteres);

  // Esperar a recibir respuesta de la computadora
  int si_respondio = buscar_respuesta();  // Inicializar con un valor que no sea '0' o '1'
  while (si_respondio == 0) {
    si_respondio = buscar_respuesta();
    delay(10);
  }
  
  
  cadena_caracteres = "";
}

// Metodo para ver si hubo una respuesta
// retorna 1 si encontro una, retorna 0 si no
int buscar_respuesta(){
  char respuesta = Serial.read();
  if (respuesta == '1'){
    contrasena_correcta();
    return 1;
  }
  else if (respuesta == '0'){
    contrasena_incorrecta();
    return 1;
  }
  return 0;
}