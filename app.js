const API_URL = "https://simplebudgetmatcherapi.vercel.app/"; 
const API_KEY = "my_secret_landmark_key"; // Using the auth key from your original API

const FETCH_OPTIONS = {
    headers: { "x-api-key": API_KEY }
};

let currentMatches = [];

function resetView() {
    document.getElementById('resultsView').style.display = 'none';
    document.getElementById('searchView').style.display = 'block';
}

function getImageUrl(icon) {
    if (!icon || icon.trim() === "") return "";
    if (icon.startsWith("http")) return icon; 
    if (icon.includes("images/")) {
        return icon.startsWith("/") ? icon.substring(1) : icon;
    } else {
        const cleanIcon = icon.startsWith("/") ? icon.substring(1) : icon;
        return `images/${cleanIcon}`;
    }
}

// Parses strings like "$45 USD" or "Free" into numerical costs for the math
function extractCost(feeString) {
    if (!feeString || feeString.toLowerCase() === "free") return 0;
    const match = feeString.match(/\d+(\.\d+)?/);
    return match ? parseFloat(match[0]) : 0;
}

async function findMatches() {
    const budgetInput = document.getElementById("budgetInput").value;
    const durationInput = document.getElementById("durationInput").value;
    
    if (!budgetInput || !durationInput) {
        alert("Please enter both your budget and duration.");
        return;
    }

    const budget = parseFloat(budgetInput);
    const duration = parseInt(durationInput);
    const btn = document.querySelector('.primary-btn');
    btn.textContent = "Calculating...";

    try {
        // Fetching from the PROFESSOR'S untouched API
        const response = await fetch(`${API_URL}/landmarks`, FETCH_OPTIONS);
        if (!response.ok) throw new Error("API Connection Failed");
        const data = await response.json();
        
        const matches = [];
        
        // Let the Javascript do the math instead of the backend
        data.landmarks.forEach(landmark => {
            const dailyCost = extractCost(landmark.entry_fee);
            const tripTotal = dailyCost * duration;
            const spare = budget - tripTotal;
            
            if (spare >= 0) {
                matches.push({
                    data: landmark,
                    dailyCost: dailyCost,
                    tripTotal: tripTotal,
                    spare: spare
                });
            }
        });

        currentMatches = matches;
        
        document.getElementById('matchCount').textContent = matches.length;
        renderCards(matches, duration);
        
        document.getElementById('searchView').style.display = 'none';
        document.getElementById('resultsView').style.display = 'block';
        
    } catch (error) {
        console.error(error);
        alert("Unable to connect to the API. Make sure index.py is running in the api folder.");
    } finally {
        btn.textContent = "Find Matches";
    }
}

function renderCards(matches, duration) {
    const grid = document.getElementById('cardsGrid');
    grid.innerHTML = "";

    if (matches.length === 0) {
        grid.innerHTML = `<p style="grid-column: 1/-1; text-align:center; color: #808080;">No destinations found for this budget. Try adjusting your inputs.</p>`;
        return;
    }

    matches.forEach((match, index) => {
        const landmark = match.data;
        const card = document.createElement("div");
        card.className = "match-card";

        const hasIcon = landmark.icon && landmark.icon.trim() !== "";
        const iconHTML = hasIcon
            ? `<img src="${getImageUrl(landmark.icon)}" alt="${landmark.title}">`
            : `<div class="no-image"></div>`;

        card.innerHTML = `
            <div class="card-image-container">
                <span class="tag">${landmark.site_type}</span>
                ${iconHTML}
            </div>
            <div class="card-body">
                <div class="card-header">
                    <div class="card-title">
                        <h3>${landmark.title}</h3>
                        <p>${landmark.country}</p>
                    </div>
                    <div class="action-icon" onclick="viewMatch(${index})">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                        </svg>
                    </div>
                </div>
                
                <div class="card-stats">
                    <div class="stat-row">
                        <span class="label">EST. ENTRY / DAY</span>
                        <span class="value green">${match.dailyCost === 0 ? 'Free' : '$' + match.dailyCost}</span>
                    </div>
                    <div class="stat-row">
                        <span class="label">${duration}-DAY TOTAL</span>
                        <span class="value">$${match.tripTotal}</span>
                    </div>
                </div>
                
                <div class="card-footer">
                    $${match.spare} to spare
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function viewMatch(index) {
    const match = currentMatches[index];
    const landmark = match.data;
    const modalBody = document.getElementById("modalBody");

    const hasIcon = landmark.icon && landmark.icon.trim() !== "";
    const heroHTML = hasIcon
        ? `
            <div class="modal-hero" style="background-image: url('${getImageUrl(landmark.icon)}');">
                <div class="modal-hero-overlay"></div>
                <div class="modal-hero-text">
                    <h2>${landmark.title}</h2>
                    <p>${landmark.country} | ${landmark.region}</p>
                </div>
            </div>
        `
        : `
            <div class="modal-hero no-image"></div>
            <h2 style="margin: 15px 0 0 0; color: #1f1f1f;">${landmark.title}</h2>
        `;

    modalBody.innerHTML = `
        ${heroHTML}
        <div class="modal-grid">
            <div class="modal-item"><strong>Established:</strong> ${landmark.established_year}</div>
            <div class="modal-item"><strong>Type:</strong> ${landmark.site_type}</div>
            <div class="modal-item"><strong>Rating:</strong> ${landmark.visitor_rating}</div>
            <div class="modal-item"><strong>Entry Fee:</strong> ${landmark.entry_fee}</div>
            <div class="modal-item"><strong>Architects:</strong> ${landmark.notable_architects}</div>
            <div class="modal-item"><strong>Governing Body:</strong> ${landmark.governing_body}</div>
            
            <div class="modal-desc">
                <strong>Description:</strong><br>
                ${landmark.description}
            </div>
        </div>
    `;

    document.getElementById("landmarkModal").classList.add("show");
}

function closeModal() {
    document.getElementById("landmarkModal").classList.remove("show");
}

window.onclick = function(event) {
    const modal = document.getElementById("landmarkModal");
    if (event.target === modal) closeModal();
};
