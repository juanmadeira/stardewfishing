# Stardew Fishing

<p align="center">
    <img src="../assets/title.png" alt="Logo de Stardew Fishing" width="475px">
</p>

[![Build status](https://github.com/juanmadeira/stardewfishing/actions/workflows/build.yml/badge.svg?branch=main&event=push)](https://github.com/juanmadeira/stardewfishing/actions/workflows/build.yml)
[![GitHub release](https://img.shields.io/github/release/juanmadeira/stardewfishing.svg)](https://github.com/juanmadeira/stardewfishing/releases/latest)

Stardew Fishing é um jogo de pesca de _quick time event_ que utiliza da biblioteca [graphics](https://mcsp.wartburg.edu/zelle/python/graphics.py), onde o jogador deve capturar peixes em um ambiente inspirado no minigame de pesca de Stardew Valley, criado originalmente por Eric Barone (CorcernedApe). O objetivo principal é pescar peixes em uma barra com um cursor de pesca que se move de maneira fluida, atento à movimentação do peixe que acrescenta ao desafio.

<p align="center">
    <img src="./screenshot.png" alt="Captura de tela de Stardew Fishing" width="550px">
</p>

## Download 
| 🪟 [Windows 10+ (x64)](https://github.com/juanmadeira/stardewfishing/releases/latest/download/stardewfishing.exe) | 🐧 [Linux (x64)](https://github.com/juanmadeira/stardewfishing/releases/latest/download/stardewfishing) |
| ------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|

<br>

<p align="center">
    <img src="../assets/fishes/common/anchovy.png" width="30px">
    <img src="../assets/fishes/common/carp.png" width="30px">
    <img src="../assets/fishes/common/herring.png" width="30px">
    <img src="../assets/fishes/common/sardine.png" width="30px">
    <img src="../assets/fishes/common/sunfish.png" width="30px">
</p>

## Controles
### Captura do peixe
Enquanto o jogo está em execução, há uma chance aleatória de surgir um peixe. O jogador deve ser ágil para escutar o som de fisgada e voltar para o jogo em um tempo rápido o bastante para entrar no modo de captura. Para capturar um peixe, o jogador deve manter o cursor sobre o peixe na barra de pesca por um determinado tempo, controlando-o com a barra de espaço ou com a seta para cima.

### Cursor e gravidade
O cursor de pesca se comporta de forma fluida, movendo-se de acordo com a gravidade. A aceleração de queda faz com que o jogador precise ser ágil para controlar o cursor e garantir que ele esteja na posição certa para capturar o peixe.

### Barra de progresso
A barra de progresso é um indicador de quão próximo o jogador está de fisgar o peixe. Quanto mais tempo o cursor ficar em contato com o peixe, mais a barra vai se enchendo. Se o cursor perder o contato com o peixe, a barra de progresso começa a diminuir gradativamente. Se a barra chegar a zero, o peixe escapa e o jogador perde a captura.

<p align="center">
    <img src="../assets/fishes/uncommon/catfish.png" width="30px">
    <img src="../assets/fishes/uncommon/rainbow-trout.png" width="30px">
    <img src="../assets/fishes/uncommon/salmon.png" width="30px">
    <img src="../assets/fishes/uncommon/shad.png" width="30px">
    <img src="../assets/fishes/uncommon/sturgeon.png" width="30px">
</p>

## Dificuldade
### Raridade dos peixes
Os peixes possuem raridades aleatórias, que influenciam tanto sua velocidade de movimento quanto a intensidade da oscilação. Peixes mais raros se movem de maneira mais imprevisível e difícil de capturar, o que aumenta a dificuldade do jogo.

### Tamanho do cursor
O tamanho do cursor varia de acordo com a dificuldade do peixe. Quanto maior a dificuldade, menor será o cursor, o que exige precisão e timing para fisgar o peixe.

### Pontuação e progresso
O objetivo do jogo é capturar o maior número possível de peixes, que são convertidos em um valor determinado por sua raridade.