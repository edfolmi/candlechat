function openSidebar() {
    document.querySelector('.sidebar').style.display = 'flex';
    document.querySelector('.sidebar-icon').style.display = 'none';
    document.querySelector('.sidebar-close-icon').style.display = 'block';
}

function closeSidebar() {
    document.querySelector('.sidebar').style.display = 'none';
    document.querySelector('.sidebar-icon').style.display = 'block';
    document.querySelector('.sidebar-close-icon').style.display = 'none';
}

function preloader() {
    let preloader = document.querySelector('.preloader');
    let bodyRed = document.querySelector(".body.red");
    let bodyGreen = document.querySelector(".body.green");
    let connector = document.querySelector(".connector");
  
    setTimeout(function () {
      bodyRed.classList.remove("red");
      bodyRed.classList.add("animate");
      bodyGreen.classList.add("green");
      connector.style.animation = "connectorAnimation2 1s infinite alternate";
    }, 2000);

    setTimeout(function () {
        preloader.remove();
    }, 3000);
};
preloader();