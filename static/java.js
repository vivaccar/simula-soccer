// 1) ao enviar o formulario, armazenar o resultado do jogo(home_goals e away_goals)
// 2) recalcular a tabela com os valores simulados

var data = JSON.parse(localStorage.getItem('data')) || []

document.addEventListener('DOMContentLoaded', function() {
	var homeGoalsInput = document.getElementById('home_goals_{{ game.id }}');
	var awayGoalsInput = document.getElementById('away_goals_{{ game.id }}');
	var form = document.getElementById('form_{{ game.id }}');

	homeGoalsInput.addEventListener('input', function() {
		checkInputs();
	});

	awayGoalsInput.addEventListener('input', function() {
		checkInputs();
	});

	function checkInputs() {
		if (homeGoalsInput.value !== '' && awayGoalsInput.value !== '') {
			game = {'game_id': '{{ game.id }}',
			'home_team': '{{ game.home_team.name }}',
			'home_goals':  homeGoalsInput.value,
			'away_team': '{{ game.away_team.name }}',
			'away_goals':  awayGoalsInput.value
			}
			data.push(game);
			localStorage.setItem('data', JSON.stringify(data));
			form.submit();
		}
	}
})