import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Constantes del juego
ANCHO = 800
ALTO = 600
FPS = 60

# Colores (RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 100, 200)
ROJO = (200, 0, 0)
VERDE = (0, 200, 0)
AMARILLO = (255, 255, 0)

# Configurar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Shooter 2D - ¡Defiende la Tierra!")
reloj = pygame.time.Clock()

class Jugador:
    def __init__(self):
        self.ancho = 40
        self.alto = 30
        self.x = ANCHO // 2 - self.ancho // 2
        self.y = ALTO - self.alto - 10
        self.velocidad = 5
        self.vivo = True
        
    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.x < ANCHO - self.ancho:
            self.x += self.velocidad
            
    def dibujar(self, pantalla):
        # Dibujar nave del jugador (triángulo)
        puntos = [
            (self.x + self.ancho // 2, self.y),
            (self.x, self.y + self.alto),
            (self.x + self.ancho, self.y + self.alto)
        ]
        pygame.draw.polygon(pantalla, AZUL, puntos)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

class Proyectil:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 4
        self.alto = 10
        self.velocidad = 7
        
    def mover(self):
        self.y -= self.velocidad
        
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, AMARILLO, (self.x, self.y, self.ancho, self.alto))
        
    def fuera_pantalla(self):
        return self.y < 0
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

class Enemigo:
    def __init__(self):
        self.ancho = 30
        self.alto = 20
        self.x = random.randint(0, ANCHO - self.ancho)
        self.y = -self.alto
        self.velocidad = random.randint(2, 4)
        
    def mover(self):
        self.y += self.velocidad
        
    def dibujar(self, pantalla):
        # Dibujar enemigo (rectángulo rojo)
        pygame.draw.rect(pantalla, ROJO, (self.x, self.y, self.ancho, self.alto))
        # Detalles del enemigo
        pygame.draw.rect(pantalla, BLANCO, (self.x + 5, self.y + 5, 5, 5))
        pygame.draw.rect(pantalla, BLANCO, (self.x + 20, self.y + 5, 5, 5))
        
    def fuera_pantalla(self):
        return self.y > ALTO
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

class Juego:
    def __init__(self):
        self.jugador = Jugador()
        self.proyectiles = []
        self.enemigos = []
        self.puntaje = 0
        self.font = pygame.font.Font(None, 36)
        self.font_grande = pygame.font.Font(None, 72)
        self.tiempo_ultimo_enemigo = 0
        self.intervalo_enemigos = 1000  # milisegundos
        self.juego_terminado = False
        
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and self.jugador.vivo:
                    # Disparar proyectil
                    proj_x = self.jugador.x + self.jugador.ancho // 2 - 2
                    proj_y = self.jugador.y
                    self.proyectiles.append(Proyectil(proj_x, proj_y))
                elif evento.key == pygame.K_r and self.juego_terminado:
                    # Reiniciar juego
                    self.reiniciar()
        return True
        
    def actualizar(self):
        if self.juego_terminado:
            return
            
        # Mover jugador
        teclas = pygame.key.get_pressed()
        self.jugador.mover(teclas)
        
        # Mover proyectiles
        for proyectil in self.proyectiles[:]:
            proyectil.mover()
            if proyectil.fuera_pantalla():
                self.proyectiles.remove(proyectil)
                
        # Generar enemigos
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_enemigo > self.intervalo_enemigos:
            self.enemigos.append(Enemigo())
            self.tiempo_ultimo_enemigo = tiempo_actual
            # Aumentar dificultad gradualmente
            if self.intervalo_enemigos > 300:
                self.intervalo_enemigos -= 10
                
        # Mover enemigos
        for enemigo in self.enemigos[:]:
            enemigo.mover()
            if enemigo.fuera_pantalla():
                self.enemigos.remove(enemigo)
                
        # Verificar colisiones proyectil-enemigo
        for proyectil in self.proyectiles[:]:
            for enemigo in self.enemigos[:]:
                if proyectil.get_rect().colliderect(enemigo.get_rect()):
                    self.proyectiles.remove(proyectil)
                    self.enemigos.remove(enemigo)
                    self.puntaje += 10
                    break
                    
        # Verificar colisiones enemigo-jugador
        for enemigo in self.enemigos:
            if enemigo.get_rect().colliderect(self.jugador.get_rect()):
                self.jugador.vivo = False
                self.juego_terminado = True
                
    def dibujar(self, pantalla):
        # Limpiar pantalla
        pantalla.fill(NEGRO)
        
        # Dibujar estrellas de fondo
        for i in range(50):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            pygame.draw.circle(pantalla, BLANCO, (x, y), 1)
        
        if not self.juego_terminado:
            # Dibujar jugador
            self.jugador.dibujar(pantalla)
            
            # Dibujar proyectiles
            for proyectil in self.proyectiles:
                proyectil.dibujar(pantalla)
                
            # Dibujar enemigos
            for enemigo in self.enemigos:
                enemigo.dibujar(pantalla)
                
        # Dibujar puntaje
        texto_puntaje = self.font.render(f"Puntaje: {self.puntaje}", True, BLANCO)
        pantalla.blit(texto_puntaje, (10, 10))
        
        # Dibujar controles
        texto_controles = pygame.font.Font(None, 24).render("← → Mover | ESPACIO Disparar", True, BLANCO)
        pantalla.blit(texto_controles, (10, ALTO - 30))
        
        # Pantalla de fin de juego
        if self.juego_terminado:
            # Overlay semi-transparente
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(128)
            overlay.fill(NEGRO)
            pantalla.blit(overlay, (0, 0))
            
            # Texto de fin de juego
            texto_fin = self.font_grande.render("¡JUEGO TERMINADO!", True, ROJO)
            rect_fin = texto_fin.get_rect(center=(ANCHO//2, ALTO//2 - 50))
            pantalla.blit(texto_fin, rect_fin)
            
            texto_puntaje_final = self.font.render(f"Puntaje Final: {self.puntaje}", True, BLANCO)
            rect_puntaje = texto_puntaje_final.get_rect(center=(ANCHO//2, ALTO//2))
            pantalla.blit(texto_puntaje_final, rect_puntaje)
            
            texto_reiniciar = self.font.render("Presiona R para reiniciar", True, VERDE)
            rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO//2, ALTO//2 + 50))
            pantalla.blit(texto_reiniciar, rect_reiniciar)
            
    def reiniciar(self):
        self.jugador = Jugador()
        self.proyectiles = []
        self.enemigos = []
        self.puntaje = 0
        self.tiempo_ultimo_enemigo = 0
        self.intervalo_enemigos = 1000
        self.juego_terminado = False

def main():
    juego = Juego()
    ejecutando = True
    
    print("¡Shooter 2D iniciado!")
    print("Controles:")
    print("- Flechas izquierda/derecha: Mover nave")
    print("- Barra espaciadora: Disparar")
    print("- R: Reiniciar (cuando termina el juego)")
    print("\n¡Defiende la Tierra de la invasión alienígena!")
    
    while ejecutando:
        # Manejar eventos
        ejecutando = juego.manejar_eventos()
        
        # Actualizar juego
        juego.actualizar()
        
        # Dibujar todo
        juego.dibujar(pantalla)
        
        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()