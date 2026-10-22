from fastapi import APIRouter

from app.services.vector_store import get_vector_store


router = APIRouter()



@router.get("/check-material")
def check_material(
    user_id:str="student1"
):


    vector_store = get_vector_store(
        user_id
    )


    if vector_store:


        return {

            "exists":True,

            "message":
            "Study material available"

        }


    return {

        "exists":False,

        "message":
        "No study material found"

    }