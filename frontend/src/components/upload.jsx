import { useState } from "react";
import axios from "axios";


function Upload({ userId }) {


    const [file, setFile] = useState(null);

    const [message, setMessage] = useState("");



    const uploadPDF = async () => {


        if (!file) {

            setMessage("Please select a PDF first");
            return;

        }



        if (!userId) {

            setMessage("User not found");
            return;

        }



        const formData = new FormData();


        formData.append(
            "file",
            file
        );


        formData.append(
            "user_id",
            userId
        );



        try {


            setMessage(
                "Uploading PDF... Please wait"
            );



            const response = await axios.post(

                "http://127.0.0.1:8000/upload",

                formData

            );



            console.log(
                "UPLOAD RESPONSE:",
                response.data
            );



            setMessage(

                `✅ ${response.data.message}
                
                User: ${response.data.user_id}

                Chunks: ${response.data.chunks}`

            );


        }


        catch(error){


            console.log(
                "UPLOAD ERROR:",
                error
            );


            setMessage(
                "❌ Upload failed"
            );


        }


    };



    return (

        <div className="card">


            <h2>
                📚 Upload PDF Notes
            </h2>


            <p>
                User ID: {userId}
            </p>



            <input

                type="file"

                accept="application/pdf"

                onChange={
                    e=>setFile(
                        e.target.files[0]
                    )
                }

            />


            <br/>
            <br/>


            <button
                onClick={uploadPDF}
            >

                Upload PDF

            </button>



            <p>
                {message}
            </p>



        </div>

    );


}


export default Upload;