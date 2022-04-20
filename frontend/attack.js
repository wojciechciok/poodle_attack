const KEY = "secret_key_11111";
const BLOCK_SIZE = 16;

async function encrypt(plaintext) {
  const mac = sha256.hmac(KEY, plaintext);
  const message = encode(plaintext) + mac;
  const paddedMessage = addPadding(message);
  AES(paddedMessage);
}

function addPadding(message) {
  const zero = 0;
  const messageLen = message.length / 2;
  const paddingLen = BLOCK_SIZE - (messageLen % BLOCK_SIZE);
  const lastByte = paddingLen.toString(16);
  const result =
    message + zero.toString(16).repeat(paddingLen * 2 - 1) + lastByte;
  return result;
}

function AES(text) {
  // An example 128-bit key (16 bytes * 8 bits/byte = 128 bits)
  // var key = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16];
  const key = aesjs.utils.utf8.toBytes(KEY);
  // Convert text to bytes
  const textBytes = hexToBytes(text);

  // The counter is optional, and if omitted will begin at 1
  const aesCbc = new aesjs.ModeOfOperation.cbc(key, key);
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

function hexToBytes(hex) {
  for (var bytes = [], c = 0; c < hex.length; c += 2)
    bytes.push(parseInt(hex.substr(c, 2), 16));
  return bytes;
}

encrypt("okok");
