document.addEventListener('DOMContentLoaded', function(){
	var nextRoundtButton = document.getElementById('next_round');
	
	nextRoundtButton.addEventListener('click', function(){
		window.Round += 1
		var numberOfTeams = JSON.parse(localStorage.getItem('generalData'))['teams'].length;
		var lastRound = (numberOfTeams - 1) * 2
		if (window.Round == lastRound)
			document.getElementById('next_round').disabled = true;
		else if (window.Round == 2)
			document.getElementById('prev_round').disabled = false;
		printGamesRound(window.Round)
	})
})