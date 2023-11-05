import sys, time, pygame, random, itertools, gc

# on doit init tous les composants pygame
pygame.init()

WHITE = 255, 255, 255


class Player:
    ##############
    ### PLAYER ###
    ##############

    id_iter = itertools.count()

    def __init__(self, game):
        self.id = next(self.id_iter)

        ### SPRITE DEFINITION ###
        self.sprite_move_right = {}
        self.sprite_move_left = {}
        self.sprite_wait_right = {}
        self.sprite_wait_left = {}
        self.sprite_hit_right = {}
        self.sprite_hit_left = {}

        # initialise animations
        # MOVING
        for i in range(0, 8):
            self.sprite_move_right.update(
                {i: pygame.image.load("sprites/dwarf_run/right/{}.png".format(i))}
            )
            self.sprite_move_left.update(
                {i: pygame.image.load("sprites/dwarf_run/left/{}.png".format(i))}
            )
        # WAITING
        for i in range(0, 5):
            self.sprite_wait_right.update(
                {i: pygame.image.load("sprites/dwarf_waiting/right/{}.png".format(i))}
            )
            self.sprite_wait_left.update(
                {i: pygame.image.load("sprites/dwarf_waiting/left/{}.png".format(i))}
            )
        # HITING
        for i in range(0, 7):
            self.sprite_hit_right.update(
                {i: pygame.image.load("sprites/dwarf_hiting/right/{}.png".format(i))}
            )
            self.sprite_hit_left.update(
                {i: pygame.image.load("sprites/dwarf_hiting/left/{}.png".format(i))}
            )
        # set default sprite direction
        self.move_sprite = self.sprite_move_right[0]
        self.hit_sprite = self.sprite_hit_right[0]
        self.wait_sprite = self.sprite_wait_right[0]
        self.move_frame = 0
        self.hit_frame = 0
        self.wait_frame = 0
        self.direction = "right"
        self.sprite_rect = self.move_sprite.get_rect()
        self.sprite_rect.y = game.screen_height - 155 - self.sprite_rect.height
        ######

        ### STATS ###
        self.speed = [4, 0]
        self.life = random.randint(20, 100)
        self.strength = random.randint(1, 10)
        self.is_alive = True
        ######

    def get_other_players_location(self, id, game):
        # we gonna exlude current id from all players positions
        filtered_position = (
            list(filter(lambda pp: pp[0] is not id, game.players_positions.items())),
        )
        # and now we gonna take all positions of prviously filtered positions
        mapped_positions = (
            list(map(lambda p: p[1], filtered_position[0]))
            if filtered_position[0]
            else False
        )
        return mapped_positions

    def move(self, game):
        # moving the dwarf
        self.sprite_rect = self.sprite_rect.move(self.speed)
        self.move_frame += 1
        # manage direction
        if self.sprite_rect.left < 0 or self.sprite_rect.right > game.screen_width:
            self.speed[0] = -self.speed[0]

            # manage sprite direction (printed sprite "self.sprite" will take left or right value, depending on border collided)
            if self.sprite_rect.left < 0:
                self.direction = "right"
            elif self.sprite_rect.right > game.screen_width:
                self.direction = "left"

        # animate sprite be making sprite to show depending on frames
        self.move_sprite = (
            self.sprite_move_left[self.move_frame % 8]
            if self.direction == "left"
            else self.sprite_move_right[self.move_frame % 8]
        )

    def hit(self, enemy, game):
        # gonna wait a little bit for hitting
        waiting_complete = self.wait_frame % 40 == 0
        if waiting_complete:
            # if we have waited long enough, we can initiate hiting
            self.hit_frame += 1
            hit_animation_complete = self.hit_frame % 7 == 0
            self.hit_sprite = (
                self.sprite_hit_left[self.hit_frame % 7]
                if self.direction == "left"
                else self.sprite_hit_right[self.hit_frame % 7]
            )
            game.screen.blit(self.hit_sprite, self.sprite_rect)
            # wait end of hit animation to inflict damages
            if hit_animation_complete:
                # and if the hit is complete, we can re-initiate waiting
                self.wait_frame += 1
                is_missed = bool(random.randint(0, 1))
                if not is_missed:
                    enemy.life -= self.strength
                    if self.life <= 0:
                        self.is_alive = False
                    if enemy.life <= 0:
                        self.is_alive = False
        else:
            self.wait_frame += 1
            self.wait_sprite = (
                self.sprite_wait_left[self.wait_frame % 5]
                if self.direction == "left"
                else self.sprite_wait_right[self.wait_frame % 5]
            )
            game.screen.blit(self.wait_sprite, self.sprite_rect)


class Game:
    ##############
    #### GAME ####
    ##############

    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 462
        self.screen_size = self.screen_width, self.screen_height
        self.screen = pygame.display.set_mode(self.screen_size)
        # .convert will make surface loading faster
        self.background = pygame.image.load("sprites/dungeon_background.png").convert()
        self.players = {}
        self.players_positions = {}

    def add_player(self):
        new_player = Player(self)
        self.players.update({new_player.id: Player(self)})

    def get_player_id_from_rect(self, value):
        for id, position in self.players_positions.items():
            if position == value:
                return id

    def get_player_from_id(self, value):
        for id, player in self.players.items():
            if id == value:
                return player

    # removing dead players means :
    # removing them from game players
    # removing their position from players_positions
    # erase their rect
    def remove_dead_players(self):
        players_to_remove = []
        for id, player in self.players.items():
            if not player.is_alive:
                players_to_remove.append(id)
                self.screen.blit(
                    self.background, player.sprite_rect, player.sprite_rect
                )
        for id in players_to_remove:
            self.players.pop(id)
            self.players_positions.pop(id)

    def play(self):
        self.screen.blit(self.background, (0, 0))
        self.add_player()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.remove_dead_players()

            random_spawn = random.randint(0, 200)
            if random_spawn == 66:
                self.add_player()

            # for each update of the screen, we have to erase all images to move them
            # if we don't do it, new element can erase other new element printed before it
            # first : erase all images printed on the screen
            for id, player in self.players.items():
                self.screen.blit(
                    self.background, player.sprite_rect, player.sprite_rect
                )
                # we also need to know all players positions
                self.players_positions.update({id: player.sprite_rect})

            # at this point, we only have background, and old positions of elements
            # now, we calculate new pos of every element and print them
            for id, player in self.players.items():
                colliding = -1
                # we're going to remove current player location from copied array
                others_positions = player.get_other_players_location(id, self)
                if others_positions:
                    colliding = player.sprite_rect.collidelist(others_positions)

                if not colliding != -1:
                    player.move(self)
                    self.screen.blit(player.move_sprite, player.sprite_rect)
                else:
                    # we have index of collided player, we need to retrieve it from players positions
                    other_player_rect = others_positions[colliding]
                    # we search this rect in players_positions
                    other_player_id = game.get_player_id_from_rect(other_player_rect)
                    # we have the id of the other player, we need the player instance
                    other_player = game.get_player_from_id(other_player_id)
                    player.hit(other_player, self)
                    other_player.hit(player, self)

            time.sleep(0.05)
            pygame.display.update()


game = Game()
game.play()
