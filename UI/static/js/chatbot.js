var question_number =2;
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
    if (data.finished==1)
        displayTable();
    else
        displayQuestion(data);
}
async function displayTable() {
    const response2 = await fetch('/table', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    const data = await response2.json();

    var license_instance = data.licenses[0];
    var allkeys=[...Object.keys(license_instance[0]),...Object.keys(license_instance[1]),...Object.keys(license_instance[2])];
    var element= document.getElementById("conversation");
    var htmlCode=`<div id="table-container" class="table-responsive"><table class="table table-dark table-striped rounded-3 overflow-hidden">
    <thead><tr><th scope="col" class="text-nowrap text-center p-3">Recommended Licenses</th>`; 
    for (let key of allkeys) {
        htmlCode += `<th scope="col" class="text-nowrap text-center p-3">${key}</th>`;
    }
    htmlCode += `</tr></thead><tbody>`;
    var counter=0;
    console.log(data.licenses_titles);
    for (let license of data.licenses) {
        let permissions = Object.values(license[0]);
        let conditions = Object.values(license[1]);
        let limitations = Object.values(license[2]);
        htmlCode+=`<tr>`;
        htmlCode+=`<td class="text-nowrap " >${data.licenses_titles[counter]}</td>`
        for (let value of permissions) {
            if(value==1)
                htmlCode+=`<td class="text-center"><img src="static/images/check-mark.svg" alt=""></td>`
            else
                htmlCode+=`<td class="text-center"><img src="static/images/cross-mark.svg" alt=""></td>`
            
        }
        for (let value of conditions) {
            if(value==1)
                htmlCode+=`<td class="text-center"><img src="static/images/check-mark.svg" alt=""></td>`
            else
                htmlCode+=`<td class="text-center"><img src="static/images/cross-mark.svg" alt=""></td>`
            
        }
        for (let value of limitations) {
            if(value==0)
                htmlCode+=`<td class="text-center"><img src="static/images/check-mark.svg" alt=""></td>`
            else
                htmlCode+=`<td class="text-center"><img src="static/images/cross-mark.svg" alt=""></td>`
            
        }
        counter++;
        htmlCode+=`</tr>`;

        
}
 htmlCode+=`</tbody>
 </table>
 </div>`;
 element.insertAdjacentHTML('beforeend', htmlCode);
 table_element=document.getElementById('table-container');
 table_element.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
}

function displayQuestion(data){
var element=document.getElementById("conversation");
var htmlString=`<div class="chat-block">
<div class="bot-icon-block">
<img class="bot-image" src="static/images/bot.png" alt="">
</div>
<div id="question-${question_number}" class="question-block">${data.question}</div>
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
htmlString=recommendations+htmlString+options;
element.insertAdjacentHTML('beforeend', htmlString);

question_element=document.getElementById("question-"+question_number);
question_element.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
question_number++;
}
