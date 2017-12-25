$(document).ready(function() {
	$("#button-refresh").on("click", refresh);
	$("#button-transfer").on("click", transfer);
	$('.ui.dropdown').dropdown();

	$("#button-receive").on("click", receiveBank);

	$("#button-free-parking").on("click", receiveFreeParking);

	refresh();
});

function transfer() {
	let gameID = window.location.pathname.split("/")[2];
	let playerID = sessionStorage.getItem("playerID");
	let recipientID = $('#transfer-recipients').dropdown("get value");
	let amount = $("#transfer-amount").val();

	let transferURL = "/api/v1/game/transfer/";
	let data = {
		"gameID": gameID,
		"playerID": playerID,
		"recipientID": recipientID,
		"amount": amount
	};

	Promise.resolve($.post(transferURL, data))
	.then(function(response) {
		if (response.status != "success") {
			console.log("Something went wrong in transfer.");
		}
	})
	.finally(function() {
		refresh();
	});
}

function receiveBank() {
	let gameID = window.location.pathname.split("/")[2];
	let playerID = sessionStorage.getItem("playerID");
	let amount = $("#receive-amount").val();

	let bankURL = "/api/v1/game/bank/";
	let data = {
		"gameID": gameID,
		"playerID": playerID,
		"amount": amount
	};

	Promise.resolve($.post(bankURL, data))
	.then(function(response) {
		if (response.status != "success") {
			console.log("Something went wrong in transfer.");
		}
	})
	.finally(function() {
		refresh();
	});
}

function receiveFreeParking() {
	let gameID = window.location.pathname.split("/")[2];
	let playerID = sessionStorage.getItem("playerID");

	let freeParkingURL = "/api/v1/game/freeparking/";
	let data = {
		"gameID": gameID,
		"playerID": playerID
	};

	Promise.resolve($.post(freeParkingURL, data))
	.then(function(response) {
		if (response.status != "success") {
			console.log("Something went wrong in transfer.");
		}
	})
	.finally(function() {
		refresh();
	});
}

function refresh() {
	$("#button-refresh").addClass("loading disabled");

	let playerID = sessionStorage.getItem("playerID");
	let gameID = window.location.pathname.split("/")[2];

	let refreshGameURL = "/api/v1/game/refresh/";
	let data = {
		gameID: gameID
	};

	Promise.resolve($.post(refreshGameURL, data))
	.then(function(response) {
		if (response.status == "success") {
			$("#table-players tbody tr").remove();
			let tableBody = $("#table-players tbody");

			$("#options-transfer div").remove();
			let transferOptions = $("#options-transfer");
			transferOptions.append($('<div class="item" data-value="-1">').text("Bank"));
			transferOptions.append($('<div class="item" data-value="-2">').text("Free parking"));

			$("#free-parking").text(formatHoldings(response.data.freeParking));

			response.data.players.forEach(function(player) {
				if (playerID == player.cookie) {
					$("#player").text(player.name);
					$("#holdings").text(formatHoldings(player.holdings));
				} else {
					tableBody.append($('<tr>')
						.append($('<td class="center aligned">').text(player.name))
						.append($('<td class="center aligned">').text(formatHoldings(player.holdings)))
					);

					transferOptions.append(
						$('<div class="item" data-value="' + player.cookie + '">').text(player.name)
					);
				}
			});
		}
	})
	.finally(function() { // Reset values
		$("#transfer-amount").val("");
		$('#transfer-recipients').dropdown("restore defaults");

		$("#receive-amount").val("");

		$("#button-refresh").removeClass("loading disabled");
	});
}

function formatHoldings(raw) {
	return "$" + raw.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
