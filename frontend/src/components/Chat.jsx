import { useState, useRef } from "react";
import ReactMarkdown from "react-markdown";


function Chat({ userId, level }) {


    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);


    const abortController = useRef(null);



    // Answer style

    const [style, setStyle] = useState(
        "Concept Learning"
    );





    const askQuestion = async () => {


        if (!question.trim() || loading) {

            return;

        }



        const userQuestion = question;



        setMessages(prev => [

            ...prev,

            {
                role:"user",
                content:userQuestion
            }

        ]);



        setQuestion("");

        setLoading(true);



        // Empty AI message

        setMessages(prev => [

            ...prev,

            {
                role:"assistant",
                content:""
            }

        ]);




        try {


            abortController.current =
                new AbortController();




            const response = await fetch(

                "http://127.0.0.1:8000/chat/stream",

                {


                    method:"POST",


                    headers:{

                        "Content-Type":
                        "application/json"

                    },


                    signal:
                    abortController.current.signal,



                    body:JSON.stringify({

                        session_id:userId,

                        user_id:userId,

                        question:userQuestion,

                        level:level,

                        style:style

                    })


                }

            );





            if(!response.body){

                throw new Error(
                    "Streaming unavailable"
                );

            }





            const reader =
                response.body.getReader();



            const decoder =
                new TextDecoder();



            let aiMessage = "";





            while(true){



                const {

                    done,

                    value


                } = await reader.read();




                if(done){

                    break;

                }




                const chunk =
                    decoder.decode(
                        value,
                        {
                            stream:true
                        }
                    );



                aiMessage += chunk;





                setMessages(prev=>{


                    const updated=[
                        ...prev
                    ];



                    updated[
                        updated.length-1
                    ]={

                        role:"assistant",

                        content:aiMessage

                    };



                    return updated;


                });



            }



        }





        catch(error){



            // User clicked Stop

            if(error.name==="AbortError"){


                setMessages(prev=>{


                    const updated=[
                        ...prev
                    ];



                    updated[
                        updated.length-1
                    ]={

                        role:"assistant",

                        content:
                        "⏹️ Response stopped"

                    };



                    return updated;


                });



                return;

            }




            console.log(
                "STREAM ERROR:",
                error
            );



            setMessages(prev=>[


                ...prev,


                {

                    role:"assistant",

                    content:
                    "❌ Unable to get response from Mentora AI"

                }


            ]);



        }





        finally{


            setLoading(false);

            abortController.current=null;


        }



    };







    const stopGeneration = ()=>{


        if(abortController.current){


            abortController.current.abort();


        }


    };







    return (

        <div className="card">



            <h2>
                🎓 Mentora Tutor
            </h2>




            {/* Answer Style */}

            <label>

                Answer Style:

            </label>




            <select

                value={style}

                onChange={
                    e=>setStyle(
                        e.target.value
                    )
                }

            >


                <option>
                    Concept Learning
                </option>


                <option>
                    Exam Preparation
                </option>


                <option>
                    Interview Preparation
                </option>


                <option>
                    Quick Revision
                </option>



            </select>







            <div className="chat-box">


            {

                messages.map(

                    (msg,index)=>(


                    <div


                        key={index}


                        className={

                            msg.role==="user"

                            ?

                            "user-msg"

                            :

                            "ai-msg"

                        }


                    >


                        <strong>


                        {

                            msg.role==="user"

                            ?

                            "Student"

                            :

                            "Mentora AI"


                        }


                        </strong>



                        <ReactMarkdown>

                            {msg.content}

                        </ReactMarkdown>



                    </div>


                    )

                )

            }






            {

                loading &&


                <div className="ai-msg">

                    Mentora AI is generating...

                </div>


            }





            </div>









            <textarea


                rows="4"


                placeholder="Ask your question..."



                value={question}



                onChange={

                    e=>setQuestion(
                        e.target.value
                    )

                }




                onKeyDown={

                    e=>{


                        if(

                            e.key==="Enter"

                            &&

                            !e.shiftKey

                        ){


                            e.preventDefault();


                            askQuestion();


                        }


                    }

                }



            />







            {

                loading ?



                <button

                    onClick={stopGeneration}

                >

                    ⏹ Stop Generating

                </button>



                :



                <button

                    onClick={askQuestion}

                >

                    Ask

                </button>



            }





        </div>

    );


}


export default Chat;