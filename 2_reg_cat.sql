CREATE TABLE public.reg_cat
(
    id serial NOT NULL,
    categoria text,
    cantidad integer,
    fecha_carga timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.reg_cat
    OWNER to postgres;