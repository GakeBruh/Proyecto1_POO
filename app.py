import os
from datetime import date
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from classes import Person, Passport 


load_dotenv()

uri = os.getenv("MONGO_URI")  

def get_collection(uri, db="passports_db", col="persons"):
    client = MongoClient(
        uri,
        server_api=ServerApi("1"),
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    client.admin.command("ping")  

    return client[db][col]

def main():
    persons_coll = get_collection(uri, db="passports_db", col="persons")
    p = Person(5, "Kevin", "99549798", 50, date(2005, 1, 12))  
    p_id = p.save(persons_coll)
    print("Persona guardada con ID:", p_id)

    passports_coll = get_collection(uri, db="passports_db", col="passports")
    passport = Passport("H18528","Honduras",date(2030, 5, 12),person_id=p_id)
    pass_id = passport.save(passports_coll)

    p.passport_id = pass_id
    p.update(persons_coll, p_id)

    print("Passport ID:", pass_id)


if __name__ == "__main__":
    main()
