const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const messagesArea = document.getElementById("messages");
const chatForm = document.getElementById("chat-form");
const presetsContainer = document.getElementById("presets");
const panelTitle = document.getElementById("panel-title");
const panelDesc = document.getElementById("panel-desc");
const optionBtns = Array.from(document.querySelectorAll(".option-btn"));
const newChatBtn = document.getElementById("new-chat-btn");
const clearBtn = document.getElementById("clear-btn");
const historyList = document.getElementById("history-list");
const historyToggle = document.getElementById("history-toggle");

const presetsByAction = {
  chat: [
    "What's new today?",
    "Help with code",
    "Brainstorm ideas",
  ],
  write: [
    "Email draft",
    "Social post",
    "Blog outline",
  ],
  analyze: [
    "Summarize text",
    "Find insights",
    "Extract key points",
  ],
};

const descriptions = {
  chat: "Ask anything and get instant responses",
  write: "Generate high-quality text and content",
  analyze: "Understand and extract insights",
};

let currentAction = "write";
let conversationHistory = [];
let chatHistories = [];
let isHistoryExpanded = true;

const setAction = (action) => {
  currentAction = action;
  
  optionBtns.forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.action === action);
  });

  panelTitle.textContent = action.charAt(0).toUpperCase() + action.slice(1) + " & Create";
  panelDesc.textContent = descriptions[action];

  updatePresets();
};

const updatePresets = () => {
  presetsContainer.innerHTML = "";
  const presets = presetsByAction[currentAction] || [];
  
  presets.forEach((preset) => {
    const btn = document.createElement("button");
    btn.className = "preset-btn";
    btn.textContent = preset;
    btn.addEventListener("click", () => {
      messageInput.value = preset;
      messageInput.focus();
    });
    presetsContainer.appendChild(btn);
  });
};

const addMessage = (role, content) => {
  const messageEl = document.createElement("div");
  messageEl.className = `message ${role}`;
  
  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  bubble.textContent = content;
  
  messageEl.appendChild(bubble);
  messagesArea.appendChild(messageEl);
  messagesArea.scrollTop = messagesArea.scrollHeight;
};

const setLoading = (isLoading) => {
  sendBtn.disabled = isLoading;
  sendBtn.textContent = isLoading ? "Sending..." : "Send";
  messageInput.disabled = isLoading;
};

const saveToHistory = () => {
  if (conversationHistory.length > 0) {
    const firstMessage = conversationHistory[0].content;
    const preview = firstMessage.length > 30 ? firstMessage.substring(0, 27) + "..." : firstMessage;
    const timestamp = new Date().toLocaleTimeString();
    
    chatHistories.unshift({
      id: Date.now(),
      preview,
      timestamp,
      messages: [...conversationHistory],
      action: currentAction,
    });
    
    if (chatHistories.length > 20) chatHistories.pop();
    updateHistoryList();
  }
};

const startNewChat = () => {
  if (conversationHistory.length > 0) {
    saveToHistory();
  }
  
  conversationHistory = [];
  messagesArea.innerHTML = '<div class="welcome-message"><h3>Welcome</h3><p>Start a new conversation or select a preset prompt below.</p></div>';
  messageInput.value = "";
  messageInput.focus();
};

const updateHistoryList = () => {
  if (chatHistories.length === 0) {
    historyList.innerHTML = '<div class="history-empty">No history yet</div>';
    return;
  }
  
  historyList.innerHTML = "";
  chatHistories.forEach((chat) => {
    const item = document.createElement("div");
    item.className = "history-item";
    
    const text = document.createElement("span");
    text.className = "history-item-text";
    text.textContent = `${chat.preview}`;
    text.title = chat.preview;
    
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "history-item-delete";
    deleteBtn.innerHTML = "✕";
    deleteBtn.onclick = (e) => {
      e.stopPropagation();
      chatHistories = chatHistories.filter((c) => c.id !== chat.id);
      updateHistoryList();
    };
    
    item.appendChild(text);
    item.appendChild(deleteBtn);
    
    item.addEventListener("click", () => {
      conversationHistory = [...chat.messages];
      currentAction = chat.action;
      setAction(chat.action);
      
      messagesArea.innerHTML = "";
      conversationHistory.forEach((msg) => {
        addMessage(msg.role, msg.content);
      });
    });
    
    historyList.appendChild(item);
  });
};

historyToggle.addEventListener("click", () => {
  isHistoryExpanded = !isHistoryExpanded;
  historyList.style.display = isHistoryExpanded ? "flex" : "none";
  historyToggle.classList.toggle("collapsed");
});

optionBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    setAction(btn.dataset.action);
  });
});

clearBtn.addEventListener("click", () => {
  startNewChat();
});

newChatBtn.addEventListener("click", () => {
  startNewChat();
});

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const message = messageInput.value.trim();
  if (!message) return;

  addMessage("user", message);
  conversationHistory.push({ role: "user", content: message });
  messageInput.value = "";
  
  setLoading(true);

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error("Request failed");
    }

    const data = await response.json();
    const reply = data.reply || "No response received.";
    
    addMessage("assistant", reply);
    conversationHistory.push({ role: "assistant", content: reply });
  } catch (err) {
    addMessage("assistant", `Error: ${err.message}`);
  } finally {
    setLoading(false);
    messageInput.focus();
  }
});

// Initialize
updatePresets();
addMessage("assistant", "Hi! How can I help you today?");
