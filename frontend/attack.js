function doAttack() {
  console.log("attacking...");
}

const KEY = "secret_key";
const BLOCK_SIZE = 16;

async function encrypt(plaintext) {
  const data = encode(plaintext);
  const mac = await hmacSha256Hex(KEY, data);
  const message = data + mac;
  paddedMessage = addPadding(message);
}

function addPadding(message) {
  const zero = 0;
  const messageLen = message.length;
  const paddingLen = BLOCK_SIZE - (messageLen % BLOCK_SIZE);
  const lastByte = paddingLen.toString(16);
  const result = message + zero.toString(16).repeat(paddingLen - 1) + lastByte;
  console.log(result);
  console.log(message);
}

encrypt("okok");

// def add_padding(message):
//     message_len = len(message)
//     padding_len = BLOCK_SIZE - (message_len % BLOCK_SIZE)
//     last_byte = padding_len.to_bytes(1, 'big')
//     result = message + bytes([0] * (padding_len - 1)) + last_byte
//     return result

// data = plaintext.encode()
// mac = hmac.new(KEY, data, hashlib.sha256).digest()
// message = data + mac
// padded_message = add_padding(message)
// aes = AES.new(KEY, AES.MODE_CBC, IV)
// return aes.encrypt(padded_message)

async function hmacSha256Hex(secret, message) {
  const enc = new TextEncoder("utf-8");
  const algorithm = { name: "HMAC", hash: "SHA-256" };
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    algorithm,
    false,
    ["sign", "verify"]
  );
  const hashBuffer = await crypto.subtle.sign(
    algorithm.name,
    key,
    enc.encode(message)
  );
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  return hashHex;
}

function encode(str) {
  var arr1 = [];
  for (var n = 0, l = str.length; n < l; n++) {
    var hex = Number(str.charCodeAt(n)).toString(16);
    arr1.push(hex);
  }
  return arr1.join("");
}

doAttack();
