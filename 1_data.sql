CREATE TABLE public.data
(
    id_data bigserial NOT NULL,
    cod_localidad integer,
    id_provincia smallserial,
    id_departamento integer,
    categoria text,
    provincia text,
    localidad text,
    nombre text,
    domicilio text,
    cp text,
    num_tel text,
    mail text,
    web text,
    fecha_carga timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id_data)
);

ALTER TABLE IF EXISTS public.data
    OWNER to postgres;