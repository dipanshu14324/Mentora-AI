// =====================================
// Backend URL
// =====================================

const API_URL = "http://127.0.0.1:8000";


// =====================================
// User
// =====================================

const user_id = "student1";

let session_id = null;

let controller = null;

let isListening = false;

let mediaRecorder = null;

let audioChunks = [];

let lastAnswer = "";


// =====================================
// DOM
// =====================================
const chatBox = document.getElementById("chat-scroll");
const input = document.getElementById("question");

const levelSelect =
document.getElementById("level");


const styleSelect =
document.getElementById("style");

const messagesBox =
document.getElementById("messages");

const scrollBox =
document.getElementById("chat-scroll");

console.log("Scroll Box:", scrollBox);

const questionInput =
document.getElementById("question");


const sendButton =
document.getElementById("send");


const stopButton =
document.getElementById("stop");


const newChatButton =
document.getElementById("newChat");


const historyBox =
document.getElementById("history");


const pdfFile =
document.getElementById("pdfFile");


const uploadButton =
document.getElementById("uploadBtn");


const uploadStatus =
document.getElementById("uploadStatus");

const quizBtn =
document.getElementById("quizBtn");


const flashBtn =
document.getElementById("flashBtn");




// =====================================
// New Chat
// =====================================

async function createNewChat(){


    const response = await fetch(
        `${API_URL}/new-chat?user_id=${user_id}`,
        {
            method:"POST"
        }
    );


    const data = await response.json();


    console.log("NEW CHAT RESPONSE:", data);


    session_id = data.session_id;


    messagesBox.innerHTML = "";


    const flashBox = document.getElementById("flashcards");

    if(flashBox){
        flashBox.innerHTML="";
    }


    const quizBox = document.getElementById("quizBox");

    if(quizBox){
        quizBox.innerHTML="";
    }


}






// =====================================
// Send Message
// =====================================


async function sendMessage(){

    stopSpeaking();

    const question =
    questionInput.value.trim();


    if(!question)
        return;



    if(!session_id){

        await createNewChat();

    }



    displayMessage(
        question,
        "user"
    );



    questionInput.value="";



    sendButton.disabled=true;

    setState("thinking");

    stopButton.disabled=false;



    controller =
    new AbortController();



    let answer="";



    const aiBox =
    displayMessage(
        "",
        "ai"
    );



    try{


        const response =
        await fetch(

        `${API_URL}/chat/stream`,

        {

        method:"POST",

        headers:{
            "Content-Type":
            "application/json"
        },


        body:JSON.stringify({

            user_id:user_id,

            session_id:session_id,

            question:question,


            level:
            levelSelect ?
            levelSelect.value:
            "Beginner",


            style:
            styleSelect ?
            styleSelect.value:
            "Concept Learning"

        }),


        signal:
        controller.signal

        }

        );



        const reader =
        response.body.getReader();


        const decoder =
        new TextDecoder();



        while(true){


            const {
                done,
                value
            } =
            await reader.read();

            if(done){

                setState("idle");

                break;
            }



            if(done)
                break;



            let chunkText = decoder.decode(
                value,
                {
                    stream:true
                }
            );


            answer += chunkText;



            aiBox.innerHTML =
            marked.parse(
                answer,
                {
                    breaks:true
                }
            );

            aiBox.classList.add("typing");


            if(
            scrollBox.scrollHeight -
            scrollBox.scrollTop -
            scrollBox.clientHeight < 100
            ){
            
            scrollBox.scrollTo({
            
                top:scrollBox.scrollHeight,
            
                behavior:"smooth"
            
            });

            }



            MathJax.typeset();

            document
            .querySelectorAll("pre code")
            .forEach((block)=>{
            
                hljs.highlightElement(block);
            
            });


        }

        answer += decoder.decode();

        answer = answer.replace(
            "Unable to generate answer.",
            ""
        );
        

    // ================================
    // Extract Flashcards
    // ================================


    if(answer.includes("FLASHCARDS_START")){


        let parts = answer.split(
            "FLASHCARDS_START"
        );


        let explanation = parts[0];


        let flashPart = parts[1]
            .split("FLASHCARDS_END")[0];


        try{


            let cards =
            JSON.parse(
                flashPart.trim()
            );


            console.log(
                "STREAM FLASHCARDS:",
                cards
            );
            

            showflashcards(cards);



        }
        catch(e){

            console.log(
                "Flashcard Parse Error",
                e
            );

        }



        answer = explanation;


    }
        lastAnswer = answer;

        // Save answer
        loadHistory();

        
        // Auto Generate Flashcards

        if(answer.length > 100){
        
            generateflashcards(answer);
        
        }

         // Speak
        await speakAnswer(answer);

        
        // Scroll back to explanation
        



    }


    catch(error){


        if(error.name==="AbortError"){


            aiBox.innerHTML =
            "⛔ Generation stopped";


        }

        else{


            console.log(error);


            aiBox.innerHTML =
            "❌ Error";

        }


    }



    finally{


        controller=null;

        sendButton.disabled=false;

        stopButton.disabled=false;

        setState("idle"); 


    }


}








// =====================================
// Stop
// =====================================


function stopGeneration(){


    // Stop AI text streaming
    if(controller){

        controller.abort();

        controller=null;

    }


    // Stop voice explanation
    stopSpeaking();


    sendButton.disabled=false;

    stopButton.disabled=true;


}




// =====================================
// Display Message
// =====================================


function displayMessage(text,role){


    const div =
    document.createElement("div");


    div.className =
    "message "+role;



    if(role==="ai"){

        div.innerHTML =
        marked.parse(
            text,
            {
                breaks:true
            }
        );

    }

    else{

        div.innerText=text;

    }


    messagesBox.appendChild(div);


    scrollBox.scrollTo({

    top:scrollBox.scrollHeight,

    behavior:"smooth"

    });


    if(window.MathJax){
    MathJax.typesetPromise();
}


    return div;

}








// =====================================
// Load History
// =====================================

async function loadHistory(){

    try{

        const response = await fetch(
            `${API_URL}/history/${user_id}`
        );


        const data = await response.json();


        console.log("HISTORY:", data);



        historyBox.innerHTML="";


        if(!data.chats || data.chats.length===0){

            historyBox.innerHTML =
            "<p>No previous chats</p>";

            return;

        }



        data.chats.forEach(chat=>{


            const row = document.createElement("div");

            row.className = "chat-row";



            const chatTitle = document.createElement("span");

            chatTitle.className="chat-title";


            chatTitle.innerText =
            chat.title || "Untitled Chat";



            chatTitle.onclick = ()=>{

                loadChat(chat.session_id);

            };




            const deleteBtn =
            document.createElement("button");


            deleteBtn.innerHTML="🗑";


            deleteBtn.onclick=(e)=>{

                e.stopPropagation();

                deleteChat(chat.session_id);

            };



            row.appendChild(chatTitle);

            row.appendChild(deleteBtn);



            historyBox.appendChild(row);



        });



    }
    catch(error){

        console.log(
            "History Error:",
            error
        );

    }

}







// =====================================
// Load Chat
// =====================================


async function loadChat(id){

    console.log("Opening chat:", id);

    session_id = id;


    messagesBox.innerHTML="";


    try{

        const response = await fetch(
            `${API_URL}/messages/${id}`
        );


        console.log("Response status:", response.status);


        const data = await response.json();


        console.log("Chat data:", data);


        if(!data.messages){

            console.log("No messages found");
            return;

        }

        

        let oldAnswer="";


        data.messages.forEach(msg=>{
        
        
        displayMessage(
        
        msg.content,
        
        msg.role==="user"
        ?
        "user"
        :
        "ai"
        
        );



        if(msg.role==="assistant"){
        
            oldAnswer = msg.content;
        
        }


        });


        lastAnswer = oldAnswer;


    }

    catch(error){

        console.log(
            "Load chat error:",
            error
        );

    }

}








// =====================================
// Upload PDF
// =====================================

async function uploadPDF(){


    const file =
    pdfFile.files[0];


    if(!file){

        alert(
            "Select PDF first"
        );

        return;

    }



    const formData =
    new FormData();



    // IMPORTANT
    formData.append(
        "user_id",
        user_id
    );



    formData.append(
        "file",
        file
    );



    uploadStatus.innerText =
    "Uploading...";



    try{


        const response =
        await fetch(

            `${API_URL}/upload`,

            {

                method:"POST",

                body:formData

            }

        );



        const data =
        await response.json();



        console.log(
            data
        );



        if(response.ok){


            uploadStatus.innerText =
            "✅ PDF Uploaded Successfully";


        }

        else{


            uploadStatus.innerText =
            "❌ Upload Failed";


        }



    }


    catch(error){


        console.log(
            "Upload Error:",
            error
        );


        uploadStatus.innerText =
        "❌ Server Error";


    }


}







// =====================================
// Check Material
// =====================================

async function checkMaterial(){

    try{

        const response =
        await fetch(
        `${API_URL}/check-material?user_id=${user_id}`
        );


        console.log(
            await response.json()
        );

    }

    catch(e){

        console.log(e);

    }

}







// =====================================
// Events
// =====================================

quizBtn.onclick =
generateQuiz;

sendButton.onclick =
sendMessage;


stopButton.onclick =
stopGeneration;


newChatButton.onclick =
async function(){

    session_id=null;

    lastAnswer="";


    messagesBox.innerHTML="";


    const flashBox=document.getElementById("flashcards");

    if(flashBox){
        flashBox.innerHTML="";
    }


    const quizBox=document.getElementById("quizBox");

    if(quizBox){
        quizBox.innerHTML="";
    }


};


if(uploadButton){

uploadButton.onclick =
uploadPDF;

}



questionInput.addEventListener(

"keydown",

(e)=>{


    if(e.key==="Enter" && !e.shiftKey){

        e.preventDefault();

        sendMessage();

    }


});

const mic =
document.getElementById("mic");


mic.onclick = startListening;

if(flashBtn){

    flashBtn.onclick = ()=>{

        if(!lastAnswer){

            alert("Ask something first");

            return;

        }

        generateflashcards(lastAnswer);

    };

}















// =====================================
// Start
// =====================================


stopButton.disabled=true;


loadHistory();

checkMaterial();

let currentAudio = null;


async function speakAnswer(text){


    try{


        const response =
        await fetch(
        `${API_URL}/text-to-speech`,
        {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },


        body:JSON.stringify({

            text:text

        })

        }

        );



        const blob =
        await response.blob();



        const audioURL =
        URL.createObjectURL(blob);



        currentAudio =
        new Audio(audioURL);



        setState("speaking");

        await currentAudio.play();



        currentAudio.onplay =
        ()=>{

            console.log(
                "Mentora speaking..."
            );

        };



        currentAudio.onended =
        ()=>{

            console.log(
                "Voice finished"
            );


            currentAudio=null;

            setState("idle");

            stopButton.disabled=true;

        };


    }


    catch(error){

        console.log(
            "Voice Error:",
            error
        );

    }


}

async function startListening(){


if(isListening)
    return;


isListening=true;



const stream =
await navigator.mediaDevices.getUserMedia({
    audio:true
});



mediaRecorder =
new MediaRecorder(stream);



audioChunks=[];



mediaRecorder.ondataavailable =
(e)=>{

    audioChunks.push(e.data);

};



mediaRecorder.onstop =
async()=>{


const audioBlob =
new Blob(
    audioChunks,
    {
        type:"audio/webm"
    }
);

stream.getTracks().forEach(
track=>track.stop()
);

await sendVoice(audioBlob);



};



mediaRecorder.start();



mic.innerHTML="🔴 Listening...";

setState("listening");



setTimeout(()=>{


if(mediaRecorder.state==="recording"){

    mediaRecorder.stop();

}


},5000);



}

async function sendVoice(blob){


const form =
new FormData();



form.append(
"file",
blob,
"voice.webm"
);



const response =
await fetch(

`${API_URL}/voice-to-text`,

{

method:"POST",

body:form

}

);



const data =
await response.json();



console.log(
"User:",
data.text
);



questionInput.value =
data.text;



await sendMessage();



mic.innerHTML="🎤";


isListening=false;


}

function stopSpeaking(){


    if(currentAudio){

        currentAudio.pause();

        currentAudio.currentTime = 0;


        URL.revokeObjectURL(
            currentAudio.src
        );


        currentAudio=null;


        console.log(
            "Mentora voice stopped"
        );

    }


    setState("idle");


}


    



function setState(state){


assistantState=state;


const box =
document.getElementById(
"voiceStatus"
);


if(state==="idle")
box.innerHTML="🟢 Ready";


if(state==="listening")
box.innerHTML="🔴 Listening";


if(state==="thinking")
box.innerHTML="🟡 Thinking";


if(state==="speaking")
box.innerHTML="🔵 Speaking";


}


async function deleteChat(id){

    if(!confirm("Delete this chat?"))
        return;

    try{

        await fetch(
            `${API_URL}/delete/${id}`,
            {
                method:"DELETE"
            }
        );

        if(session_id===id){

            session_id=null;
            messagesBox.innerHTML="";

        }

        loadHistory();

    }
    catch(err){

        console.log(err);

    }

}


async function generateflashcards(answer){


const box =
document.getElementById("flashcards");


box.innerHTML =
`
<div class="loading">
Generating flashcards... 🧠
</div>
`;



const response =
await fetch(
`${API_URL}/flashcards`,
{
method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

answer:answer.substring(0,3000)

})

});



const data =
await response.json();

console.log("FLASHCARD RESPONSE:", data);

console.log("FIRST CARD:", data.cards[0]);

showflashcards(data.cards);


}

function showflashcards(cards){

    document.getElementById("flash-section").style.display = "block";

    console.log("SHOW FLASHCARDS CALLED");
    console.log("CARDS DATA:", cards);

    const box =
    document.getElementById("flashcards");
    console.log("FLASHCARD BOX:", box);

box.innerHTML="";



requestAnimationFrame(()=>{


cards.forEach(card=>{


const div =
document.createElement("div");


div.className="flash-card";


div.innerHTML=`

<div class="card-inner">


<div class="card-front">

<h3>
❓ ${card.question}
</h3>

<p>
Click to reveal
</p>

</div>



<div class="card-back">

<h3>
✅ Answer
</h3>


<p>
${card.answer || card.content || card.explanation || "No answer available"}
</p>


</div>


</div>

`;



div.onclick=function(){

div.classList.toggle("flip");

};



box.appendChild(div);


});


});



const scrollBox =
document.getElementById("chat-scroll");


if(scrollBox){

scrollBox.scrollTo({

top:scrollBox.scrollHeight,

behavior:"smooth"

});

}


}




async function generateQuiz(){


if(!lastAnswer){

alert(
"Ask a question first"
);

return;

}


const response =
await fetch(
`${API_URL}/quiz`,
{

method:"POST",

headers:{
"Content-Type":"application/json"
},


body:JSON.stringify({

answer:lastAnswer

})

}

);



const data =
await response.json();



showQuiz(data.questions);


setTimeout(()=>{

    messagesBox.scrollTo({

        top:messagesBox.scrollHeight,

        behavior:"smooth"

    });


},200);



}



function showQuiz(questions){
document.getElementById("quiz-section").style.display = "block";
const box =
document.getElementById(
"quizBox"
);


box.innerHTML="";



questions.forEach(
(q,index)=>{


let div =
document.createElement(
"div"
);


div.className="quiz-card";



div.innerHTML=`

<h3>
${index+1}. ${q.question}
</h3>


${q.options.map(
option=>`

<label>

<input 
type="radio"
name="q${index}"
value="${option}"
>

${option}

</label>

<br>

`
).join("")}



<button onclick='checkAnswer(
${JSON.stringify(q)},
${index}
)'>
Check
</button>


<p id="result${index}">
</p>


`;



box.appendChild(div);


});
// ADD THIS HERE

box.scrollIntoView({

behavior:"smooth",

block:"center"

});


}


function checkAnswer(q,index){


const selected =
document.querySelector(
`input[name="q${index}"]:checked`
);



const result =
document.getElementById(
`result${index}`
);



if(!selected){

result.innerHTML=
"Select option first";

return;

}



if(selected.value===q.answer){


result.innerHTML=
"✅ Correct\n\n"+
q.explanation;


}

else{


result.innerHTML=
"❌ Wrong\n\nCorrect: "+
q.answer+
"\n\n"+
q.explanation;


}


}




        