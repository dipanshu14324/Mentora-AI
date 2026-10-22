import { useState } from "react";

import Upload from "./components/Upload";
import Chat from "./components/Chat";

import { getUserId } from "./utils/user";


function App(){


const [userId] = useState(
    getUserId()
);


const [level,setLevel] = useState(
    "Beginner"
);



return (

<div className="app">


<h1>
🤖 Mentora AI Tutor
</h1>



<h2>
🎓 Student Learning Profile
</h2>

<p
style={{
    marginTop: "-8px",
    color: "#666"
}}
>
Choose your current knowledge level. Mentora will personalize every explanation based on this.
</p>


<select

value={level}

onChange={
e=>setLevel(e.target.value)
}

>

<option>
Beginner
</option>

<option>
Intermediate
</option>

<option>
Advanced
</option>

</select>



<Upload

userId={userId}

/>



<Chat

userId={userId}

level={level}

/>



</div>

);

}


export default App;