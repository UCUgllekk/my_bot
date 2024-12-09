#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from logging import DEBUG, debug, getLogger
from math import sqrt
# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)


def parse_field_info():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    plato = input()[:-1].split()
    size = (int(plato[1]), int(plato[2]))
    return size


def parse_field(size: int):
    """
    Parse the field.

    First of all, this function is also responsible for determining the next
    move. Actually, this function should rather only parse the field, and return
    it to another function, where the logic for choosing the move will be.

    Also, the algorithm for choosing the right move is wrong. This function
    finds the first position of _our_ character, and outputs it. However, it
    doesn't guarantee that the figure will be connected to only one cell of our
    territory. It can not be connected at all (for example, when the figure has
    empty cells), or it can be connected with multiple cells of our territory.
    That's definitely what you should address.

    Also, it might be useful to distinguish between lowecase (the most recent piece)
    and uppercase letters to determine where the enemy is moving etc.

    The input may look like this:

        01234567890123456
    000 .................
    001 .................
    002 .................
    003 .................
    004 .................
    005 .................
    006 .................
    007 ..O..............
    008 ..OOO............
    009 .................
    010 .................
    011 .................
    012 ..............X..
    013 .................
    014 .................

    :param player int: Represents whether we're the first or second player
    """
    field = []
    height = size[0] + 1
    for _ in range(height):
        row = input()
        field.append(row[4:])
    return field[1:]
    #     if move is None:
    #         c = l.lower().find("o" if height == 1 else "x")
    #         if c != -1:
    #             move = i - 1, c - 4
    # assert move is not None
    # return move


def parse_figure():
    """
    Parse the figure.

    The function parses the height of the figure (maybe the width would be
    useful as well), and then reads it.
    It would be nice to save it and return for further usage.

    The input may look like this:

    Piece 2 2:
    **
    ..
    """
    size = input()
    height = int(size.split()[1])
    figure = []
    for _ in range(height):
        piece = input()
        figure.append(piece)
    return figure

def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    size = parse_field_info()
    field = parse_field(size)
    figure = parse_figure()

    def possible_coordinates(gravec: int, rozmir: tuple[int], \
        pole: list, figura: list) -> list[tuple[int]]:
        '''
        Return list with all possible coordinates for move
        '''
        coords = []

        enemy_coords = []

        if gravec == 1:

            my_sign = 'O'

            enemy_sign = 'X'

        else:

            enemy_sign = 'O'

            my_sign = 'X'

        figure_coords = [(height, width) for width in range(len(figura[0])) \

            for height in range(len(figura)) \

                if figure[height][width] == '*']

        for col in range(rozmir[0] - len(figura) + 1):

            for row in range(rozmir[1] - len(figura[0]) + 1):

                count = 0

                enemy_count = 0

                for a,b in figure_coords:

                    if pole[col][row] == my_sign or (my_sign  in (pole[col+a][row+b])):

                        count += 1

                        enemy_count += 2

                    if pole[col][row] == enemy_sign or (enemy_sign  in (pole[col+a][row+b])):

                        count += 2

                        enemy_count += 1

                if count == 1:

                    coords.append((col,row))

                if enemy_count == 1:

                    enemy_coords.append((col,row))

        return (coords, enemy_coords)

    def distance(point1, point2):
        '''
        Returns vector distance between my coordinates and enemy's coordinates
        '''
        return sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

    def shortest_distance(coords: tuple[list[tuple[int]]]):
        '''
        Returns closest coordinate to the opponent
        '''
        min_distance = float('inf')

        my_move = coords[0]

        enemy_move = coords[1]

        if my_move and enemy_move:

            for m_m in my_move:

                for e_m in enemy_move:

                    dist = distance(m_m, e_m)

                    if dist < min_distance:

                        min_distance = dist

                        closest_coord = m_m

            return closest_coord
        return []

    move = possible_coordinates(player, size, field, figure)

    last_move = move[0]

    best_move = shortest_distance(move)

    return best_move if best_move else last_move[0] if last_move else (0,0)


def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        print(*move)


def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    player = input()
    return 1 if "p1 :" in player else 2


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
