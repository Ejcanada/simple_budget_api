const API_URL = "https://simplebudgetmatcherapi.vercel.app/"; 
const API_KEY = "my_secret_budget_key";

const FETCH_OPTIONS = {
    headers: { "x-api-key": API_KEY }
};

let currentMatches = []; // Stores the current results for the modal

// BUILD A FULL IMAGE URL 
function getImageUrl(image) {
    if (!image || image.trim() === "") return "";
    if (image.startsWith("http")) return image; 

    if (image.includes("images/")) {
        return image.startsWith("/") ? image.substring(1) : image;
    } else {
        const cleanIcon = image.startsWith("/") ? image.substring(1) : image;
        return `images/${cleanIcon}`;
    }
}

// GET MATCHES BASED ON BUDGET
async function findMatches() {
    // Read from inputs, fallback to default values if empty
    const budgetInput = document.getElementById("budgetInput");
    const durationInput = document.getElementById("durationInput");
    
    const budget = budgetInput ? budgetInput.value : 2500;
    const duration = durationInput ? durationInput.value : 7;

    const landmarkList = document.getElementById("landmarkList");
    if (!landmarkList) return;

    landmarkList.innerHTML = `
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Calculating budget matches...</p>
        </div>
    `;

    try {
        const response = await fetch(`${API_URL}/match?budget=${budget}&duration=${duration}`, FETCH_OPTIONS);
        const data = await response.json();
        
        currentMatches = data.matches || [];
        displayMatches(currentMatches, data.duration);
    }
    catch (error) {
        console.error(error);
        landmarkList.innerHTML = "Unable to connect to the API.";
    }
}

// DISPLAY MATCHES 
function displayMatches(matches, duration) {
    const landmarkList = document.getElementById("landmarkList");
    landmarkList.innerHTML = "";

    if (matches.length === 0) {
        landmarkList.innerHTML = `<p class="no-results">No destinations found for this budget. Try increasing your amount.</p>`;
        return;
    }

    matches.forEach((match, index) => {
        const card = document.createElement("div");
        card.className = "landmark-card";
        
        card.style.animationDelay = `${index * 0.05}s`;

        const hasIcon = match.image && match.image.trim() !== "";
        const iconHTML = hasIcon
            ? `<img src="${getImageUrl(match.image)}" alt="${match.name}" class="landmark-icon" onerror="this.outerHTML='<div class=\\'landmark-icon no-image\\'></div>'">`
            : `<div class="landmark-icon no-image"></div>`;

        card.innerHTML = `
            ${iconHTML}
            <div class="card-info">
                <h3>${match.name}</h3>
                <div class="landmark-location">${match.country}</div>
                <span class="type-badge">${match.tag}</span>
                <p><strong>Est. Per Day:</strong> $${match.daily_cost}</p>
                <p><strong>${duration}-Day Total:</strong> $${match.trip_total}</p>
                <button onclick="viewMatch(${index})"> View Details </button>
            </div>
        `;
        landmarkList.appendChild(card);
    });
}

// GET ONE MATCH FOR MODAL
function viewMatch(index) {
    try {
        const match = currentMatches[index];
        const modalBody = document.getElementById("modalBody");

        const hasIcon = match.image && match.image.trim() !== "";
        const heroHTML = hasIcon
            ? `
                <div class="modal-hero" style="background-image: url('${getImageUrl(match.image)}');">
                    <div class="modal-hero-overlay"></div>
                    <div class="modal-hero-text">
                        <h2>${match.name}</h2>
                        <p>${match.country}</p>
                    </div>
                </div>
            `
            : `
                <div class="modal-hero no-image"></div>
                <h2 style="margin: 15px 0 0 0; color: #1f1f1f;">${match.name}</h2>
                <p style="color: #555; margin-top: 5px;">${match.country}</p>
            `;

        modalBody.innerHTML = `
            ${heroHTML}
            <div class="modal-grid">
                <div class="modal-item"><strong>Travel Vibe:</strong> ${match.tag}</div>
                <div class="modal-item"><strong>Daily Cost:</strong> $${match.daily_cost}</div>
                <div class="modal-item"><strong>Total Trip Cost:</strong> $${match.trip_total}</div>
                <div class="modal-item"><strong>Money to Spare:</strong> $${match.spare}</div>
                
                <div class="modal-desc">
                    <strong>Why ${match.name}?</strong><br>
                    This destination comfortably fits your budget profile. After covering basic estimated costs for your trip, you will have $${match.spare} left over for souvenirs, extra activities, or emergencies!
                </div>
            </div>
        `;

        // Show the modal
        document.getElementById("landmarkModal").classList.add("show");
    }
    catch (error) {
        console.error(error);
        alert("Unable to retrieve details.");
    }
}

// CLOSE MODAL FUNCTION
function closeModal() {
    document.getElementById("landmarkModal").classList.remove("show");
}

// CLOSE MODAL WHEN CLICKING OUTSIDE THE BOX
window.onclick = function(event) {
    const modal = document.getElementById("landmarkModal");
    if (event.target === modal) {
        closeModal();
    }
};

// INITIAL LOAD
findMatches();
