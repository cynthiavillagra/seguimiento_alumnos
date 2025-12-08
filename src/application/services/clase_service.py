"""
Servicio de Aplicación: ClaseService
Sistema de Seguimiento de Alumnos
"""

from typing import List, Optional
from datetime import date
from src.domain.entities.clase import Clase
from src.infrastructure.repositories.base.clase_repository_base import ClaseRepositoryBase
from src.infrastructure.repositories.base.curso_repository_base import CursoRepositoryBase
from src.domain.exceptions.domain_exceptions import (
    ClaseNoEncontradaException,
    CursoNoEncontradoException,
    BusinessRuleException
)

class ClaseService:
    
    def __init__(self, clase_repo: ClaseRepositoryBase, curso_repo: CursoRepositoryBase):
        self.clase_repo = clase_repo
        self.curso_repo = curso_repo
    
    def registrar_clase(
        self,
        curso_id: int,
        numero_clase: int,
        fecha: date,
        tema: Optional[str] = None
    ) -> Clase:
        # Validar curso
        if not self.curso_repo.obtener_por_id(curso_id):
            raise CursoNoEncontradoException(f"Curso {curso_id} no encontrado")
            
        # Validar si ya existe clase con ese numero ?? El repo lo hace con UNIQUE constraint
        # Validar fecha ??
        
        clase = Clase(
            curso_id=curso_id,
            numero_clase=numero_clase,
            fecha=fecha,
            tema=tema
        )
        return self.clase_repo.crear(clase)
    
    def obtener_clase(self, id: int) -> Clase:
        clase = self.clase_repo.obtener_por_id(id)
        if not clase:
            raise ClaseNoEncontradaException(f"Clase {id} no encontrada")
        return clase
    
    def listar_clases_curso(self, curso_id: int) -> List[Clase]:
        if not self.curso_repo.obtener_por_id(curso_id):
            raise CursoNoEncontradoException(f"Curso {curso_id} no encontrado")
        return self.clase_repo.obtener_por_curso(curso_id)
    
    def actualizar_clase(
        self,
        clase_id: int,
        numero_clase: Optional[int] = None,
        fecha: Optional[date] = None,
        tema: Optional[str] = None
    ) -> Clase:
        clase = self.obtener_clase(clase_id)
        
        if numero_clase is not None:
            clase.numero_clase = numero_clase
        if fecha is not None:
            clase.fecha = fecha
        if tema is not None:
            clase.tema = tema
            
        return self.clase_repo.actualizar(clase)
    
    def eliminar_clase(self, id: int) -> bool:
        return self.clase_repo.eliminar(id)
