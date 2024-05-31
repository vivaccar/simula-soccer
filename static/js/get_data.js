function getCurrentRound(){
	let currentTime = Date.now() / 1000 //transormo de milissegundos para segundos(unidade de medida dos timestamps dos games)
	var allGames = JSON.parse(localStorage.getItem('generalData'))['games']
	var curGameTime = 0
	var curRound = 1
	allGames.forEach((game, index) => {
		if ((game.timestamp) > currentTime  && ((game.timestamp) < curGameTime || curGameTime == 0)){
			curGameTime = game.timestamp
			curRound = game.round
	}})
	return (curRound)
}

const l_id = league_id
document.addEventListener('DOMContentLoaded', (event) => {
	getGeneralData()
})
function getCSRFToken() {
	return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
function getGeneralData() {
	console.log(l_id)
	fetch('get_data', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
			'X-CSRFToken': getCSRFToken(),
		},
		body: new URLSearchParams({ 'league_id': l_id }).toString(),
	})
	.then(response => response.json())
	.then(data => {
	const generalDataJson = JSON.stringify(data);
	localStorage.setItem('generalData', generalDataJson);
	window.Round = getCurrentRound();
	printGamesRound(window.Round)
})
}