const apiUrl = "http://localhost:8000/api/watchlist/";

document.addEventListener("DOMContentLoaded", function () {
    fetch(apiUrl, {
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
        })
        .catch(error => console.error("Error fetching watchlist:", error));
});

function removeFromWatchlist(videoId) {
    fetch(apiUrl + videoId + "/", {
        method: "DELETE",
        credentials: "include", // Include session cookies
    })
        .then(response => {
            if (response.ok) {
                location.reload(); // Reload page to reflect changes
            }
        })
        .catch(error => console.error("Error removing video:", error));
}
