function printRound(){
	let roundHTML = `<h4 style="font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;">RODADA ${window.Round}</h4>`
	document.getElementById('round_container').innerHTML = roundHTML
	document.getElementById('prev_round').disabled = (window.Round == 1)
}

document.addEventListener('DOMContentLoaded', function(){
	var prevRoundtButton = document.getElementById('prev_round');

	prevRoundtButton.addEventListener('click', function(){
		window.Round -= 1
		var numberOfTeams = JSON.parse(localStorage.getItem('generalData'))['teams'].length;
		var numberOfRounds = (numberOfTeams - 1) * 2
		if (window.Round == 1)
			document.getElementById('prev_round').disabled = true;
		else if (window.Round == numberOfRounds - 1)
			document.getElementById('next_round').disabled = false;
		printGamesRound(window.Round)
	})
})