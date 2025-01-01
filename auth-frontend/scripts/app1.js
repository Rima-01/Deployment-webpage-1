document.addEventListener("DOMContentLoaded", () => {
    const videoGrid = document.getElementById("video-grid");
    const videoPlayer = document.getElementById("video");

    if (videoGrid) {
        // Posters page logic
        fetchPosters();
    } else if (videoPlayer) {
        // Video player page logic
        fetchAndPlayVideo();
    }
});

// Fetch and display posters
async function fetchPosters() {
    const API_URL = "http://52.207.108.185:8001/videos/get_videos/"; // Replace with your backend API URL
    const videoGrid = document.getElementById("video-grid");

    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        if (data.success) {
            // Loop through the video list and create poster elements
            data.videos.forEach((video) => {
                const img = document.createElement("img");
                img.src = video.poster_url; // Pre-signed poster URL
                img.alt = video.title;
                img.title = video.title; // Tooltip for the poster
                img.className = "video-poster";
                img.onclick = () =>
                    navigateToVideoPage(video.video_id, video.title, video.description);
                videoGrid.appendChild(img);
            });
        } else {
            console.error("Failed to fetch posters:", data.error);
            displayError(videoGrid, "Failed to load videos. Please try again.");
        }
    } catch (error) {
        console.error("Error fetching posters:", error);
        displayError(videoGrid, "An error occurred while loading videos.");
    }
}

// Navigate to video page
function navigateToVideoPage(videoId, title, description) {
    const videoPageUrl = `/play_video.html?video_id=${videoId}&title=${encodeURIComponent(
        title
    )}&description=${encodeURIComponent(description)}`;
    window.location.href = videoPageUrl;
}

// Fetch video details and play video
async function fetchAndPlayVideo() {
    const video = document.getElementById("video");
    const videoTitle = document.getElementById("video-title");
    const descriptionElement = document.getElementById("description");

    const urlParams = new URLSearchParams(window.location.search);
    const videoId = urlParams.get("video_id");
    const title = urlParams.get("title");
    const description = urlParams.get("description");

    // Set the title and description
    videoTitle.textContent = title || "Untitled Video";
    descriptionElement.textContent = description || "No description available.";

    const API_URL = `http://52.207.108.185:8001/videos/play_video/${videoId}/`;

    try {
        const response = await fetch(API_URL, { method: "POST" });
        const data = await response.json();

        if (data.success) {
            video.src = data.video_url; // Pre-signed video URL
        } else {
            console.error("Failed to fetch video:", data.error);
            videoTitle.textContent = "Error Loading Video";
            descriptionElement.textContent = "Unable to fetch video details.";
        }
    } catch (error) {
        console.error("Error fetching video:", error);
        videoTitle.textContent = "Error Loading Video";
        descriptionElement.textContent = "An error occurred while loading the video.";
    }
}

// Navigate back to posters page
function goBack() {
    window.location.href = "/posters.html";
}

// Display an error message in the posters grid
function displayError(container, message) {
    const errorElement = document.createElement("p");
    errorElement.textContent = message;
    errorElement.style.color = "red";
    errorElement.style.textAlign = "center";
    container.appendChild(errorElement);
}
