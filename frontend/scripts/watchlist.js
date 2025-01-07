const apiUrl = "http://54.152.167.28:8002/api/watchlist/";

// Get user_id from localStorage
const userId = localStorage.getItem('user_id');

if (!userId) {
    alert("You are not logged in. Redirecting to login page...");
    window.location.href = "login.html"; // Redirect to login if user_id is not found
}

// Logout functionality
document.addEventListener("DOMContentLoaded", () => {
    const logoutButton = document.getElementById("logout-button");
    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            localStorage.removeItem('user_id');
            window.location.href = "login.html";
        });
    }
});

// Load the user's watchlist
document.addEventListener("DOMContentLoaded", function () {
    fetch(`${apiUrl}?user_id=${encodeURIComponent(userId)}`, {  // Pass user_id as a query parameter
        credentials: "include", // Include session cookies
    })
        .then(response => {
            if (response.status === 401) {
                alert("You are not logged in.");
                window.location.href = "login.html"; // Redirect to login page if unauthenticated
                return;
            }
            return response.json();
        })
        .then(data => {
            const container = document.getElementById("watchlist-container");
            container.innerHTML = ""; // Clear any loading message

            if (data.message === "Your watchlist is empty.") {
                container.innerHTML = `<p>${data.message}</p>`; // Fixed string template syntax
            } else {
                data.forEach(video => {
                    const card = document.createElement("div");
                    card.className = "video-card";
                    card.innerHTML = `
                        <img src="${video.poster_url}" alt="${video.title}">
                        <h4>${video.title}</h4>
                        <button onclick="removeFromWatchlist('${video.video_id}')">Remove</button>
                    `;
                    container.appendChild(card);
                });
            }
        })
        .catch(error => console.error("Error fetching watchlist:", error));
});

// Remove a video from the watchlist
function removeFromWatchlist(videoId) {
    fetch(`${apiUrl}${encodeURIComponent(videoId)}/?user_id=${encodeURIComponent(userId)}`, {  // Pass user_id as a query parameter
        method: "DELETE",
        credentials: "include", // Include session cookies
    })
        .then(response => {
            if (response.ok) {
                alert("Video removed from your watchlist.");
                location.reload(); // Reload page to reflect changes
            } else {
                alert("Failed to remove video from watchlist.");
            }
        })
        .catch(error => console.error("Error removing video:", error));
}
