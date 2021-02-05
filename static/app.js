
//Sets up game for 60 second timer
let gameStillGoing = true;
setTimeout(function () {
    gameStillGoing = false;
    responseToHuman("game-over", "")
}, 60000)

$("#form").on("submit", async function (e) {
    e.preventDefault();
    if (gameStillGoing) {

        const $word = $("#word").val();

        const submit_form = new FormData();
        submit_form.append('word', $word)

        const response = await axios.post(`/guess`, submit_form);

        responseToHuman(response.data.word, $word, response.data.word_score)
        updateStats(response.data.total_score, response.data.high_score)
        $('#word').val('')
    }
})

function responseToHuman(phrase, word, score) {
    const $wordResponse = $("#wordResponse");
    translation = {
        "ok": ` is worth ${score} points`,
        "not-on-board": " isn't on the board",
        "not-word": " isn't  in our dictionary",
        "game-over": "Time's up, please play again",
        "already-guessed": " has already been guessed"
    }

    $wordResponse.html('')
    $wordResponse.append(`<h4>${word.toUpperCase()}${translation[phrase]}</h4>`)
}

function updateStats(score, highScore) {
    $('#score').text(score)
    $('#highScore').text(highScore)
}