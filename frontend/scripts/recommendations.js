document.addEventListener("DOMContentLoaded", () => {
//    const API_URL = "http://54.152.167.28:8003/get_recommendations/"; // Backend URL
//    const API_URL = 'http:/3.88.57.158:8003/get_recommendations/?_=${new Date().getTime()}';
    const API_URL = `http://34.239.234.119:8003/get_recommendations/?_=${new Date().getTime()}`;

    const recommendationContainer = document.getElementById("recommendation-container");

    // Fetch and display recommendations
    function fetchRecommendations() {
        fetch(API_URL)
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    recommendationContainer.innerHTML = ""; // Clear existing recommendations
                    const videos = data.videos;
                    videos.forEach((video) => {
                        const item = document.createElement("div");
                        item.className = "recommendation-item";

                        const poster = document.createElement("img");
                        poster.src = video.poster_url;
                        poster.alt = video.title;
                        poster.title = video.title;
                        poster.onclick = () => navigateToVideoPage(video.video_id, video.title, video.description);

                        const description = document.createElement("div");
                        description.className = "description";
                        const title = document.createElement("h3");
                        title.textContent = video.title;
                        const desc = document.createElement("p");
                        desc.textContent = video.description;

                        description.appendChild(title);
                        description.appendChild(desc);
                        item.appendChild(poster);
                        item.appendChild(description);
                        recommendationContainer.appendChild(item);
                    });
                } else {
                    console.error("Failed to fetch recommendations:", data.error);
                    recommendationContainer.innerHTML = `<p style="color: red; text-align: center;">Failed to load recommendations. Please try again later.</p>`;
                }
            })
            .catch((error) => {
                console.error("Error fetching recommendations:", error);
                recommendationContainer.innerHTML = `<p style="color: red; text-align: center;">An error occurred. Please try again later.</p>`;
            });
    }

    // Initial fetch
    fetchRecommendations();

    // Refresh recommendations every 30 seconds
    setInterval(fetchRecommendations, 10000);
});

function navigateToVideoPage(videoId, title, description) {
    const videoPageUrl = `/play_video.html?video_id=${videoId}&title=${encodeURIComponent(
        title
    )}&description=${encodeURIComponent(description)}`;
    window.location.href = videoPageUrl;
}
