const video = document.querySelector('video.bg-cover');
const autoPlayToggle = document.querySelector('#hero-video-toggle');

function pauseVideo() {
    if (!video || !autoPlayToggle) return;
    video.pause();
    updateIcons();
    localStorage.setItem('hero-pause-video','true');

}

function playVideo() {
    if (!video || !autoPlayToggle) return;
    video.play();
    updateIcons();
    localStorage.removeItem('hero-pause-video');
}

const toggleVideoState = () => {
    if (!video || !autoPlayToggle) return;
    if (video.paused) {
        playVideo()
    } else {
        pauseVideo();
    }
   

}

const updateIcons = () => {
    const icons = autoPlayToggle.querySelectorAll('g');
    for(let i = 0; i < icons.length; i++) {
        icons[i].classList.toggle('is-active');
    }
}

function init() {
    if (!video || !autoPlayToggle) return;
    autoPlayToggle.addEventListener('click', toggleVideoState);
    const userPref = localStorage.getItem('hero-pause-video');
    console.log(userPref);
    if (userPref) {
        pauseVideo();
    }
}
init();
