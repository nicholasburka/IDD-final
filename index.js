var mqtt = require('paho-mqtt');

console.log(mqtt)

//from https://www.npmjs.com/package/paho-mqtt
client = new mqtt.Client('farlab.infosci.cornell.edu', Number(8883), "clientId");

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

client.connect({onSuccess:onConnect});

var this_net_id = 0;
const net_id_length = 5;

//from https://stackoverflow.com/questions/1349404/generate-random-string-characters-in-javascript
function rand_id(length) {
	var result = '';
	var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
	var charactersLength = characters.length;
	for ( var i = 0; i < length; i++ ) {
		result += characters.charAt(Math.floor(Math.random()*charactersLength));
	}
	return result;
}

function onConnect() {
	client.subscribe('oldphone-handshake');
	this_net_id = rand_id(net_id_length);
	message = new mqtt.Message(this_net_id);
	message.destinationName = 'oldphone-handshake';
	client.send(message);
}

function onMessageArrived(message) {
	console.log("onMessageArrived"+message.payloadString);
	//if two devices respond at same time
	if (message.payload.substr(0,net_id_length) === this_net_id) {
		console.log("received handshake netid conf from server");
		client.unsubscribe('oldphone-handshake');
		client.subscribe(this_net_id);
	}
}

function onConnectionLost(responseObject) {
	if (responseObject.errorCode !== 0) {
		console.log("onConnectionLost:"+responseObject.errorMessage);
	}
	else {
		console.log("onConnectionLost:");
		console.log(responseObject);
	}
}

