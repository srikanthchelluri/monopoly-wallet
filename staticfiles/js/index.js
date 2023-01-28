$(document).ready(function() {
	$("#button-start-game").on("click", startGame);
	$("#button-join-game").on("click", joinGame);
});

function startGame() {
	resetPlayerID();

	let playerName = getPlayerName();
	if (playerName == null) { return; }

	let createGameURL = "/api/v1/game/create/";
	let data = {
		"playerID": sessionStorage.getItem("playerID"),
		"playerName": playerName
	};

	Promise.resolve($.post(createGameURL, data))
	.then(function(response) {
		if (response.status == "success") {
			let gameID = response.data.gameID;
			window.location = '/game/' + gameID;
		}
	});
}

function joinGame() {
	resetPlayerID();

	let gameID = $("#input-join-game").val();

	let playerName = getPlayerName();
	if (playerName == null) { return; }

	let joinGameURL = "/api/v1/game/join/";
	let data = {
		"gameID": gameID,
		"playerID": sessionStorage.getItem("playerID"),
		"playerName": playerName
	};

	Promise.resolve($.post(joinGameURL, data))
	.then(function(response) {
		if (response.status == "success") {
			window.location = '/game/' + gameID;
		}
	});
}

// Helper methods
function resetPlayerID() {
	sessionStorage.removeItem("playerID");
	let randomPlayerID = Math.floor(Math.random() * 10**16);
	sessionStorage.setItem("playerID", randomPlayerID);
}

function getPlayerName() {
	let playerName = $("#input-name").val();
	if (playerName.length > 16) {
		return null;
	} else {
		return playerName;
	}
}