-- Migración: Agregar campos nota, estado y observaciones a entrega_tp
-- Fecha: 2024-12-08

-- Agregar campo estado
ALTER TABLE entrega_tp 
ADD COLUMN IF NOT EXISTS estado TEXT DEFAULT 'pendiente';

-- Agregar campo nota
ALTER TABLE entrega_tp 
ADD COLUMN IF NOT EXISTS nota REAL;

-- Agregar campo observaciones
ALTER TABLE entrega_tp 
ADD COLUMN IF NOT EXISTS observaciones TEXT;

-- Agregar constraints (si no existen)
-- Nota: PostgreSQL no permite ADD CONSTRAINT IF NOT EXISTS, así que usamos DO block
DO $$ 
BEGIN
    -- Verificar constraint de nota
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'entrega_tp_nota_check') THEN
        ALTER TABLE entrega_tp ADD CONSTRAINT entrega_tp_nota_check CHECK (nota IS NULL OR (nota >= 1 AND nota <= 10));
    END IF;
    
    -- Verificar constraint de estado
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'entrega_tp_estado_check') THEN
        ALTER TABLE entrega_tp ADD CONSTRAINT entrega_tp_estado_check CHECK (estado IN ('pendiente', 'entregado', 'tarde', 'no_entregado'));
    END IF;
END $$;
