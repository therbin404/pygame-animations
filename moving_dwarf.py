import sys, time, pygame

# on doit init tous les composants pygame
pygame.init()

WHITE = 255, 255, 255


class Player:
    def __init__(self, game):
        ### SPRITE DEFINITION ###
        self.sprite_right = pygame.image.load("sprites/u_right.png")
        self.sprite_left = pygame.image.load("sprites/u_left.png")
        # set default sprite direction
        self.sprite = self.sprite_right
        self.sprite_rect = self.sprite.get_rect()
        self.sprite_rect.y = game.screen_height - self.sprite_rect.height
        ######
        self.speed = [2, 0]

    def move(self, game):
        # moving the dwarf
        self.sprite_rect = self.sprite_rect.move(self.speed)
        print(self.sprite_rect.y)
        # filling the screen to erase previous image of the dwarf
        game.screen.fill(WHITE)
        # manage direction
        if self.sprite_rect.left < 0 or self.sprite_rect.right > game.screen_width:
            self.speed[0] = -self.speed[0]

            # manage sprite direction (printed sprite "self.sprite" will take left or right value, depending on border collided)
            if self.sprite_rect.left < 0:
                self.sprite = self.sprite_right
            elif self.sprite_rect.right > game.screen_width:
                self.sprite = self.sprite_left

        game.screen.blit(self.sprite, self.sprite_rect)


class Game:
    def __init__(self):
        self.screen_width = 400
        self.screen_height = 200
        self.screen_size = self.screen_width, self.screen_height
        self.screen = pygame.display.set_mode(self.screen_size)

    def play(self):
        player = Player(self)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            player.move(self)
            time.sleep(0.01)
            pygame.display.flip()


game = Game()
game.play()
