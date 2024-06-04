var data = [];

function printGamesRound(round) {
	printRound()
	console.log("entrou na print round");
	var gamesContainer = document.getElementById("gamesContainer");
	var allGames = JSON.parse(localStorage.getItem('generalData'))['games'];
	console.log("all games: ", allGames);
	var allTeams = JSON.parse(localStorage.getItem('generalData'))['teams'];
	var gamesRound = allGames.filter((game) => game['round'] == round);
	gamesRound = gamesRound.sort((a, b) => a['timestamp'] - b['timestamp']);
	console.log("games round:", gamesRound);

	gamesContainer.innerHTML = '';
	gamesRound.forEach((game, index) => {
		var home_team = allTeams.find((team => team.name == game.home_team));
		var away_team = allTeams.find((team => team.name == game.away_team));
		var formHTML = `
	<form id="form_${game.game_id}">
	<div style="align-items: center; text-align: center; border:1px solid gainsboro;">
		<div>
			<br>
			<input type="hidden" name="home_team" value="${game.home_team}">
			<input type="hidden" name="away_team" value="${game.away_team}">
			<input type="hidden" name="game_id" value="${game.game_id}">
			<img src="${home_team.logo}" alt="" height="7%" width="7%">
			<input type="number" ${game.real_played ? 'disabled' : ''} name="home_goals" id="home_goals_${game.game_id}" min="0" max="9" value="${game.home_goals != null ? game.home_goals : ''}">
			X
			<input type="number" ${game.real_played ? 'disabled' : ''} name="away_goals" id="away_goals_${game.game_id}" min="0" max="9" value="${game.away_goals != null ? game.away_goals : ''}">
			<img src="${away_team.logo}" alt="" height="7%" width="7%">
			<p style="font-size: 12px;">${game.stadium} - ${game.local_time}</p>
		</div>
	</div>
	</form>`;
		gamesContainer.innerHTML += formHTML;
	});

	eventListener(gamesRound);
}

function eventListener(gamesRound) {
	gamesRound.forEach((game) => {
		var homeGoalsInput = document.getElementById(`home_goals_${game.game_id}`);
		var awayGoalsInput = document.getElementById(`away_goals_${game.game_id}`);

		homeGoalsInput.addEventListener('input', function () {
			checkInputs(game, homeGoalsInput, awayGoalsInput);
		});

		awayGoalsInput.addEventListener('input', function () {
			checkInputs(game, homeGoalsInput, awayGoalsInput);
		});
	});
}

function checkInputs(game, homeGoalsInput, awayGoalsInput) {
	if (homeGoalsInput.value !== '' && awayGoalsInput.value !== '' && homeGoalsInput.value >= 0 && awayGoalsInput.value >= 0) {
		game['home_goals'] = homeGoalsInput.value
		game['away_goals'] = awayGoalsInput.value
		let GameIdToFind = game.game_id;
		console.log("gameIdToFind: ", GameIdToFind);
		var generaldata = JSON.parse(localStorage.getItem('generalData'));
		var gamesList = generaldata['games']
		var foundGame = gamesList.find(object => object['game_id'] == GameIdToFind);
		console.log("jogo encontrado: ", foundGame)
		console.log("simulated jogo encontrado: ", foundGame['simulated'])
		if (foundGame['simulated']) {
			resetTeamsVariables(foundGame, generaldata);
		}
		exec_game(game, generaldata);
		print_table(generaldata);
	}
}

function resetTeamsVariables(game, generaldata) {
	console.log("entrou na resetTeams")
	let gameLocalStorage = generaldata['games'].find(object => object['game_id'] == game.game_id)
	console.log("game do ls", gameLocalStorage)
	let home_team = generaldata['teams'].find(team => team.name == game['home_team'])
	let away_team = generaldata['teams'].find(team => team.name == game['away_team'])
	home_team.games_played -= 1
	away_team.games_played -= 1
	home_team.goals_pro -= parseInt(game['home_goals'])
	home_team.goals_con -= parseInt(game['away_goals'])
	home_team.sg -= parseInt(game['home_goals']) - parseInt(game['away_goals'])
	away_team.goals_pro -= parseInt(game['away_goals'])
	away_team.goals_con -= parseInt(game['home_goals'])
	away_team.sg -= parseInt(game['away_goals']) - parseInt(game['home_goals'])
	if (parseInt(game['home_goals']) > parseInt(game['away_goals'])) {
		home_team.points -= 3
		home_team.wins -= 1
		away_team.loss -= 1
	}
	if (parseInt(game['home_goals']) == parseInt(game['away_goals'])) {
		home_team.points -= 1
		away_team.points -= 1
		home_team.draws -= 1
		away_team.draws -= 1
	}
	if (parseInt(game['away_goals']) > parseInt(game['home_goals'])) {
		away_team.points -= 3
		away_team.wins -= 1
		home_team.loss -= 1
	}
	gameLocalStorage['simulated'] = false
	gameLocalStorage['home_goals'] = null
	gameLocalStorage['away_goals'] = null
	localStorage.setItem('generalData', JSON.stringify(generaldata));
}

function ft_sort_table(generalData) {
	console.log("sort")
	console.log("general", generalData['league_data'])
	if (generalData['league_data']['id'] == 39) {
		generalData['teams'].sort((a, b) => {
			if (a.points != b.points) {
				return b.points - a.points;
			} else {
				if (a.sg != b.sg) {
					return b.sg - a.sg;
				} else {
					return b.goals_pro - a.goals_pro;
				}
			}
		});
	}
	else if (generalData['league_data']['league_id'] == 71 || generalData['league_data']['league_id'] == 72) {
		generalData['teams'].sort((a, b) => {
			console.log("br")
			if (a.points != b.points) {
				return b.points - a.points;
			} else {
				if (a.wins != b.wins) {
					return b.wins - a.wins;
				} else {
					if (a.sg != b.sg)
						return b.sg - a.sg;
					else {
						return b.goals_pro
					}
				}
			}
		});
	}
	else if (generalData['league_data']['name'] == 'Bundesliga') {
		generalData['teams'].sort((a, b) => {
			if (a.points != b.points) {
				return b.points - a.points;
			} else {
				if (a.sg != b.sg) {
					return b.sg - a.sg;
				} else {
					return b.goals_pro - a.goals_pro;
				}
			}
		});
	}
	else if (generalData['league_data']['name'] == 'La Liga' || generalData['league_data']['name'] == 'Serie A') {
		console.log("entrou")
		generalData['teams'].sort((a, b) => {
			if (b.points != a.points) {
				return b.points - a.points;
			} else {
				return (desempate(a, b, generalData['games']))
			}
		})
	}
}
function exec_game(game, generaldata) {
	let gameLocalStorage = generaldata['games'].find(object => object['game_id'] == game.game_id)
	var home_team = game['home_team'];
	var away_team = game['away_team'];
	var home_team_data = generaldata['teams'].find(team => team.name === home_team);
	var away_team_data = generaldata['teams'].find(team => team.name === away_team);
	gameLocalStorage['simulated'] = true
	home_team_data.goals_pro += parseInt(game['home_goals']);
	home_team_data.goals_con += parseInt(game['away_goals']);
	home_team_data.sg += parseInt(game['home_goals']) - parseInt(game['away_goals']);
	home_team_data.games_played += 1;
	away_team_data.goals_pro += parseInt(game['away_goals']);
	away_team_data.goals_con += parseInt(game['home_goals']);
	away_team_data.sg += parseInt(game['away_goals']) - parseInt(game['home_goals']);
	away_team_data.games_played += 1;
	if (parseInt(game['home_goals']) > parseInt(game['away_goals'])) {
		home_team_data.points += 3;
		home_team_data.wins += 1;
		away_team_data.loss += 1;
	} else if (parseInt(game['home_goals']) == parseInt(game['away_goals'])) {
		home_team_data.draws += 1;
		away_team_data.draws += 1;
		home_team_data.points += 1;
		away_team_data.points += 1;
	} else {
		away_team_data.points += 3;
		away_team_data.wins += 1;
		home_team_data.loss += 1;
	}
	gameLocalStorage['home_goals'] = parseInt(game['home_goals'])
	gameLocalStorage['away_goals'] = parseInt(game['away_goals'])
	home_team_data.aproveitamento = ((home_team_data.points / (home_team_data.games_played * 3)) * 100).toFixed(1);
	away_team_data.aproveitamento = ((away_team_data.points / (away_team_data.games_played * 3)) * 100).toFixed(1);
	ft_sort_table(generaldata)
	localStorage.setItem('generalData', JSON.stringify(generaldata));
	console.log("depois de exec game");
}

function desempate(team_a, team_b, gamesList) {
	console.log("ENTROU NO DESEMPATE")
	var game_1 = gamesList.find(game => game.home_team == team_a.name && game.away_team == team_b.name)
	var game_2 = gamesList.find(game => game.home_team == team_b.name && game.away_team == team_a.name)
	console.log("game 1:", game_1)
	console.log("game 2:", game_2)
	var team_a_goals = parseInt(game_1['home_goals'] != null ? game_1['home_goals'] : 0) + parseInt(game_2['away_goals'] != null ? game_2['away_goals'] : 0)
	var team_b_goals = parseInt(game_1['away_goals'] != null ? game_1['away_goals'] : 0) + parseInt(game_2['home_goals'] != null ? game_2['home_goals'] : 0)
	console.log("team a gols:", team_a_goals)
	console.log("team b gols:", team_b_goals)
	if (team_a_goals == team_b_goals)
		return (team_b.sg - team_a.sg)
	return (team_b_goals - team_a_goals)
}

function print_table(generaldata) {
	console.log("entrou na print tableeeeeee")
	const tbody = document.querySelector('tbody')
	tbody.innerHTML = ''
	generaldata['teams'].forEach((team, index) => {
		const row = document.createElement('tr');
		row.id = `team_row_${team.id_name}`;
		let backgroundColor = '';
		let textColor = 'black';

		if (index + 1 <= generaldata['league_data']['zone_1']) {
			backgroundColor = 'green';
			textColor = 'white';
		} else if (generaldata['league_data']['zone_2'] && index + 1 <= generaldata['league_data']['zone_2']) {
			backgroundColor = 'blue';
			textColor = 'white';
		} else if (generaldata['league_data']['zone_3'] && index + 1 <= generaldata['league_data']['zone_3']) {
			backgroundColor = 'rgb(199, 186, 0)';
			textColor = 'white'
		} else if (index + 1 >= generaldata['league_data']['zone_reb']) {
			backgroundColor = 'red';
			textColor = 'white'
		}
		row.innerHTML = `	
			<td class="text-center mb-4" style="background-color: ${backgroundColor}; color: ${textColor};"><strong>${index + 1}</strong></td>
			<td><img src="${team.logo}" alt="" width="13%" height="13%"> ${team.name}</td>
			<td class="text-center mb-4"><strong>${team.points}</strong></td>
			<td class="text-center mb-4">${team.games_played}</td>
			<td class="text-center mb-4">${team.wins}</td>
			<td class="text-center mb-4">${team.draws}</td>
			<td class="text-center mb-4">${team.loss}</td>
			<td class="text-center mb-4">${team.goals_pro}</td>
			<td class="text-center mb-4">${team.goals_con}</td>
			<td class="text-center mb-4">${team.sg}</td>
			<td class="text-center mb-4">${team.aproveitamento}%</td>
			`;
		tbody.appendChild(row);
	})
}

