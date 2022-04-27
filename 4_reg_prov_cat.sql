CREATE TABLE public.reg_prov_cat
(
    id_reg serial NOT NULL,
    provincia integer,
    categoria integer,
    cantidad integer,
    fecha_carga timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id_reg)
);

ALTER TABLE IF EXISTS public.reg_prov_cat
    OWNER to postgres;