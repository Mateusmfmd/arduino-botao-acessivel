# arduino-botao-acessivel
[![CI](https://github.com/Mateusmfmd/arduino-botao-acessivel/actions/workflows/ci.yml/badge.svg)](https://github.com/Mateusmfmd/arduino-botao-acessivel/actions/workflows/ci.yml)

Botão de acionamento amplo em Arduino para interfaces assistivas. O projeto transforma uma ação física simples em eventos seriais que podem ser consumidos por um aplicativo, uma ponte Python ou outro dispositivo.

## Por que este projeto existe

Botões pequenos podem exigir precisão motora e força que nem todas as pessoas conseguem aplicar. Um botão externo maior, com acionamento leve e retorno visual, pode ser posicionado conforme a necessidade da pessoa usuária.

O firmware foi mantido simples e reutilizável:

- usa o `INPUT_PULLUP`, sem resistor externo;
- aplica debounce não bloqueante de 35 ms;
- envia um evento apenas quando o estado realmente muda;
- acende o LED integrado enquanto o botão está pressionado;
- usa mensagens legíveis para facilitar a integração e o diagnóstico.

## Componentes

- Arduino Uno, Nano ou compatível;
- botão de acionamento amplo ou switch normalmente aberto;
- cabo jumper;
- LED integrado da placa (opcional, usado como retorno visual).

## Ligação

| Componente | Arduino |
|---|---|
| Um terminal do botão | D2 |
| Outro terminal do botão | GND |
| LED de feedback | LED integrado (`LED_BUILTIN`) |

```text
                 +--------------------+
                 |     Arduino        |
                 |                    |
 botão amplo ----+ D2                 |
                 |                    |
 botão amplo ----+ GND                |
                 |                    |
                 | LED_BUILTIN        |---- feedback visual
                 +--------------------+
```

Não conecte o botão diretamente ao 5V: o sketch usa o resistor de pull-up interno e considera `LOW` como botão pressionado.

## Como executar

1. Abra `arduino-botao-acessivel.ino` na Arduino IDE.
2. Selecione a placa e a porta serial.
3. Faça o upload.
4. Abra o Monitor Serial em **9600 baud**.
5. Pressione e solte o botão para observar os eventos.

O firmware não depende de serviços externos: depois de instalado, ele funciona
diretamente na placa e usa somente a porta serial USB para comunicar os eventos.

## Validação local

Os testes estruturais verificam a configuração essencial do sketch, o protocolo
serial, a documentação, a licença, a CI e a ausência de caches versionados:

```bash
python -m pip install pytest
pytest -q
```

Com o Arduino CLI instalado, também é possível validar a compilação para Arduino
Uno:

```bash
arduino-cli compile --fqbn arduino:avr:uno .
```

## Protocolo serial

Cada evento ocupa uma linha:

```text
BOTAO_ACESSIVEL:PRONTO
BOTAO_ACESSIVEL:PRESSIONADO
BOTAO_ACESSIVEL:SOLTO
```

A mensagem `PRONTO` é emitida uma vez na inicialização. A aplicação integradora pode ignorar eventos desconhecidos e reagir a `PRESSIONADO` e `SOLTO`.

## Integração com Python

Exemplo mínimo usando `pyserial`:

```python
import serial

with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as porta:
    for linha in porta:
        evento = linha.decode("utf-8", errors="replace").strip()
        if evento == "BOTAO_ACESSIVEL:PRESSIONADO":
            print("Ação acessível acionada")
```

No Windows, substitua `/dev/ttyACM0` por algo como `COM3`.

## Teste manual

- Ao ligar a placa, deve aparecer `BOTAO_ACESSIVEL:PRONTO`.
- Ao pressionar, deve aparecer uma única linha `...:PRESSIONADO` e o LED deve acender.
- Ao manter pressionado, não devem surgir linhas repetidas.
- Ao soltar, deve aparecer uma única linha `...:SOLTO` e o LED deve apagar.
- Toques rápidos ou ruído mecânico não devem gerar uma sequência de eventos duplicados.

## Segurança e acessibilidade

Este protótipo trabalha com baixa tensão e deve ser testado com supervisão. A posição, a força de acionamento, o tamanho e a cor do botão devem ser definidos com a pessoa usuária e, quando aplicável, com profissionais de terapia ocupacional ou educação especial.

O projeto não substitui uma avaliação individual de acessibilidade.

## Licença

MIT. Veja [LICENSE](LICENSE).

## Autor

Mateus Florido Pena
