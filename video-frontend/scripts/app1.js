const videoGrid = document.getElementById('video-grid');
const videoPlayer = document.getElementById('video-player');
const video = document.getElementById('video');

// Fetch video data from the backend API
async function fetchVideos() {
    try {
        const response = await fetch('http://localhost:8000/videos/');
        if (!response.ok) {
            throw new Error(`Error fetching videos: ${response.statusText}`);
        }
        const videos = await response.json();
        displayVideos(videos.videos); // Assume API response includes a "videos" key
    } catch (error) {
        console.error('Failed to fetch videos:', error);
    }
}

// Display video posters dynamically
function displayVideos(videos) {
    videos.forEach(video => {
        const img = document.createElement('img');
        img.src = video.poster_url;
        img.alt = video.title;
        img.title = video.title; // Adds a tooltip with the video title
        img.className = 'video-poster';
        img.onclick = () => playVideo(video.video_url);
        videoGrid.appendChild(img);
    });
}

// Play the selected video in the video player
function playVideo(url) {
    video.src = url;
    videoPlayer.classList.remove('hidden');
}

// Close the video player
function closePlayer() {
    videoPlayer.classList.add('hidden');
    video.pause();
}

// Fetch and display videos on page load
fetchVideos();
