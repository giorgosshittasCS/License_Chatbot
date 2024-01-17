function Refresh(){
    location.reload();
}
function handleAnswer(element) {
    var answer= element.textContent;
    if (answer =="Yes")
        element.classList.add("green");
    else if (answer =="No")
        element.classList.add("red");
    else if(answer =="Don't Mind")
        element.classList.add("orange");

    var elements = document.getElementsByClassName('option');

// Iterate through the elements and disable onClick
    for (var i = 0; i < elements.length; i++) {
    // Store a reference to the current element
        var currentElement = elements[i];

    // Disable the existing onClick function
    currentElement.removeAttribute('onclick');
}
submitAnswer(answer)

}
async function submitAnswer(answer) {
    const response = await fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answer }),
    });

    const data = await response.json();
    displayQuestion(data);
}
function displayQuestion(data){
var element=document.getElementById("conversation");
var htmlString=`<div class="chat-block">
<div class="bot-icon-block">
<img class="bot-image" src="static/images/bot.png" alt="">
</div>
<div class="question-block">${data.question}</div>
</div>
<div class="options-block">`;
var options= `
<button class="yes-block option" onclick="handleAnswer(this)">Yes</button>
<button class="no-block option" onclick="handleAnswer(this)">No</button>
`;

if (data.options.includes("Don't Mind")){
    options+= `<button class="neutral-block option" onclick="handleAnswer(this)">Don't Mind</button>`;
}

var recommendations=`</div><div class="recommendations-block">
<div class="recommendation-text">Recommended:</div>
<div class="licenses-block">${data.current_subset}</div>
</div>`;
htmlString+=options+recommendations;
element.insertAdjacentHTML('beforeend', htmlString);
}