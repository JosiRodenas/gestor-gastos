from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

BASE_DATOS = "gastos.db"
CATEGORIAS = ["Alimentación", "Transporte", "Ocio", "Vivienda", "Otros"]

app = FastAPI()


class GastoNuevo(BaseModel):
    descripcion: str
    importe: float
    categoria: str


@app.get("/")
def inicio():
    return {"mensaje": "Hola"}


@app.get("/gastos")
def obtener_gastos():
    conexion = sqlite3.connect(BASE_DATOS)
    filas = conexion.execute(
        "SELECT id, descripcion, importe, categoria FROM gastos"
    ).fetchall()
    conexion.close()

    gastos = []
    for id_gasto, descripcion, importe, categoria in filas:
        gastos.append({
            "id": id_gasto,
            "descripcion": descripcion,
            "importe": importe,
            "categoria": categoria,
        })

    return gastos


@app.post("/gastos", status_code=201)
def crear_gasto(gasto: GastoNuevo):
    if gasto.categoria not in CATEGORIAS:
        raise HTTPException(status_code=400, detail=f"Categoría no válida. Opciones: {CATEGORIAS}")

    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.execute(
        "INSERT INTO gastos (descripcion, importe, categoria) VALUES (?, ?, ?)",
        (gasto.descripcion, gasto.importe, gasto.categoria)
    )
    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()

    return {
        "id": nuevo_id,
        "descripcion": gasto.descripcion,
        "importe": gasto.importe,
        "categoria": gasto.categoria,
    }


@app.delete("/gastos/{id_gasto}", status_code=204)
def borrar_gasto(id_gasto: int):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.execute("DELETE FROM gastos WHERE id = ?", (id_gasto,))
    conexion.commit()
    borrados = cursor.rowcount
    conexion.close()

    if borrados == 0:
        raise HTTPException(status_code=404, detail=f"No existe el gasto {id_gasto}")





@app.get("/gastos/resumen")
def resumen():
    conexion = sqlite3.connect(BASE_DATOS)
    filas = conexion.execute("""
        SELECT categoria, SUM(importe), COUNT(*)
        FROM gastos
        GROUP BY categoria
    """).fetchall()
    conexion.close()

    return [
        {"categoria": categoria, "total": total, "cantidad": cantidad}
        for categoria, total, cantidad in filas
    ]