from unittest import TestCase
from app import app, validate_word, calculate_score, boggle_game, calculate_high_score
from flask import session
from boggle import Boggle

test_board_a = [
    ['A', 'A', 'A', 'A', 'A'],
    ['A', 'A', 'A', 'A', 'A'],
    ['A', 'A', 'A', 'A', 'A'],
    ['A', 'A', 'A', 'A', 'A'],
    ['A', 'A', 'A', 'A', 'A'],
]

test_board_b = [
    ['C', 'A', 'T', 'A', 'N'],
    ['B', 'A', 'A', 'O', 'O'],
    ['D', 'I', 'A', 'A', 'A'],
    ['O', 'A', 'T', 'A', 'A'],
    ['G', 'A', 'A', 'E', 'A'],
]


class FlaskTests(TestCase):
    def test_game_form(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle the Mind </h1>', html)

    def test_word_submit(self):
        with app.test_client() as client:
            with client.session_transaction() as client_session:
                client_session['board'] = test_board_a
                client_session['total_score'] = 0
                client_session['high_score'] = 0
                client_session['words_used'] = []

            res = client.post('/guess', data={'word': 'A'})
            json_res = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(json_res['word'], 'ok')
            self.assertEqual(json_res['high_score'], 1)
            self.assertEqual(json_res['total_score'], 1)

    def test_word_submit_not_valid(self):
        with app.test_client() as client:
            with client.session_transaction() as client_session:
                client_session['board'] = test_board_a
                client_session['total_score'] = 0
                client_session['high_score'] = 0
                client_session['words_used'] = []

            res = client.post('/guess', data={'word': 'log'})
            json_res = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(json_res['word'], 'not-on-board')
            self.assertEqual(json_res['high_score'], 0)
            self.assertEqual(json_res['total_score'], 0)

    def test_Boggle_make_board(self):
        board = boggle_game.make_board()

        self.assertIsInstance(board[0][0], str)
        self.assertEqual(len(board[0][0]), 1)
        self.assertEqual(len(board[0]), 5)
        self.assertEqual(len(board), 5)

    def test_Boggle_check_valid_word_board_a(self):
        self.assertEqual(boggle_game.check_valid_word(test_board_a, 'A'), 'ok')
        self.assertEqual(boggle_game.check_valid_word(test_board_a, 'a'), 'ok')
        self.assertEqual(boggle_game.check_valid_word(test_board_a, 'cat'),
                         'not-on-board')
        self.assertEqual(
            boggle_game.check_valid_word(test_board_a, 'asfdsfsd'), 'not-word')

    def test_Boggle_check_valid_word_board_b(self):
        self.assertEqual(boggle_game.check_valid_word(test_board_b, 'cat'),
                         'ok')
        self.assertEqual(boggle_game.check_valid_word(test_board_b, 'dog'),
                         'ok')
        self.assertEqual(boggle_game.check_valid_word(test_board_b, 'bite'),
                         'ok')
        self.assertEqual(boggle_game.check_valid_word(test_board_b, 'noon'),
                         'not-on-board')
        self.assertEqual(
            boggle_game.check_valid_word(test_board_b, 'asfdsfsd'), 'not-word')

    def test_Boggle_read_dict(self):
        words = boggle_game.read_dict('words.txt')

        self.assertIsInstance(words, list)
        self.assertIn('a', words)
        self.assertNotIn('assdfs', words)

    def test_validate_word(self):
        words_used = ['cat', 'dog']

        self.assertEqual(validate_word('cat', words_used, test_board_b),
                         ('already-guessed', ['cat', 'dog']))
        self.assertEqual(validate_word('bite', words_used, test_board_b),
                         ('ok', ['cat', 'dog', 'bite']))
        self.assertEqual(validate_word('kangaroo', words_used, test_board_b),
                         ('not-on-board', ['cat', 'dog', 'bite', 'kangaroo']))
        self.assertEqual(
            validate_word('noon', words_used, test_board_b),
            ('not-on-board', ['cat', 'dog', 'bite', 'kangaroo', 'noon']))
        self.assertEqual(
            validate_word('nopetynope', words_used, test_board_b),
            ('not-word',
             ['cat', 'dog', 'bite', 'kangaroo', 'noon', 'nopetynope']))

    def test_calculate_score(self):

        self.assertEqual(calculate_score('A', 'ok'), 1)
        self.assertEqual(calculate_score('cat', 'ok'), 3)
        self.assertEqual(calculate_score('kangaroo', 'ok'), 8)
        self.assertEqual(calculate_score('dog', 'not-on-board'), 0)
        self.assertEqual(calculate_score('nopety-nope', 'not-word'), 0)
        self.assertEqual(calculate_score('cat', 'already-guessed'), 0)

    def test_calculate_high_score(self):
        self.assertEqual(calculate_high_score(4, 5), 5)
        self.assertEqual(calculate_high_score(4, 4), 4)
        self.assertEqual(calculate_high_score(0, 4), 4)
        self.assertEqual(calculate_high_score(4, 0), 4)
