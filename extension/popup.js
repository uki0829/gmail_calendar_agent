const API_URL = "http://127.0.0.1:8000";

const statusSpan = document.getElementById("status");
const statusDot = document.getElementById("status-indicator");
const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const messageDiv = document.getElementById("message");
const eventsCount = document.getElementById("events-count");
const priorityCount = document.getElementById("priority-count");
const feedContainer = document.getElementById("feed-container");

async function updateStatus() {
    try {
        const response = await fetch(`${API_URL}/status`);
        const data = await response.json();
        statusSpan.textContent = data.running ? "ACTIVE" : "INACTIVE";

        // Update Stats
        if (data.stats) {
            eventsCount.textContent = data.stats.created_today;
            priorityCount.textContent = data.stats.priority_count;
        }

        if (data.running) {
            document.body.classList.add("running");
            document.body.classList.remove("stopped");
            statusDot.className = "status-dot running";
            startBtn.disabled = true;
            stopBtn.disabled = false;
        } else {
            document.body.classList.add("stopped");
            document.body.classList.remove("running");
            statusDot.className = "status-dot stopped";
            startBtn.disabled = false;
            stopBtn.disabled = true;
        }
    } catch (error) {
        statusSpan.textContent = "DISCONNECTED";
        statusDot.className = "status-dot";
        document.body.classList.remove("running", "stopped");
        startBtn.disabled = true;
        stopBtn.disabled = true;
    }
}

async function updateFeed() {
    try {
        const response = await fetch(`${API_URL}/recent_emails`);
        const data = await response.json();
        renderFeed(data.emails);
    } catch (error) {
        console.error("Failed to fetch feed:", error);
    }
}

function renderFeed(emails) {
    feedContainer.innerHTML = "";
    if (!emails || emails.length === 0) {
        feedContainer.innerHTML = '<div style="text-align:center; font-size:10px; color:#444; padding:10px;">No recent important emails</div>';
        return;
    }

    emails.forEach(email => {
        const card = document.createElement("div");
        card.className = "email-card";

        // Clean up sender (remove <email> part if too long)
        const senderName = email.sender.split('<')[0].trim();

        card.innerHTML = `
      <div class="email-header">
        <div class="email-info">
          <span class="email-sender" title="${email.sender}">${senderName}</span>
          <span class="email-subject" title="${email.subject}">${email.subject}</span>
        </div>
        <span class="badge ${email.category}">${email.category}</span>
      </div>
      <div class="email-body">
        <p class="summary-text">${email.summary}</p>
      </div>
    `;

        // Accordion Logic
        card.addEventListener("click", () => {
            card.classList.toggle("expanded");
        });

        feedContainer.appendChild(card);
    });
}

startBtn.addEventListener("click", async () => {
    try {
        statusSpan.textContent = "INITIALIZING...";
        startBtn.disabled = true;
        const response = await fetch(`${API_URL}/start`, { method: "POST" });
        const data = await response.json();
        messageDiv.textContent = data.message;
        setTimeout(updateStatus, 500);
    } catch (error) {
        messageDiv.textContent = "Failed to start agent";
        updateStatus();
    }
});

stopBtn.addEventListener("click", async () => {
    try {
        statusSpan.textContent = "STOPPING...";
        stopBtn.disabled = true;
        const response = await fetch(`${API_URL}/stop`, { method: "POST" });
        const data = await response.json();
        messageDiv.textContent = data.message;
        setTimeout(updateStatus, 500);
    } catch (error) {
        messageDiv.textContent = "Failed to stop agent";
        updateStatus();
    }
});

// Initial check
updateStatus();
updateFeed();
// Poll status every 2 seconds
setInterval(() => {
    updateStatus();
    updateFeed();
}, 2000);
