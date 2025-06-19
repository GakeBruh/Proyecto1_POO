from dataclasses import dataclass, asdict
from datetime import date
from bson.objectid import ObjectId

@dataclass
class Passport:
    number: str
    country: str
    expiration_date: date
    person_id: int

    def save(self, coll):
        data = asdict(self)
        data['expiration_date'] = self.expiration_date.isoformat()
        return str(coll.insert_one(data).inserted_id)
    
    def update(self, coll, document_id):
        filtro = {"_id": ObjectId(document_id)}
        nuevos_valores = {
            "$set": {
                "number": self.number,
                "country": self.country,
                "expiration_date": self.expiration_date.isoformat(),
                "person_id": self.person_id
            }
        }
        resultado = coll.update_one(filtro, nuevos_valores)
        if resultado.matched_count > 0:
            print("Pasaporte actualizado correctamente.")
        else:
            print("No se encontro pasaporte con ese ID intente nuevamente.")
        return resultado