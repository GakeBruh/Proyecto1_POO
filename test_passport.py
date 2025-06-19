import unittest
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from pymongo import MongoClient
from classes import Person, Passport
from datetime import date

load_dotenv()

class TestPersonPassport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.uri = os.getenv("MONGO_URI")
        cls.client = MongoClient(cls.uri, tls=True, tlsAllowInvalidCertificates=True)
        cls.db = cls.client["passports_db"]
        cls.persons_coll = cls.db["persons"]
        cls.passports_coll = cls.db["passports"]
        cls.test_ids = []

    def test_relacion(self):
        # Paso 1: Crear persona y guardar
        persona = Person(id=101, name="Test User", phone="8888-1234", age=25, birthdate=date(2000, 1, 1))
        persona_id = persona.save(self.persons_coll)
        self.test_ids.append(ObjectId(persona_id))

        pasaporte = Passport(
            number="T123456",
            country="Honduras",
            expiration_date=date(2030, 1, 1),
            person_id=persona_id
        )
        passport_id = pasaporte.save(self.passports_coll)
        self.test_ids.append(ObjectId(passport_id))

        persona.passport_id = passport_id
        persona.update(self.persons_coll, persona_id)

        passport_doc = self.passports_coll.find_one({"_id": ObjectId(passport_id)})
        person_doc = self.persons_coll.find_one({"_id": ObjectId(persona_id)})

        self.assertEqual(str(passport_doc["person_id"]), persona_id)
        self.assertEqual(str(person_doc["passport_id"]), passport_id)

    def test_actualizacion(self):
        persona = Person(id=102, name="Actualizable", phone="9999-5678", age=28, birthdate=date(1995, 12, 31))
        persona_id = persona.save(self.persons_coll)
        self.test_ids.append(ObjectId(persona_id))

        pasaporte = Passport(
            number="ACT567",
            country="El Salvador",
            expiration_date=date(2032, 6, 15),
            person_id=persona_id
        )
        passport_id = pasaporte.save(self.passports_coll)
        self.test_ids.append(ObjectId(passport_id))

        persona.passport_id = passport_id
        result = persona.update(self.persons_coll, persona_id)
        self.assertEqual(result.modified_count, 1)

        updated = self.persons_coll.find_one({"_id": ObjectId(persona_id)})
        self.assertEqual(updated["passport_id"], passport_id)

    def tearDown(self):
        for _id in self.test_ids:
            self.persons_coll.delete_one({"_id": _id})
            self.passports_coll.delete_one({"_id": _id})
        self.test_ids.clear()

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

if __name__ == "__main__":
    unittest.main()


