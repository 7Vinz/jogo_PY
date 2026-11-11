# Speed Racing — Rear Camera Pseudo-3D

Corrida arcade em Python/Pygame, com câmera traseira em pseudo-3D e multiplayer local em tela dividida.

## Instalação
Requer Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Controles
| Ação | Jogador 1 (tela esquerda) | Jogador 2 (tela direita) |
|---|---|---|
| Acelerar | W | Seta para cima |
| Frear | S | Seta para baixo |
| Virar à esquerda | A | Seta esquerda |
| Virar à direita | D | Seta direita |

ESC sai. R reinicia depois que todos cruzarem a chegada.

## Como funciona a câmera
Cada jogador tem sua própria câmera traseira, em uma das metades da tela. A pista é desenhada por faixas horizontais com largura crescente, simulando profundidade. Carros rivais e o outro jogador são projetados no horizonte conforme a diferença de distância percorrida.

## Estrutura
- `main.py`: inicialização
- `settings.py`: resolução, cores e parâmetros físicos
- `src/game.py`: loop, multiplayer e integração
- `src/car.py`: controles, aceleração e IA
- `src/renderer.py`: cenário, pista em perspectiva e carros
- `src/race.py`: contagem regressiva e classificação
- `src/hud.py`: velocidade e instruções

## Protótipo
A primeira versão inclui dois jogadores locais, quatro rivais com IA, aceleração, frenagem, direção, pista pseudo-3D, painel de velocidade, cronômetro e chegada. Colisões físicas, curvas reais de pista, nitro, spritesheets e áudio podem ser adicionados nas próximas versões.
