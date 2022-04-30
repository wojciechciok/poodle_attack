const KEY = "secret_key_11111";
const IV = "secret_key_11111";
const BLOCK_SIZE = 16;
const TOKEN = "super_secret_cookie";
let keyUrl = "http://127.0.0.1:5002/key";
let currentKey = KEY;
let currentIV = IV;

function encrypt(plaintext) {
  const mac = sha256.hmac(currentKey, plaintext);
  const message = encode(plaintext) + mac;
  const paddedMessage = addPadding(message);
  return AES(paddedMessage);
}

function addPadding(message) {
  const zero = 0;
  const messageLen = message.length / 2;
  const paddingLen = BLOCK_SIZE - (messageLen % BLOCK_SIZE);
  const lastByte = paddingLen.toString(16);
  const result = message +
    zero.toString(16).repeat((paddingLen - 1) * 2) +
    (paddingLen > 9 ? lastByte : "0" + lastByte);
  return result;
}

function AES(text) {
  // An example 128-bit key (16 bytes * 8 bits/byte = 128 bits)
  // var key = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16];
  //const key = aesjs.utils.utf8.toBytes(KEY);
  // Convert text to bytes
  const textBytes = hexToBytes(text);

  const keyBytes = aesjs.utils.utf8.toBytes(currentKey);
  const ivBytes = aesjs.utils.utf8.toBytes(currentIV);
  // The counter is optional, and if omitted will begin at 1
  const aesCbc = new aesjs.ModeOfOperation.cbc(keyBytes, ivBytes);
  const encryptedBytes = aesCbc.encrypt(textBytes);

  // To print or store the binary data, you may convert it to hex
  const encryptedHex = aesjs.utils.hex.fromBytes(encryptedBytes);
  return encryptedHex;
}

function encode(str) {
  var arr1 = [];
  for (var n = 0, l = str.length; n < l; n++) {
    var hex = Number(str.charCodeAt(n)).toString(16);
    arr1.push(hex);
  }
  return arr1.join("");
}

function hexToSting(str) {
	var hex  = str.toString();
	var result = '';
	for (var n = 0; n < hex.length; n += 2) {
		result += String.fromCharCode(parseInt(hex.substr(n, 2), 16));
	}
	return result;
}

function hexToBytes(hex) {
  for (var bytes = [], c = 0; c < hex.length; c += 2)
    bytes.push(parseInt(hex.substr(c, 2), 16));
  return bytes;
}

function toHexString(byteArray) {
  return Array.from(byteArray, function(byte) {
    return ('0' + (byte & 0xFF).toString(16)).slice(-2);
  }).join('')
}


async function sendRequest(url, body) {
  let keyResponse = await fetch(keyUrl, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  let keyObject = await keyResponse.json();
  currentKey = keyObject.key;
  currentIV = keyObject.iv;
  let response = await makeRequest(url, body);
  return response;
}



// attacker has access to this function
async function makeRequest(url, body) {
  let message = url + TOKEN + body.param;
  let encrypted = encrypt(message);
  response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: encrypted }),
  });
  let text = await response.text();
  return text;
}
