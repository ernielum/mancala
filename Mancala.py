# Author: Ernie Lum
# GitHub username: ernielum
# Date: 12/4/22
# Description: Defines a class Mancala that allows two people to play a text-based version of the game.

class Mancala:
    """
    Represents a Mancala game with methods to create players, play the game, and display the winner.
    """
    def __init__(self):
        """
        Constructor method for Mancala class. Takes no parameters.
        Initializes game board to an empty list, empty list of players, and all data members are private.
        Also initializes two dictionaries that indicate which pits are across from one another which is
        important for implementing special rule #2.
        """
        self._game_board = []
        self._players = []
        self._match_pits_player_1 = {
            0:12,
            1:11,
            2:10,
            3:9,
            4:8,
            5:7,
        }
        self._match_pits_player_2 = {
            12:0,
            11:1,
            10:2,
            9:3,
            8:4,
            7:5,
        }

    def create_player(self, player_name):
        """
        Takes one parameter:
        player_name - name in the form of a string input that represents the player
        Purpose: Sets up a player for a game of mancala. Adds player object and player board to the game.
        Returns: player object
        Does not create a new player if there are already two players. Player 1 is the first player created.
        """
        if len(self._players) >= 2:
            print("Only two players are allowed to play in a game of Mancala.")
        else:
            player = Player(player_name)
            self._players.append(player)
            self._game_board += player.get_board()
            return player

    def print_board(self):
        """
        Takes no parameters.
        Purpose: Prints the current board information for each player in the following format:
        Player (1 or 2):
        Store: number of seeds in player's store
        Player seeds number from pt 1 to 6 in a list
        """
        print("player1:")
        print(f"store: {self._players[0].get_board()[-1]}")
        print(self._players[0].get_board()[0:-1])
        print("player2:")
        print(f"store: {self._players[1].get_board()[-1]}")
        print(self._players[1].get_board()[0:-1])

    def return_winner(self):
        """
        Takes no parameters.
        Purpose: Displays the winner of the game if the game has ended.
        Returns:
        Player's name - if the game has ended and one player's score is higher than the other's
        Tie - if the game has ended and scores are equal
        Game has not ended - if there are still seed(s) in at least one pit for each player
        Uses Player class method get_name to retrieve player name and get_board to compare player's store values.
        """
        if sum(self._game_board[0:6]) + sum(self._game_board[7:-1]) == 0:
            if self._players[0].get_board()[-1] > self._players[1].get_board()[-1]:
                return f"Winner is player 1: {self._players[0].get_name()}"
            elif self._players[0].get_board()[-1] < self._players[1].get_board()[-1]:
                return f"Winner is player 2: {self._players[1].get_name()}"
            else:
                return "It's a tie"
        else:
            return "Game has not ended"

    def play_game(self, player_index, pit_index):
        """
        Takes two parameters:
        player_index = indicates which player's move
        pit_index = represents which pit the player is picking up
        Purpose: Given player makes a move based on given pit.
        Updates seed count in each pit and players' stores according to Mancala gameplay rules.
        Returns: List of seeds at this current moment of the game in the following format:
        [player1 pit1, player1 pit2, player1 pit3, player1 pit4, player1 pit5, player1 pit6, player1 store,
         Player2 pit1, player2 pit2, player2 pit3, player2 pit4, player2 pit5, player2 pit6, player2 store]
        Prints that the player can make another move if special rule #1 has been met.
        Prints invalid move if player_index not 1 or 2, pit_index < 1 pit_index > 6, or no seeds in selected pit.
        Uses Mancala class methods check_special_rules and check_end_game.
        """
        if self.check_end_game():
            return "Game is ended"
        if pit_index < 1 or pit_index > 6:
            print("That is not a valid pit. Try again.")
            return "Invalid number for pit index"
        else:
            if player_index < 1 or player_index > 2:
                print("That is an invalid player. Try again.")
                return "Invalid number for player index"
            elif player_index == 1:
                pit_index = pit_index - 1
                if self._game_board[pit_index] == 0:
                    print("There are no seeds in this pit. Try again.")
                    return
                seed_count = self._game_board[pit_index]
                self._game_board[pit_index] = 0
                while seed_count > 0:
                    if pit_index >= 12:
                        pit_index = -1
                        continue
                    self._game_board[pit_index + 1] += 1
                    pit_index += 1
                    seed_count -= 1
                self.check_special_rules(1, seed_count, pit_index)
            else:
                pit_index = pit_index + 6
                if self._game_board[pit_index] == 0:
                    print("There are no seeds in this pit. Try again.")
                    return
                seed_count = self._game_board[pit_index]
                self._game_board[pit_index] = 0
                while seed_count > 0:
                    if pit_index == 6:
                        continue
                    if pit_index > 12:
                        pit_index = -1
                        continue
                    self._game_board[pit_index + 1] += 1
                    pit_index += 1
                    seed_count -= 1
                self.check_special_rules(2, seed_count, pit_index)
            self._players[0].set_board(self._game_board[0:7])
            self._players[1].set_board(self._game_board[7:])
        self.set_end_game()
        return self._game_board

    def set_end_game(self):
        """
        Takes no parameters.
        Purpose: Checks if either player's pits are empty and therefore the game has ended.
        The other player will take the remaining seeds in their pit and add to their store.
        Returns: True that game is ended if conditions are met.
        """
        if sum(self._players[0].get_board()[0:-1]) == 0:
            total = self._players[1].get_board()[-1] + sum(self._players[1].get_board()[0:-1])
            self._players[1].set_board([0, 0, 0, 0, 0, 0, total])
            self._game_board[7:] = self._players[1].get_board()
        if sum(self._players[1].get_board()[0:-1]) == 0:
            total = self._players[0].get_board()[-1] + sum(self._players[0].get_board()[0:-1])
            self._players[0].set_board([0, 0, 0, 0, 0, 0, total])
            self._game_board[0:7] = self._players[0].get_board()

    def check_end_game(self):
        """
        Takes no parameters.
        Purpose: Determines if the game has ended.
        Returns: True if the game has ended.
        """
        if sum(self._players[0].get_board()[0:-1]) == 0 and sum(self._players[1].get_board()[0:-1]) == 0:
            return True

    def check_special_rules(self, player_index, seed_count, pit_index):
        """
        Takes three parameters: player_index, seed_count, and pit_index.
        player_index - indicates which player to apply the special rules
        seed_count - the amount of seeds currently in play
        pit_index - the pit at which the player's move ended on
        Purpose: Determine if a special rule has been met.
        Special rule #1 - player takes another turn if last seed in play lands in their store
        Special rule #2 - player captures opposing pit seeds and the last seed in play
                          if the last seed in play landed in their own pit that was empty.
        """
        if player_index == 1:
            if seed_count == 0 and pit_index == 6:                                         # special rule 1
                print("Player 1 takes another turn.")
            elif seed_count == 0 and self._game_board[pit_index] == 1 and pit_index < 6:   # special rule 2
                self._game_board[6] += 1
                self._game_board[pit_index] = 0
                self._game_board[6] += self._game_board[self._match_pits_player_1[pit_index]]
                self._game_board[self._match_pits_player_1[pit_index]] = 0
        elif player_index == 2:
            if seed_count == 0 and pit_index == 13:                                         # special rule 1
                print("Player 2 takes another turn.")
            elif seed_count == 0 and self._game_board[pit_index] == 1 and pit_index > 6:    # special rule 2
                self._game_board[-1] += 1
                self._game_board[pit_index] = 0
                self._game_board[-1] += self._game_board[self._match_pits_player_2[pit_index]]
                self._game_board[self._match_pits_player_2[pit_index]] = 0

class Player:
    """
    Represents a Player that wil lbe used by the Mancala class.
    """
    def __init__(self, player_name):
        """
        Takes one parameter:
        player_name = string argument which will represent the Player object
        Initializes a starting player with a given name and their side of the board
        with 4 seeds in each pit and 0 seeds in the store.
        """
        self._name = player_name
        self._player_board = [4, 4, 4, 4, 4, 4, 0]

    def get_board(self):
        """
        Takes no parameters. Used by Mancala class to get player's current board information.
        Returns:
        A list that represents the player's side of the board in the following format:
        [player pit1, player pit2, player pit3, player pit4, player pit5, player pit6, player store]
        """
        return self._player_board

    def set_board(self, player_board):
        """
        Takes one parameter. Used by Mancala class. Mancala play_game method will use this  method to
        update player's side of the board.
        """
        self._player_board = player_board

    def get_name(self):
        """
        Takes no parameters. Used by Mancala class when determining the winner.
        Returns the name of the player.
        """
        return self._name