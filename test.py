from unittest import TestCase
from app import app, validate_word, calculate_score, boggle_game
from flask import session
from boggle import Boggle

test_board = [
    ['A', 'A', 'A', 'A', 'A'],
    ['A', 'A', 'A', 'A', 'A'],
    ['A', 'A', 'A', 'A', 'A'],
    ['A', 'A', 'A', 'A', 'A'],
    ['A', 'A', 'A', 'A', 'A'],
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
                client_session['board'] = test_board
                client_session['total_score'] = 0
                client_session['word_score'] = 0
                client_session['high_score'] = 0
                client_session['words_used'] = []

            res = client.post('/guess', data={'word': 'A'})
            json_res = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(json_res['word'], 'ok')
            self.assertEqual(json_res['high_score'], 1)
            self.assertEqual(json_res['total_score'], 1)
            self.assertEqual(json_res['word_score'], 1)

    def test_Boggle_make_board(self):
        board = boggle_game.make_board()

        self.assertIsInstance(board[0][0], str)
        self.assertEqual(len(board[0][0]), 1)
        self.assertEqual(len(board[0]), 5)
        self.assertEqual(len(board), 5)

    def test_Boggle_check_valid_word(self):
        self.assertEqual(boggle_game.check_valid_word(test_board, 'A'), 'ok')
        self.assertEqual(boggle_game.check_valid_word(test_board, 'a'), 'ok')
        self.assertEqual(boggle_game.check_valid_word(test_board, 'cat'),
                         'not-on-board')
        self.assertEqual(boggle_game.check_valid_word(test_board, 'asfdsfsd'),
                         'not-word')

    def test_Boggle_read_dict(self):
        words = boggle_game.read_dict('words.txt')

        self.assertIsInstance(words, list)
        self.assertIn('a', words)
        self.assertNotIn('assdfs', words)