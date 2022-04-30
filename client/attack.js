async function attack() {
  // make a loop here
  let padding = "";
  let url =  "http://127.0.0.1:5001/part1?param=";
  let originalLength = 0
  let BLOCK_SIZE = 16
  let fillLength = 0;
  while(true)
  {
      let part1Url = url + padding
      let response = await makeRequest(part1Url,
        { param: "" }
      );
      response = Number(response);

      if(originalLength > 0 && response > originalLength)
      {
        break;
      }

      if(response > 0)
      {
        originalLength = response;
      }
      padding += "A";
      fillLength++;
      console.log(fillLength);
  }
  console.log(fillLength);
  let guessedSecret = "";
  url = "http://127.0.0.1:5001/part2?param=";


  // paddingFront = "A".repeat(BLOCK_SIZE) + "#".repeat(fillLength);
  // let paddedUrl = url+paddingFront;
  // let body = "B".repeat(BLOCK_SIZE);
  // response2 = await sendRequest(paddedUrl, {param: body});

  for(var block = Math.floor(originalLength/32) -2; block > 0; block -=1)
  {
    for(var i = 0; i < BLOCK_SIZE; i++)
    {
      let response2 = "Failure"
      while(response2 == "Failure")
      {
        paddingFront = "A".repeat(BLOCK_SIZE + i) + "#".repeat(fillLength);
        let paddedUrl = url+paddingFront;
        let body = "B".repeat(BLOCK_SIZE - i);
        response2 = await sendRequest(paddedUrl, {param: body});
        if(response2 == "#"){
          return;
        }
      }
      guessedSecret = response2 + guessedSecret;
      console.log(guessedSecret)
    }
  }
  console.log(guessedSecret);

}


attack();
