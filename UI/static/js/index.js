document.addEventListener("DOMContentLoaded", function() {
    second=document.getElementById("second");
    third=document.getElementById("third");
    button=document.getElementById("moveToChatbot");
    // animate__lightSpeedInLeft
    setTimeout(function() {
        // Remove the 'hidden' class to show the container
        second.style.visibility="visible";
        second.style.animationDuration= "1s";
        second.classList.add("animate__lightSpeedInLeft");
    }, 800);
    setTimeout(function() {
        // Remove the 'hidden' class to show the container
        third.style.visibility="visible";
        third.style.animationDuration= "1s";
        third.classList.add("animate__lightSpeedInLeft");
    }, 1200);
    
    setTimeout(function() {
        // Remove the 'hidden' class to show the container
        button.style.visibility="visible";
        button.style.animationDuration= "1s";
        button.classList.add("animate__backInRight");
    }, 1700);
});