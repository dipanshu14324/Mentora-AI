export function getUserId(){

    let userId = localStorage.getItem(
        "mentora_user_id"
    );


    if(!userId){

        userId =
        crypto.randomUUID();


        localStorage.setItem(
            "mentora_user_id",
            userId
        );

    }


    return userId;

}