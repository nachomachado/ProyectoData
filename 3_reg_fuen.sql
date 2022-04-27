CREATE TABLE public.reg_fuente
(
    id serial NOT NULL,
    fuente text,
    cantidad integer,
    fecha_carga timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.reg_fuente
    OWNER to postgres;