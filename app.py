from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "jinja"

boggle_game = Boggle()


@app.route('/')
def start_game():
    """Initialize game and variables for the session when you hit the root route

    Returns:
        Renders the game.html template
    """
    session['board'] = boggle_game.make_board()
    session['total_score'] = 0
    session['games_played'] = session.get('games_played', 0) + 1
    session['high_score'] = session.get('high_score', 0)
    session['words_used'] = []
    return render_template("game.html")


@app.route('/guess', methods=["POST"])
def check_guess():
    """Gets a word from user and checks it against board with validate_word method
    then calls calculate score to calculate word score, total score and high score
    Return to app.js to add to board
        [json]: ({
        "word": validated_word,
        "total_score": session['total_score'],
        "word_score": session['word_score'],
        "high_score": session['high_score'],
    })
    """
    word = request.form['word']

    validated_word, session['words_used'] = validate_word(
        word, session['words_used'], session['board'])
    word_score = calculate_score(word, validated_word)
    session['high_score'] = calculate_high_score(session['total_score'],
                                                 session['high_score'])

    return jsonify({
        "word": validated_word,
        "total_score": session['total_score'],
        "word_score": word_score,
        "high_score": session['high_score'],
    })


def calculate_score(word, phrase):
    """Calculated word score based on length of word and return score

    Args:
        word (string): word as guess from user
        phrase (string): phrase generated by Boggle.check_valid_word class method
    """
    if phrase == "ok":
        return len(word)
    else:
        return 0


def calculate_high_score(total_score, high_score):
    """Calculate and returns high score whether its bigger than current game score or not

    Args:
        total_score (num): total for the game
        high_score (num): high score for the user

    Returns:
        num: greater of the 2 numbers
    """
    if total_score > high_score:
        return total_score
    else:
        return high_score


def validate_word(word, words_used, board):
    """checks to see if word has been guessed before and if not then calls method
    check_valid_word to see if word is on the gameboard

    Args:
        word (string): word guess from user

    Returns:
        string: already-guessed if word has been guessed before
                ok if valid word on board
                not-on-board if valid word thats not on the board
                not-word if not a word in the dictionary
    """
    if word in words_used:
        return 'already-guessed', words_used
    else:
        words_used.append(word)
        return boggle_game.check_valid_word(board, word), words_used
