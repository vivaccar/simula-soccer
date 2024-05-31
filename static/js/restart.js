document.addEventListener('DOMContentLoaded', function(){
	var restartButton = document.getElementById('restart');
	
	restartButton.addEventListener('click', function(){
		localStorage.removeItem('generalData')
	})
})