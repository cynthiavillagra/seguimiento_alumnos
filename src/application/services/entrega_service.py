"""
Servicio de Aplicación: EntregaTPService
Sistema de Seguimiento de Alumnos
"""

from typing import List, Optional
from datetime import date
from src.domain.entities.entrega_tp import EntregaTP
from src.infrastructure.repositories.base.entrega_tp_repository_base import EntregaTPRepositoryBase
from src.infrastructure.repositories.base.tp_repository_base import TrabajoPracticoRepositoryBase
from src.infrastructure.repositories.base.inscripcion_repository_base import InscripcionRepositoryBase
from src.domain.exceptions.domain_exceptions import (
    TrabajoPracticoNoEncontradoException,
    AlumnoNoInscriptoException
)

class EntregaTPService:
    
    def __init__(
        self, 
        entrega_repo: EntregaTPRepositoryBase, 
        tp_repo: TrabajoPracticoRepositoryBase,
        inscripcion_repo: InscripcionRepositoryBase
    ):
        self.entrega_repo = entrega_repo
        self.tp_repo = tp_repo
        self.inscripcion_repo = inscripcion_repo
    
    def registrar_entrega(
        self, 
        tp_id: int, 
        alumno_id: int, 
        fecha_entrega_real: Optional[date] = None, 
        entregado: bool = True,
        estado: str = 'pendiente',
        nota: Optional[float] = None,
        observaciones: Optional[str] = None
    ) -> EntregaTP:
        # Obtener TP
        tp = self.tp_repo.obtener_por_id(tp_id)
        if not tp:
            raise TrabajoPracticoNoEncontradoException(f"TP {tp_id} no encontrado")
            
        # Validar inscripción
        if not self.inscripcion_repo.existe(alumno_id, tp.curso_id):
            raise AlumnoNoInscriptoException(f"El alumno {alumno_id} no está inscripto en el curso de este TP")
            
        # Calcular si es tardía
        es_tardia = False
        if fecha_entrega_real and tp.fecha_entrega:
             if fecha_entrega_real > tp.fecha_entrega:
                 es_tardia = True
        
        # Si no se pasa fecha real, asumimos hoy si se marca como entregado
        if entregado and not fecha_entrega_real:
             today = date.today()
             fecha_entrega_real = today
             if today > tp.fecha_entrega:
                 es_tardia = True
        elif not entregado:
             fecha_entrega_real = None
             es_tardia = False # Si no entregó, no es "entrega tardía" (es no entrega)

        entrega = EntregaTP(
            trabajo_practico_id=tp_id,
            alumno_id=alumno_id,
            fecha_entrega_real=fecha_entrega_real,
            entregado=entregado,
            es_tardia=es_tardia,
            estado=estado,
            nota=nota,
            observaciones=observaciones
        )
        
        return self.entrega_repo.crear_o_actualizar(entrega)
    
    def obtener_entrega(self, id: int) -> EntregaTP:
        entrega = self.entrega_repo.obtener_por_id(id)
        if not entrega:
            # TODO: Exception específica
             raise ValueError(f"Entrega {id} no encontrada")
        return entrega

    def obtener_entrega_alumno_tp(self, alumno_id: int, tp_id: int) -> Optional[EntregaTP]:
        return self.entrega_repo.obtener_por_alumno_y_tp(alumno_id, tp_id)
    
    def listar_entregas_tp(self, tp_id: int) -> List[EntregaTP]:
        if not self.tp_repo.obtener_por_id(tp_id):
            raise TrabajoPracticoNoEncontradoException(f"TP {tp_id} no encontrado")
        return self.entrega_repo.obtener_por_tp(tp_id)

    def eliminar_entrega(self, id: int) -> bool:
        return self.entrega_repo.eliminar(id)
