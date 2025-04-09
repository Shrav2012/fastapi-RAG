let token = null;
const loginBtn = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signupBtn");
const logoutBtn = document.getElementById("logoutBtn");
const uploadBtn = document.getElementById("uploadBtn");
const chatForm = document.getElementById("chatForm");

const authSection = document.getElementById("authSection");
const uploadSection = document.getElementById("uploadSection");
const chatSection = document.getElementById("chatSection");
const loader = document.getElementById("loader");
const chatHistory = document.getElementById("chatHistory");
const docList = document.getElementById("docList");
const docHistory = document.getElementById("docHistory");
const toggleTheme = document.getElementById("toggleTheme");

const backendURL = "http://localhost:8000"; // change if hosted elsewhere

function showAppUI() {
  authSection.classList.add("hidden");
  uploadSection.classList.remove("hidden");
  chatSection.classList.remove("hidden");
  logoutBtn.classList.remove("hidden");
  docHistory.classList.remove("hidden");
}

function resetUI() {
  token = null;
  authSection.classList.remove("hidden");
  uploadSection.classList.add("hidden");
  chatSection.classList.add("hidden");
  logoutBtn.classList.add("hidden");
  docHistory.classList.add("hidden");
  chatHistory.innerHTML = "";
  docList.innerHTML = "";
}

logoutBtn.onclick = () => resetUI();

loginBtn.onclick = async () => {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const form = new URLSearchParams();
  form.append("username", username);
  form.append("password", password);

  const res = await fetch(`${backendURL}/token`, {
    method: "POST",
    body: form
  });

  const data = await res.json();
  if (res.ok) {
    token = data.access_token;
    showAppUI();
  } else {
    alert("Login failed");
  }
};

signupBtn.onclick = () => {
  alert("Signup is mocked. Use username: testuser, password: testpass");
};

uploadBtn.onclick = async () => {
  const fileInput = document.getElementById("uploadInput");
  const file = fileInput.files[0];
  if (!file) return alert("Please choose a file.");

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${backendURL}/upload`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: formData
  });

  const data = await res.json();
  if (res.ok) {
    const li = document.createElement("li");
    li.textContent = `${file.name} - ${new Date().toLocaleString()}`;
    docList.appendChild(li);
    alert("File uploaded successfully!");
  } else {
    alert("Upload failed");
  }
};

chatForm.onsubmit = async (e) => {
  e.preventDefault();
  const query = document.getElementById("queryInput").value;
  if (!query.trim()) return;

  const userMsg = document.createElement("div");
  userMsg.innerHTML = `<p class='font-medium'>You (${new Date().toLocaleTimeString()}):</p><p>${query}</p>`;
  chatHistory.appendChild(userMsg);

  loader.classList.remove("hidden");
  const form = new URLSearchParams();
  form.append("query", query);

  const res = await fetch(`${backendURL}/query`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: form
  });

  const data = await res.json();
  loader.classList.add("hidden");

  const aiMsg = document.createElement("div");
  aiMsg.innerHTML = `<p class='text-blue-600 font-medium'>AI (${new Date().toLocaleTimeString()}):</p><p>${data.answer}</p>`;
  chatHistory.appendChild(aiMsg);

  document.getElementById("queryInput").value = "";
};

// Dark Mode Toggle
if (toggleTheme) {
  toggleTheme.addEventListener("click", () => {
    document.documentElement.classList.toggle("dark");
    document.body.classList.toggle("bg-gray-900");
    document.body.classList.toggle("text-white");
  });
}
