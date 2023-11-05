import sys, time, pygame, random

# on doit init tous les composants pygame
pygame.init()

WHITE = 255, 255, 255


class Player:
    def __init__(self, game):
        ### SPRITE DEFINITION ###
        self.sprite_right = {}
        self.sprite_left = {}

        # initialise animations
        for i in range(0, 8):
            self.sprite_right.update(
                {i: pygame.image.load("sprites/dwarf_run/right/{}.png".format(i))}
            )
            self.sprite_left.update(
                {i: pygame.image.load("sprites/dwarf_run/left/{}.png".format(i))}
            )
        # set default sprite direction
        self.sprite = self.sprite_right[0]
        self.frame = 0
        self.direction = "right"
        self.sprite_rect = self.sprite.get_rect()
        self.sprite_rect.y = game.screen_height - 75 - self.sprite_rect.height
        ######
        self.speed = [2, 0]

    def move(self, game):
        # moving the dwarf
        self.sprite_rect = self.sprite_rect.move(self.speed)
        self.frame += 1
        # manage direction
        if self.sprite_rect.left < 0 or self.sprite_rect.right > game.screen_width:
            self.speed[0] = -self.speed[0]

            # manage sprite direction (printed sprite "self.sprite" will take left or right value, depending on border collided)
            if self.sprite_rect.left < 0:
                self.direction = "right"
            elif self.sprite_rect.right > game.screen_width:
                self.direction = "left"

        # animate sprite be making sprite to show depending on frames
        self.sprite = (
            self.sprite_left[self.frame % 8]
            if self.direction == "left"
            else self.sprite_right[self.frame % 8]
        )


class Game:
    def __init__(self):
        self.screen_width = 512
        self.screen_height = 231
        self.screen_size = self.screen_width, self.screen_height
        self.screen = pygame.display.set_mode(self.screen_size)
        # .convert will make surface loading faster
        self.background = pygame.image.load("sprites/dungeon_background.png").convert()
        self.players = {}

    def add_player(self):
        self.players.update({len(self.players): Player(self)})

    def play(self):
        self.screen.blit(self.background, (0, 0))
        self.add_player()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            random_spawn = random.randint(1, 200)
            if random_spawn == 66:
                self.add_player()

            # for each update of the screen, we have to erase all images to move them
            # if we don't do it, new element can erase other new element printed before it
            # first : erase all images printed on the screen
            for player in self.players.values():
                self.screen.blit(
                    self.background, player.sprite_rect, player.sprite_rect
                )
            # at this point, we only have background, and old positions of elements
            # now, we calculate new pos of every element and print them
            for player in self.players.values():
                player.move(self)
                self.screen.blit(player.sprite, player.sprite_rect)
            time.sleep(0.05)
            pygame.display.update()


game = Game()
game.play()
