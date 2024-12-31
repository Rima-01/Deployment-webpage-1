document.addEventListener("DOMContentLoaded", () => {
    const videoGrid = document.getElementById('video-grid'); // Posters grid
    const videoPlayer = document.getElementById('video');   // Video player

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
    const API_URL = "http://44.212.18.20:8001/videos/"; // Replace with backend API URL
    const videoGrid = document.getElementById('video-grid');

    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        if (data.success) {
            data.videos.forEach(video => {
                const img = document.createElement('img');
                img.src = video.poster_url; // Pre-signed poster URL
                img.alt = video.title;
                img.title = video.title; // Tooltip
                img.className = 'video-poster';
                img.onclick = () => navigateToVideoPage(video.video_id, video.title, video.description);
                videoGrid.appendChild(img);
            });
        } else {
            console.error('Failed to fetch posters:', data.error);
        }
    } catch (error) {
        console.error('Error fetching posters:', error);
    }
}

// Navigate to video page
function navigateToVideoPage(videoId, title, description) {
    const videoPageUrl = `/video.html?video_id=${videoId}&title=${encodeURIComponent(title)}&description=${encodeURIComponent(description)}`;
    window.location.href = videoPageUrl;
}

// Fetch video details and play video
async function fetchAndPlayVideo() {
    const video = document.getElementById('video');
    const videoTitle = document.getElementById('video-title');
    const descriptionElement = document.getElementById('description');

    const urlParams = new URLSearchParams(window.location.search);
    const videoId = urlParams.get('video_id');
    const title = urlParams.get('title');
    const description = urlParams.get('description');

    // Set the title and description
    videoTitle.textContent = title;
    descriptionElement.textContent = description;

    const API_URL = `http://44.212.18.20:8001/videos/video/${videoId}/`;

    try {
        const response = await fetch(API_URL, { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            video.src = data.video_url; // Pre-signed video URL
        } else {
            console.error('Failed to fetch video:', data.error);
        }
    } catch (error) {
        console.error('Error fetching video:', error);
    }
}

// Navigate back to posters page
function goBack() {
    window.location.href = "/posters.html";
}
