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

    def save(self, coll):
        data = asdict(self)
        data['birthdate'] = self.birthdate.isoformat()  
        return str(coll.insert_one(data).inserted_id)
    
    def update(self, coll, document_id):
        filtro ={"_id": ObjectId(document_id)}
        nuevos_valores = {
            "$set":{
                "id": self.id,
                "name":self.name,
                "phone" : self.phone,
                "age" : self.age,
                "birthdate" : self.birthdate.isoformat()
            }
        }
        resultado = coll.update_one(filtro, nuevos_valores)
        if  resultado.matched_count > 0:
            print("Persona actualizada correctamente")
        else:
            print("No se encontro a ninguna persona con ese ID intente nuevamente")
        return resultado