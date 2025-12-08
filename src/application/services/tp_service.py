"""
Servicio de Aplicación: TrabajoPracticoService
Sistema de Seguimiento de Alumnos
"""

from typing import List, Optional
from datetime import date
from src.domain.entities.trabajo_practico import TrabajoPractico
from src.infrastructure.repositories.base.tp_repository_base import TrabajoPracticoRepositoryBase
from src.infrastructure.repositories.base.curso_repository_base import CursoRepositoryBase
from src.domain.exceptions.domain_exceptions import (
    CursoNoEncontradoException,
    TrabajoPracticoNoEncontradoException
)

class TrabajoPracticoService:
    
    def __init__(self, tp_repo: TrabajoPracticoRepositoryBase, curso_repo: CursoRepositoryBase):
        self.tp_repo = tp_repo
        self.curso_repo = curso_repo
    
    def crear_tp(self, curso_id: int, titulo: str, fecha_entrega: date, descripcion: Optional[str] = None) -> TrabajoPractico:
        if not self.curso_repo.obtener_por_id(curso_id):
            raise CursoNoEncontradoException(f"Curso {curso_id} no encontrado")
            
        tp = TrabajoPractico(
            curso_id=curso_id,
            titulo=titulo,
            fecha_entrega=fecha_entrega,
            descripcion=descripcion
        )
        return self.tp_repo.crear(tp)
    
    def obtener_tp(self, id: int) -> TrabajoPractico:
        tp = self.tp_repo.obtener_por_id(id)
        if not tp:
            raise TrabajoPracticoNoEncontradoException(f"TP {id} no encontrado")
        return tp
    
    def listar_tps_curso(self, curso_id: int) -> List[TrabajoPractico]:
        if not self.curso_repo.obtener_por_id(curso_id):
             raise CursoNoEncontradoException(f"Curso {curso_id} no encontrado")
        return self.tp_repo.obtener_por_curso(curso_id)

    def listar_todos_tps(self) -> List[TrabajoPractico]:
        """Lista todos los TPs de todos los cursos"""
        return self.tp_repo.obtener_todos()

    def actualizar_tp(
        self, 
        tp_id: int, 
        titulo: Optional[str] = None, 
        descripcion: Optional[str] = None,
        fecha_entrega: Optional[date] = None
    ) -> TrabajoPractico:
        tp = self.obtener_tp(tp_id)
        
        if titulo is not None:
            tp.titulo = titulo
        if descripcion is not None:
             tp.descripcion = descripcion
        if fecha_entrega is not None:
             tp.fecha_entrega = fecha_entrega
             
        return self.tp_repo.actualizar(tp)

    def eliminar_tp(self, tp_id: int) -> bool:
        return self.tp_repo.eliminar(tp_id)
