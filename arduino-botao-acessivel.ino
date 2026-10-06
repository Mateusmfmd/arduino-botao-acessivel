/*
 * arduino-botao-acessivel
 *
 * Botão de acionamento amplo para interfaces assistivas.
 * O firmware envia eventos pela serial sem bloquear o loop:
 *   BOTAO_ACESSIVEL:PRESSIONADO
 *   BOTAO_ACESSIVEL:SOLTO
 *
 * Ligações: botão entre D2 e GND; LED opcional no LED_BUILTIN.
 */

const byte PINO_BOTAO = 2;
const byte PINO_LED = LED_BUILTIN;
const unsigned long TEMPO_DEBOUNCE_MS = 35;

bool leituraEstavel = HIGH;
bool ultimaLeitura = HIGH;
unsigned long momentoDaMudanca = 0;

void emitirEvento(const __FlashStringHelper* evento) {
  Serial.print(F("BOTAO_ACESSIVEL:"));
  Serial.println(evento);
}

void setup() {
  pinMode(PINO_BOTAO, INPUT_PULLUP);
  pinMode(PINO_LED, OUTPUT);
  digitalWrite(PINO_LED, LOW);

  Serial.begin(9600);
  Serial.println(F("BOTAO_ACESSIVEL:PRONTO"));
}

void loop() {
  const bool leituraAtual = digitalRead(PINO_BOTAO);

  if (leituraAtual != ultimaLeitura) {
    momentoDaMudanca = millis();
    ultimaLeitura = leituraAtual;
  }

  if ((millis() - momentoDaMudanca) >= TEMPO_DEBOUNCE_MS &&
      leituraEstavel != leituraAtual) {
    leituraEstavel = leituraAtual;

    const bool pressionado = (leituraEstavel == LOW);
    digitalWrite(PINO_LED, pressionado ? HIGH : LOW);
    emitirEvento(pressionado ? F("PRESSIONADO") : F("SOLTO"));
  }
}
