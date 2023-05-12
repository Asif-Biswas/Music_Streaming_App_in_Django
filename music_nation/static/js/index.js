$(document).ready(function () {
  $("#nav-icon").click(function () {
    $(this).toggleClass("open");
    $(".overlay").toggleClass("open");
    $(".overlay a").toggleClass("open");
    $(".overlay p").toggleClass("open");
  });
});
const musicbar = document.querySelector(".music");
const musicname = document.querySelector(".musicname");
const artis = document.querySelector(".artist");
const img = document.querySelector(".cover");
const imgs = document.querySelector(".shadow");
const rote = document.querySelector(".cover");
const playBtn = document.querySelector(".play-btn");
const pauseBtn = document.querySelector(".pause-btn");
const preBtn = document.querySelector(".prev-btn");
const nextBtn = document.querySelector(".next-btn");
const music = document.getElementById("music");
const musicList = document.getElementsByTagName("li");
const progressBar = document.getElementById("progress-bar");
let currentTrack = 0;
let currentList;


function init() {
  if (currentTrack === 0) {
    music.src = tracks[0].url;
    music.load();
  }

  for (let i = 0; i < tracks.length; i++) {
    $("#musiclist")
      .append(`<li id="${i}">
                <div class="box p-2" >
                  <div class="content">
                    <h3>
                    <i class="fas fa-music"></i>
                    ${tracks[i].name}</h3>
                    <audio id="music" src="${tracks[i].url}"></audio>
                  <div>
                </div>
              </li>`);
  }

  for (let musicIndex = 0; musicIndex < musicList.length; musicIndex++) {
    musicList[musicIndex].addEventListener("click", switchMusic, false);
  }
}

function switchMusic(e) {
  if (currentList !== undefined) {
    removePlayedBackground();
    music.pause();
  }
  currentTrack = this.id;
  music.src = tracks[currentTrack].url;
  music.load();
  play();
}

function addChoosedBackground() {
  currentList = document.getElementById(currentTrack);
  currentList.classList.add("song-play-now");
}

function removePlayedBackground() {
  currentList.classList.remove("song-play-now");
}

function play() {
  //img.src = tracks[currentTrack].image;
  //imgs.src = tracks[currentTrack].image;
  artis.innerHTML = tracks[currentTrack].album;
  musicname.innerHTML = tracks[currentTrack].name;
  //rote.classList.add("rote");
  playBtn.classList.add("hidden");
  pauseBtn.classList.remove("hidden");
  musicbar.classList.add("openn");
  music.play();
  musicIsPlaying = true;
  addChoosedBackground();
  //document.getElementById("end-time").innerHTML = tracks[currentTrack].duration;
}

function pause() {
  //rote.classList.remove("rote");
  pauseBtn.classList.add("hidden");
  playBtn.classList.remove("hidden");

  musicIsPlaying = false;
  music.pause();
}

function prePlay() {
  removePlayedBackground();
  music.pause();

  if (currentTrack > 0) {
    currentTrack--;
  } else {
    currentTrack = tracks.length - 1;
  }

  music.src = tracks[currentTrack].url;
  music.load();
  play();
}

function nextPlay() {
  removePlayedBackground();
  music.pause();

  if (currentTrack < tracks.length - 1) {
    currentTrack++;
  } else {
    currentTrack = 0;
  }

  music.src = tracks[currentTrack].url;
  music.load();
  play();
}

function calculateTotalValue(length) {
  let minutes = Math.floor(length / 60),
    seconds_int = length - minutes * 60,
    seconds_str = seconds_int.toString(),
    seconds = seconds_str.substr(0, 2),
    time = minutes + ":" + seconds;

  return time;
}

function formatTime() {
  let timeline = document.getElementById("start-time");
  let s = parseInt(music.currentTime % 60);
  let m = parseInt((music.currentTime / 60) % 60);
  if (s < 10) {
    timeline.innerHTML = m + ":0" + s;
  } else {
    timeline.innerHTML = m + ":" + s;
  }
}

function updateProgress() {
  let current = music.currentTime;
  let percent = (current / music.duration) * 100;
  progressBar.setAttribute("value", percent);
}

playBtn.addEventListener("click", play, false);
pauseBtn.addEventListener("click", pause, false);
preBtn.addEventListener("click", prePlay, false);
nextBtn.addEventListener("click", nextPlay, false);
music.addEventListener("ended", nextPlay, false);

// 歌曲已播放時間
music.addEventListener("timeupdate", formatTime, false);
music.addEventListener("timeupdate", updateProgress, false);

// progressBar.addEventListener("click", function(e) {
//   try {
//     let percent = e.offsetX / this.offsetWidth;
//     console.log(percent, percent * music.duration);
//     music.currentTime = parseInt(percent * music.duration)
//     console.log(music.duration, music.currentTime, percent * music.duration);
//     //progressBar.setAttribute("value", percent / 100);
//   } catch (error) {
//     console.log(error);
//   }

// });

init();


const volume = document.getElementById("volume");
volume.addEventListener("change", function(e) {
  music.volume = e.currentTarget.value;
})