"""
Monte Carlo Simulation about Aeroplane Chess

by Yifan Bao, Mingyan Gong
last update on 04/23/2019
"""
import random


COLOR = ['red', 'yellow', 'blue', 'green']


class Plane:

    __all_pieces = []

    __entering_location = {'red': 39,
                           'yellow': 0,
                           'blue': 13,
                           'green': 26}

    def __init__(self, color, location='hangar'):
        self.color = color
        self.location = location
        self.location_color = color
        self.distance_travelled = 0
        Plane.__all_pieces.append(self)

    @staticmethod
    def clear_board():
        while len(Plane.__all_pieces):
            piece = Plane.__all_pieces.pop(0)
            del piece

    def update_location(self):
        if self.location == 'hangar':
            self.location = 'standby'
        elif self.location == 'standby' or isinstance(self.location, int):
            if self.distance_travelled <= 50:  # still in the track
                entering_location = Plane.__entering_location[self.color]
                self.location = entering_location + self.distance_travelled
                self.location_color = COLOR[self.location % 4 - 1]
            elif self.distance_travelled <= 55:  # entering into home zone
                self.location = 'home zone'
                self.location_color = self.color
            else:  # arrived in the center
                self.location = 'settled'
        elif self.location == 'settled':
            raise ValueError('Should not update the location of a settled plane!')

    def standby(self):
        """

        :return:
        >>> p = Plane('red')
        >>> print(p.color, p.location)
        red hangar
        >>> p.standby()
        Hangar -> Standby
        """
        # TODO: use update_location instead?
        if self.location != 'hangar':
            raise ValueError('Plane have entered in!')
        else:
            self.location = 'standby'
            print('Hangar -> Standby')

    def move(self, distance: int, enable_jump=True):
        # Move the plane
        self.distance_travelled += distance
        self.update_location()

        # When landing on an opponent's piece, send back that piece to its hangar
        if isinstance(self.location, int):
            Plane.send_back_plane_at(self.location)

        # When landing on the entrance of the plane color's shortcut, jump to the exit
        if self.distance_travelled == 18:
            self.move(12, False)
        elif enable_jump:
            # When landing on a space of the plane's own color, jump to the next space of that color
            if self.color == self.location_color:
                self.move(4, False)

    @staticmethod
    def send_back_plane_at(location):
        for plane in Plane.__all_pieces:
            if plane.location == location:
                plane.send_back()

    def send_back(self):
        self.location = 'hangar'
        self.location_color = self.color
        self.distance_travelled = 0


class Player:

    __all_players = []

    def __init__(self, color):
        self.color = color
        self.moving_planes = []
        self.settled_planes = []
        Player.__all_players.append(self)
        self.setup_planes()

    # TODO: clear player?

    @staticmethod
    def setup_players(number=4):
        for player_no in range(number):
            Player(COLOR[player_no])
        # TODO: check the number of players (should be 2-4)

    def setup_planes(self):
        p1 = Plane(self.color)
        p2 = Plane(self.color)
        p3 = Plane(self.color)
        p4 = Plane(self.color)
        self.moving_planes = [p1, p2, p3, p4]

    def move_plane(self):
        # Roll the dice
        dice = random.randint(1, 6)

        # Get a list of all planes that are available to move or standby,
        # and select one from them to move
        available_planes = []
        if dice == 6:
            # If there are planes in the hangar, get one of them standby
            for plane in self.moving_planes:
                if plane.location == 'hangar':
                    available_planes.append(plane)
            if len(available_planes):
                selected_plane = random.choice(available_planes)
                selected_plane.standby()
            # If not, move one of the planes in the track
            else:
                available_planes = self.moving_planes
                selected_plane = random.choice(available_planes)
                selected_plane.move(6)
            # Get another roll after rolling a 6
            self.move_plane()
        else:
            # A roll of 1-5, move a plane in the track
            for plane in self.moving_planes:
                if plane.location != 'hangar':
                    available_planes.append(plane)
            if len(available_planes):
                selected_plane = random.choice(available_planes)
                selected_plane.move(dice)


if __name__ == '__main__':
    Player.setup_players()

    print()
