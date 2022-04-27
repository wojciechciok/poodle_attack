async function attack() {
  // make a loop here
  let response = await makeRequest(
    "http://127.0.0.1:5001/part2?param=AAAAAAA",
    { param: "BBBBBBB" }
  );
  console.log(response);
}

attack();
