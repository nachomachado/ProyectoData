CREATE TABLE public.cant_pant_buta_espa
(
    id_cant smallserial NOT NULL,
    provincia text,
    cant_pantallas integer,
    cant_butacas integer,
    cant_esp_incaa integer,
    fecha_carga timestamp with time zone DEFAULT NOW(),
    PRIMARY KEY (id_cant)
);

ALTER TABLE IF EXISTS public.cant_pant_buta_espa
    OWNER to postgres;