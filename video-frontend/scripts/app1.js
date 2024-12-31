const videoGrid = document.getElementById('video-grid');
const videoPlayer = document.getElementById('video-player');
const video = document.getElementById('video');
const description = document.getElementById('description'); // Element to display video description

// API base URL for the video streaming backend
const VIDEO_API_BASE_URL = "http://44.212.18.20:8001"; // Update the port if needed

// Fetch video data from the backend API
async function fetchVideos() {
    try {
        const response = await fetch(`${VIDEO_API_BASE_URL}/videos/`);
        if (!response.ok) {
            throw new Error(`Error fetching videos: ${response.statusText}`);
        }
        const data = await response.json();
        if (data.success) {
            displayVideos(data.videos);
        } else {
            console.error('Failed to fetch videos:', data.error);
        }
    } catch (error) {
        console.error('Failed to fetch videos:', error);
    }
}

// Display video posters dynamically
function displayVideos(videos) {
    videos.forEach(video => {
        const img = document.createElement('img');
        img.src = video.poster_url; // Use the pre-signed poster URL
        img.alt = video.title;
        img.title = video.title; // Adds a tooltip with the video title
        img.className = 'video-poster';
        img.onclick = () => playVideo(video.video_id, video.description); // Pass video_id and description
        videoGrid.appendChild(img);
    });
}

// Play the selected video in the video player
async function playVideo(videoId, videoDescription) {
    try {
        const response = await fetch(`${VIDEO_API_BASE_URL}/videos/video/${videoId}/`, { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            video.src = data.video_url; // Use the pre-signed video URL
            description.textContent = videoDescription || "No description available."; // Show description
            videoPlayer.classList.remove('hidden');
        } else {
            console.error('Error fetching video:', data.error);
        }
    } catch (error) {
        console.error('Failed to play video:', error);
    }
}

// Close the video player
function closePlayer() {
    videoPlayer.classList.add('hidden');
    video.pause();
}

// Fetch and display videos on page load
fetchVideos();
