from fastapi import APIRouter, HTTPException
from models import TeacherCreate, Teacher  # Importar los modelos apropiados
from database import get_db_connection
from typing import List

router = APIRouter()

# Ruta para crear un nuevo profesor
@router.post("/teachers/", response_model=Teacher)
def create_teacher(teacher: TeacherCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar si el email ya existe
        cursor.execute("SELECT * FROM teachers WHERE email = %s", (teacher.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        # Insertar el profesor
        query = """
        INSERT INTO teachers (name, email)
        VALUES (%s, %s)
        """
        values = (teacher.name, teacher.email)

        cursor.execute(query, values)
        conn.commit()

        teacher_id = cursor.lastrowid
        return Teacher(teacher_id=teacher_id, name=teacher.name, email=teacher.email)

    except Exception as e:
        conn.rollback()  # Hacer rollback en caso de error
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()

# Ruta para crear múltiples profesores
@router.post("/teachers/bulk/", response_model=List[Teacher])
def create_teachers(teachers: List[TeacherCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar si alguno de los emails ya existe
        for teacher in teachers:
            cursor.execute("SELECT * FROM teachers WHERE email = %s", (teacher.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail=f"El email '{teacher.email}' ya está registrado")

        # Preparar la consulta de inserción
        query = """
        INSERT INTO teachers (name, email)
        VALUES (%s, %s)
        """
        values = [(teacher.name, teacher.email) for teacher in teachers]

        # Ejecutar el insert masivo
        cursor.executemany(query, values)
        conn.commit()

        # Obtener los IDs generados
        teacher_ids = [cursor.lastrowid + i for i in range(len(values))]

        # Retornar la lista de profesores insertados
        return [Teacher(teacher_id=teacher_id, name=teacher.name, email=teacher.email) for teacher_id, teacher in zip(teacher_ids, teachers)]
    
    except Exception as e:
        conn.rollback()  # Hacer rollback en caso de error
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()

# Ruta para listar todos los profesores
@router.get("/teachers/", response_model=List[Teacher])
def list_teachers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM teachers"
        cursor.execute(query)
        teachers = cursor.fetchall()
        return [Teacher(teacher_id=teacher['teacher_id'], name=teacher['name'], email=teacher['email']) for teacher in teachers]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()

# Ruta para eliminar un profesor por ID
@router.delete("/teachers/{teacher_id}", response_model=dict)
def delete_teacher(teacher_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar si el profesor existe
        cursor.execute("SELECT * FROM teachers WHERE teacher_id = %s", (teacher_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Profesor no encontrado")

        # Eliminar el profesor
        cursor.execute("DELETE FROM teachers WHERE teacher_id = %s", (teacher_id,))
        conn.commit()

        return {"detail": "Profesor eliminado exitosamente"}
    
    except Exception as e:
        conn.rollback()  # Hacer rollback en caso de error
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()
