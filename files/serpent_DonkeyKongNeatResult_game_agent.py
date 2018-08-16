from serpent.game_agent import GameAgent
from serpent.input_controller import KeyboardKey

import sys

import numpy as np

from .helpers.ann_evaluation import Eval


class SerpentDonkeyKongNeatResultGameAgent(GameAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.frame_handlers["PLAY"] = self.handle_play

        self.frame_handler_setups["PLAY"] = self.setup_play

        self.analytics_client = None

        # Genetic algorithms parameters
        self.neat = Eval(5)
        self.old_keys = [0,0,0,0,0]
        self.input_keys = {0: KeyboardKey.KEY_LEFT, 1: KeyboardKey.KEY_RIGHT, 2: KeyboardKey.KEY_UP, 3: KeyboardKey.KEY_DOWN, 4: KeyboardKey.KEY_X}

        self.counter = 0
        self.old_posX = -1000
        self.evaluated_individuals = 0

    def setup_play(self):
        pass

    def handle_play(self, game_frame):
        if (self.game.api.not_running()):
            keys = [0,0,0,0,0]
            self._press_keys(keys)
            self.game.api.run()
        else :
            locations = self.game.api.analyze_frame(game_frame)
            if (self.evaluated_individuals % 3 == 0 and self.evaluated_individuals != 0):
            	self.input_controller.tap_key(KeyboardKey.KEY_R, duration=0.5)
            	# self.game.api.replay()
            	self.evaluated_individuals = 0
            else :
                if (self.game.api.is_in_menu()):
                    self.input_controller.tap_key(KeyboardKey.KEY_R)
                    self.game.api.next()
                    #self.neat.prepare_next()
                    if (locations[0] != None): # En mode demo
                        self.input_controller.tap_key(KeyboardKey.KEY_SPACE)
                    self.input_controller.tap_key(KeyboardKey.KEY_ENTER) # lancer partie
                    self.input_controller.tap_key(KeyboardKey.KEY_ENTER)
                    self.old_posX = -1000
                    self.counter = 0
                elif (self.game.api.is_playing()):
                    reduced_frame, projection_matrix = self.game.api.get_projection_matrix(game_frame, locations[0])
                    keys = self.neat.feed(projection_matrix)
                    if (keys[2] == 1):
                        keys = [0,0,1,0,0]

                    self.game.api.analyze_action(projection_matrix, keys)
                    
                    self._press_keys(keys)
                    self.old_keys = keys

                    if(keys == [0,0,0,0,0] or (self.old_posX != -1000 and locations[0] != None and projection_matrix[len(projection_matrix)-1] != 3 and  abs(self.old_posX-locations[0][1]) <= 5)):
                        self.counter = self.counter + 1
                        if(self.counter == 30):
                            score = self.game.api.get_score_value(locations[0])
                            if (score[0] == -1000 and score[1] == -1000):
                                self.counter = 0
                                self.old_posX = -1000
                            else:
                                self.game.api.win()
                                keys = [0,0,0,0,0]
                                self._press_keys(keys)
                                self.old_keys = keys
                                self.input_controller.tap_key(KeyboardKey.KEY_R, duration=1.0)
                                self.game.api.run()
                                self.neat.fitness(score)
                    else :
                        self.counter = 0
                        if (locations[0] != None):
                            self.old_posX = locations[0][1]
                elif (self.game.api.is_dead()):
                    position_dead = self.game.api.get_death_location(game_frame)
                    score = self.game.api.get_score_value(position_dead)
                    self.neat.fitness(score)
                    self.game.api.run()
                    keys = [0,0,0,0,0]
                    self._press_keys(keys)
                    self.old_keys = keys
                    self.input_controller.tap_key(KeyboardKey.KEY_R, duration=0.5)
                elif (self.game.api.has_won()):
                    keys = [0,0,0,0,0]
                    self._press_keys(keys)
                    self.old_keys = keys
                    self.input_controller.tap_key(KeyboardKey.KEY_R, duration=0.5)
                    self.game.api.run()
                    self.neat.fitness([10,0,10,0,1])

    def _press_keys(self, keys):
        old = np.array(self.old_keys[:len(self.old_keys)-1])
        new = np.array(keys[:len(keys)-1])
        
        released = np.bitwise_and(old, np.invert(new))
        pressed = np.bitwise_and(new, np.invert(old))

        to_release = [indice for (indice, value) in enumerate(released) if value == 1]
        to_press = [indice for (indice, value) in enumerate(pressed) if value == 1]

        for i in to_release:
            self.input_controller.release_key(self.input_keys[i])

        for i in to_press:
            self.input_controller.press_key(self.input_keys[i])

        if (keys[len(keys)-1] == 1):
            self.input_controller.tap_key(self.input_keys[len(keys)-1])