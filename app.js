let ws = null;

function connect() {
  // Replace IP address with "localhost"
  let ip = document.getElementById("IP").value;
  ip = ip.replace(ip, "localhost");

  // Get username from input field
  let username = document.getElementById("username").value;

  // Open WebSocket connection
  ws = new WebSocket(`ws://${ip}:8765`);
  ws.onopen = function () {
    let main_login = document.getElementById("main_login");
    let main_view = document.getElementById("main_view");

    main_login.style.display = "none";
    main_view.style.display = "flex";

    console.log(`Connected to server at ws://${ip}:8765`);
    ws.send(username);
  };
  ws.onmessage = function (event) {
    console.log(`[+] Received message from server: ${event.data}`);
    // Check if message was sent by client
    if (event.data.startsWith(`[${username}]`)) {
      return;
    }
    // Check if message was sent by the server and add class to the message
    let messageClass = '';
    if (event.data.startsWith('[SERVER]')) {
      messageClass = 'class="server-message"';
    }
    // Update the viewport div with the received message
    document.getElementById('viewport').innerHTML += `<p ${messageClass}>${event.data}</p>`;
  };

  // Print an error message when the client cannot connect to the server
  ws.onerror = function () {
    let error_str = document.getElementById("error_str");
    error_str.innerText = "Server could not be found, please try again."
    console.log("WebSocket error occurred");
  };

  ws.onclose = function () {
    console.log("Connection to server closed");
  };
}

function send() {
  // Get message from input field
  let message = document.getElementById("message_input").value;

  // Get username from input field
  let username = document.getElementById("username").value;

  // Send message to server
  ws.send(message);
  console.log(`[+] Sent message to server: ${message}`);
  
  // Append the sent message as an HTML element to the viewport div
  let messageElement = document.createElement('p');
  messageElement.innerText = `[${username}]: ${message}`;
  document.getElementById('viewport').insertAdjacentElement('beforeend', messageElement);

  // Scroll the viewport to the bottom
  let viewport = document.getElementById('viewport');
  viewport.scrollTop = viewport.scrollHeight;

  // Clear the input field
  document.getElementById('message_input').value = '';
}

// Get the message input field
let messageInput = document.getElementById("message_input");

// Add an event listener to the message input field
messageInput.addEventListener("keypress", function(event) {
  // Check if the "Enter" key was pressed
  if (event.key === "Enter") {
    // Call the send() function
    send();
  }
});