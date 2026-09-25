async function findMatches() {
    const budget = document.getElementById('budgetInput').value;
    const duration = document.getElementById('durationInput').value;
    const btn = document.querySelector('.primary-btn');

    if (!budget || !duration) {
        alert("Please enter both your budget and duration.");
        return;
    }

    btn.textContent = "Searching...";

    try {
        // Add the headers for the API key authentication
        const FETCH_OPTIONS = {
            headers: { "x-api-key": "my_secret_budget_key" }
        };

        const response = await fetch(`/api/match?budget=${budget}&duration=${duration}`, FETCH_OPTIONS);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        renderCards(data);
        showResultsView();
        
    } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to find matches. Make sure the API is running and the API key is correct.");
    } finally {
        btn.textContent = "Find Matches";
    }
}
