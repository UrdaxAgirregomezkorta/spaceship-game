# Spaceship Game

Un juego 2D de disparos desarrollado en Python usando Pygame donde debes defender la Tierra de una invasion alienigena.

## Descripcion

Este es un juego clasico de disparos en 2D donde controlas una nave espacial que debe destruir enemigos que caen desde la parte superior de la pantalla. El objetivo es obtener la mayor puntuacion posible mientras evitas las colisiones con los enemigos.

## Caracteristicas

- Movimiento fluido de la nave del jugador
- Sistema de disparos con proyectiles
- Enemigos que aparecen aleatoriamente
- Sistema de puntuacion
- Dificultad progresiva (los enemigos aparecen mas rapido con el tiempo)
- Deteccion de colisiones
- Pantalla de fin de juego con opcion de reinicio
- Fondo animado con estrellas

## Requisitos

- Python 3.6 o superior
- Pygame

## Instalacion

1. Clona este repositorio:
```bash
git clone https://github.com/UrdaxAgirregomezkorta/spaceship-game.git
cd spaceship-game
```

2. Instala Pygame:
```bash
pip install pygame
```

## Como jugar

1. Ejecuta el juego:
```bash
python main.py
```

2. Controles:
   - Flecha izquierda: Mover nave hacia la izquierda
   - Flecha derecha: Mover nave hacia la derecha
   - Barra espaciadora: Disparar
   - R: Reiniciar el juego (cuando termina)

## Reglas del juego

- Usa las flechas para mover tu nave
- Presiona la barra espaciadora para disparar a los enemigos
- Cada enemigo destruido te da 10 puntos
- Si un enemigo toca tu nave, el juego termina
- La velocidad de aparicion de enemigos aumenta gradualmente

## Estructura del codigo

- `Jugador`: Clase que maneja la nave del jugador
- `Proyectil`: Clase para los disparos del jugador
- `Enemigo`: Clase para las naves enemigas
- `Juego`: Clase principal que maneja la logica del juego

## Autor

Desarrollado por UrdaxAgirregomezkorta

## Licencia

Este proyecto es de codigo abierto y esta disponible bajo la licencia MIT.