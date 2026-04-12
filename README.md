# README – Extensões do Projeto Asteroids (Pygame)

## Visão geral

Este projeto consiste em uma extensão do jogo clássico Asteroids, desenvolvido utilizando a biblioteca Pygame. A versão original apresenta mecânicas básicas como movimentação da nave, disparo, destruição de asteroides, presença de inimigos (UFO) e progressão por waves.

O objetivo deste trabalho é enriquecer a experiência do jogador por meio da implementação de novas mecânicas, buscando aumentar a variedade, a estratégia e a dinâmica do jogo, sem descaracterizar a proposta original.

---

## Ideia geral das melhorias

As novas mecânicas foram pensadas para atuar em diferentes aspectos do gameplay:

- progressão, com foco em recompensar habilidade  
- sobrevivência, reduzindo situações frustrantes  
- combate, adicionando variações de ataque  
- ambiente, trazendo novas interações  
- estratégia, permitindo maior controle da situação em tela  

A proposta é manter a base do jogo, mas adicionar elementos que tornem a experiência mais interessante ao longo das partidas.

---

## Mecânicas implementadas

### 1. Sistema de combo - Fernando

O jogador recebe um multiplicador de pontos ao destruir asteroides ou inimigos em sequência dentro de um curto intervalo de tempo.

O multiplicador aumenta conforme a sequência continua. Caso o jogador demore para destruir um novo alvo, o combo é reiniciado.

Impacto: incentiva um estilo de jogo mais agressivo e torna a pontuação mais dinâmica.

---

### 2. Escudo temporário (pickup) - Fernando

Um item pode surgir na tela e, ao ser coletado, concede invulnerabilidade por alguns segundos.

Durante esse período, a nave não sofre dano por colisões ou tiros. O efeito é temporário e se encerra automaticamente.

Impacto: reduz mortes inesperadas e oferece ao jogador momentos de maior segurança.

---

### 3. Asteroide explosivo

Alguns asteroides possuem comportamento especial. Ao serem destruídos, geram uma explosão que afeta outros asteroides próximos.

Essa explosão pode destruir múltiplos alvos e gerar reações em cadeia.

Impacto: adiciona uma camada estratégica ao jogo e cria situações de alto impacto durante a partida.

---

### 4. Power-up de tiro

Determinados itens concedem melhorias temporárias ao disparo da nave.

Entre os efeitos possíveis estão o disparo duplo, triplo ou o aumento da cadência de tiro. Após um período, o comportamento da arma retorna ao padrão.

Impacto: aumenta a sensação de progresso e torna o combate mais variado.

---

### 5. Mina espacial

A nave pode soltar uma mina que permanece na tela por um tempo limitado.

A mina explode ao entrar em contato com inimigos ou após um intervalo de tempo, causando dano em área.

Impacto: permite maior controle do espaço e introduz novas possibilidades estratégicas.

---

## Antes e depois do jogo

Antes das modificações, o jogo era focado principalmente em desviar e atirar, com pouca variação de decisões durante a partida.

Após a implementação das novas mecânicas, o jogador passa a ter mais opções estratégicas, podendo escolher entre jogar de forma mais agressiva, utilizar recursos defensivos, controlar o espaço ou aproveitar momentos de vantagem.

O resultado é um gameplay mais dinâmico, com maior sensação de progressão e variedade ao longo das waves.
