from dataclasses import dataclass, asdict
from datetime import date
from bson.objectid import ObjectId

@dataclass
class Person:
    id: int
    name: str
    phone: str
    age: int
    birthdate: date
    passport_id: str | None = None        

    def save(self, coll):
        data = asdict(self)
        data['birthdate'] = self.birthdate.isoformat()
        if self.passport_id is None:
            data.pop('passport_id')
        inserted_id = coll.insert_one(data).inserted_id
        return str(inserted_id)

    def update(self, coll, document_id: str):
        filtro = {"_id": ObjectId(document_id)}
        nuevos_valores = {
            "$set": {
                "id": self.id,
                "name": self.name,
                "phone": self.phone,
                "age": self.age,
                "birthdate": self.birthdate.isoformat(),
                **({"passport_id": self.passport_id} if self.passport_id else {})
            }
        }
        resultado = coll.update_one(filtro, nuevos_valores)
        if resultado.matched_count:
            print("Persona actualizada correctamente")
        else:
            print("No se encontró persona con ese ID")
        return resultado
