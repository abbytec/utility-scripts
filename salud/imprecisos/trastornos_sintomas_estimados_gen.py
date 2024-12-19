import pandas as pd

trastornos = [
    'Depresión mayor',
    'Trastorno de ansiedad generalizada',
    'Fobia social',
    'Trastorno de pánico',
    'Fobia específica',
    'Trastorno obsesivo-compulsivo',
    'Trastorno de estrés postraumático',
    'Trastorno bipolar I',
    'Trastorno bipolar II',
    'Trastorno ciclotímico',
    'Esquizofrenia',
    'Trastorno esquizoafectivo',
    'Anorexia nerviosa',
    'Bulimia nerviosa',
    'Trastorno por atracón',
    'Trastorno límite de la personalidad',
    'Trastorno antisocial de la personalidad',
    'Trastorno narcisista de la personalidad',
    'Trastorno evitativo de la personalidad',
    'Trastorno dependiente de la personalidad',
    'TDAH',
    'Trastorno del espectro autista',
    'Distimia (Trastorno depresivo persistente)',
    'Trastorno por consumo de alcohol',
    'Trastorno por consumo de opioides',
    'Trastorno por consumo de estimulantes',
    'Trastorno de síntomas somáticos',
    'Trastorno de ansiedad por enfermedad',
    'Trastorno de despersonalización/desrealización',
    'Trastorno de identidad disociativo'
]

sintomas = [
    'Ansiedad', 
    'Estado_ánimo_bajo', 
    'Anhedonia', 
    'Problemas_de_sueño', 
    'Fatiga', 
    'Pensamientos_intrusivos',
    'Miedos_específicos', 
    'Comportamiento_compulsivo', 
    'Flashbacks', 
    'Alucinaciones', 
    'Delirios', 
    'Autoestima_baja', 
    'Irritabilidad', 
    'Cambios_de_humor', 
    'Dificultad_de_concentración', 
    'Sentimientos_de_culpa', 
    'Ideación_suicida', 
    'Restricción_alimentaria', 
    'Descontrol_alimentario', 
    'Abuso_de_sustancias', 
    'Despersonalización', 
    'Desrealización', 
    'Hipervigilancia', 
    'Aislamiento_social', 
    'Conductas_evitativas'
]

# Valores estimativos (0-10) no aleatorios, intentando reflejar ciertas tendencias típicas:

data = {
    'Depresión mayor': {
        'Ansiedad':5,'Estado_ánimo_bajo':9,'Anhedonia':9,'Problemas_de_sueño':7,'Fatiga':8,'Pensamientos_intrusivos':6,
        'Miedos_específicos':3,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':9,
        'Irritabilidad':6,'Cambios_de_humor':7,'Dificultad_de_concentración':8,'Sentimientos_de_culpa':8,'Ideación_suicida':9,
        'Restricción_alimentaria':3,'Descontrol_alimentario':2,'Abuso_de_sustancias':5,'Despersonalización':2,'Desrealización':2,
        'Hipervigilancia':3,'Aislamiento_social':9,'Conductas_evitativas':6
    },
    'Trastorno de ansiedad generalizada': {
        'Ansiedad':9,'Estado_ánimo_bajo':5,'Anhedonia':4,'Problemas_de_sueño':7,'Fatiga':6,'Pensamientos_intrusivos':7,
        'Miedos_específicos':6,'Comportamiento_compulsivo':3,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':5,
        'Irritabilidad':6,'Cambios_de_humor':5,'Dificultad_de_concentración':7,'Sentimientos_de_culpa':5,'Ideación_suicida':3,
        'Restricción_alimentaria':2,'Descontrol_alimentario':3,'Abuso_de_sustancias':4,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':8,'Aislamiento_social':5,'Conductas_evitativas':7
    },
    'Fobia social': {
        'Ansiedad':8,'Estado_ánimo_bajo':6,'Anhedonia':4,'Problemas_de_sueño':5,'Fatiga':4,'Pensamientos_intrusivos':5,
        'Miedos_específicos':9,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':8,
        'Irritabilidad':4,'Cambios_de_humor':4,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':5,'Ideación_suicida':4,
        'Restricción_alimentaria':2,'Descontrol_alimentario':3,'Abuso_de_sustancias':3,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':7,'Aislamiento_social':9,'Conductas_evitativas':8
    },
    'Trastorno de pánico': {
        'Ansiedad':9,'Estado_ánimo_bajo':5,'Anhedonia':4,'Problemas_de_sueño':8,'Fatiga':6,'Pensamientos_intrusivos':6,
        'Miedos_específicos':8,'Comportamiento_compulsivo':2,'Flashbacks':3,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':5,
        'Irritabilidad':5,'Cambios_de_humor':5,'Dificultad_de_concentración':6,'Sentimientos_de_culpa':4,'Ideación_suicida':3,
        'Restricción_alimentaria':3,'Descontrol_alimentario':3,'Abuso_de_sustancias':4,'Despersonalización':4,'Desrealización':4,
        'Hipervigilancia':8,'Aislamiento_social':6,'Conductas_evitativas':7
    },
    'Fobia específica': {
        'Ansiedad':7,'Estado_ánimo_bajo':4,'Anhedonia':3,'Problemas_de_sueño':4,'Fatiga':4,'Pensamientos_intrusivos':4,
        'Miedos_específicos':9,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':4,
        'Irritabilidad':3,'Cambios_de_humor':3,'Dificultad_de_concentración':4,'Sentimientos_de_culpa':3,'Ideación_suicida':2,
        'Restricción_alimentaria':2,'Descontrol_alimentario':2,'Abuso_de_sustancias':2,'Despersonalización':2,'Desrealización':2,
        'Hipervigilancia':6,'Aislamiento_social':5,'Conductas_evitativas':8
    },
    'Trastorno obsesivo-compulsivo': {
        'Ansiedad':8,'Estado_ánimo_bajo':5,'Anhedonia':4,'Problemas_de_sueño':6,'Fatiga':5,'Pensamientos_intrusivos':9,
        'Miedos_específicos':7,'Comportamiento_compulsivo':9,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':6,
        'Irritabilidad':5,'Cambios_de_humor':4,'Dificultad_de_concentración':7,'Sentimientos_de_culpa':7,'Ideación_suicida':4,
        'Restricción_alimentaria':2,'Descontrol_alimentario':2,'Abuso_de_sustancias':3,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':5,'Aislamiento_social':5,'Conductas_evitativas':6
    },
    'Trastorno de estrés postraumático': {
        'Ansiedad':8,'Estado_ánimo_bajo':6,'Anhedonia':5,'Problemas_de_sueño':8,'Fatiga':6,'Pensamientos_intrusivos':8,
        'Miedos_específicos':5,'Comportamiento_compulsivo':3,'Flashbacks':9,'Alucinaciones':2,'Delirios':2,'Autoestima_baja':5,
        'Irritabilidad':7,'Cambios_de_humor':6,'Dificultad_de_concentración':6,'Sentimientos_de_culpa':6,'Ideación_suicida':4,
        'Restricción_alimentaria':2,'Descontrol_alimentario':3,'Abuso_de_sustancias':5,'Despersonalización':5,'Desrealización':5,
        'Hipervigilancia':9,'Aislamiento_social':6,'Conductas_evitativas':7
    },
    'Trastorno bipolar I': {
        'Ansiedad':6,'Estado_ánimo_bajo':7,'Anhedonia':5,'Problemas_de_sueño':6,'Fatiga':5,'Pensamientos_intrusivos':5,
        'Miedos_específicos':3,'Comportamiento_compulsivo':3,'Flashbacks':2,'Alucinaciones':3,'Delirios':3,'Autoestima_baja':5,
        'Irritabilidad':7,'Cambios_de_humor':9,'Dificultad_de_concentración':6,'Sentimientos_de_culpa':5,'Ideación_suicida':5,
        'Restricción_alimentaria':3,'Descontrol_alimentario':4,'Abuso_de_sustancias':6,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':4,'Aislamiento_social':5,'Conductas_evitativas':4
    },
    'Trastorno bipolar II': {
        'Ansiedad':6,'Estado_ánimo_bajo':8,'Anhedonia':7,'Problemas_de_sueño':5,'Fatiga':6,'Pensamientos_intrusivos':5,
        'Miedos_específicos':4,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':2,'Delirios':2,'Autoestima_baja':6,
        'Irritabilidad':6,'Cambios_de_humor':8,'Dificultad_de_concentración':6,'Sentimientos_de_culpa':6,'Ideación_suicida':6,
        'Restricción_alimentaria':3,'Descontrol_alimentario':3,'Abuso_de_sustancias':4,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':4,'Aislamiento_social':6,'Conductas_evitativas':5
    },
    'Trastorno ciclotímico': {
        'Ansiedad':5,'Estado_ánimo_bajo':5,'Anhedonia':4,'Problemas_de_sueño':4,'Fatiga':4,'Pensamientos_intrusivos':4,
        'Miedos_específicos':3,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':5,
        'Irritabilidad':5,'Cambios_de_humor':7,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':4,'Ideación_suicida':3,
        'Restricción_alimentaria':2,'Descontrol_alimentario':2,'Abuso_de_sustancias':3,'Despersonalización':2,'Desrealización':2,
        'Hipervigilancia':3,'Aislamiento_social':4,'Conductas_evitativas':4
    },
    'Esquizofrenia': {
        'Ansiedad':4,'Estado_ánimo_bajo':6,'Anhedonia':5,'Problemas_de_sueño':5,'Fatiga':5,'Pensamientos_intrusivos':5,
        'Miedos_específicos':3,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':9,'Delirios':9,'Autoestima_baja':5,
        'Irritabilidad':5,'Cambios_de_humor':5,'Dificultad_de_concentración':6,'Sentimientos_de_culpa':4,'Ideación_suicida':4,
        'Restricción_alimentaria':2,'Descontrol_alimentario':2,'Abuso_de_sustancias':4,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':4,'Aislamiento_social':7,'Conductas_evitativas':5
    },
    'Trastorno esquizoafectivo': {
        'Ansiedad':5,'Estado_ánimo_bajo':7,'Anhedonia':6,'Problemas_de_sueño':5,'Fatiga':5,'Pensamientos_intrusivos':5,
        'Miedos_específicos':4,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':7,'Delirios':7,'Autoestima_baja':6,
        'Irritabilidad':6,'Cambios_de_humor':7,'Dificultad_de_concentración':6,'Sentimientos_de_culpa':5,'Ideación_suicida':5,
        'Restricción_alimentaria':2,'Descontrol_alimentario':3,'Abuso_de_sustancias':4,'Despersonalización':4,'Desrealización':4,
        'Hipervigilancia':4,'Aislamiento_social':6,'Conductas_evitativas':5
    },
    'Anorexia nerviosa': {
        'Ansiedad':7,'Estado_ánimo_bajo':8,'Anhedonia':7,'Problemas_de_sueño':5,'Fatiga':8,'Pensamientos_intrusivos':5,
        'Miedos_específicos':6,'Comportamiento_compulsivo':5,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':9,
        'Irritabilidad':5,'Cambios_de_humor':5,'Dificultad_de_concentración':6,'Sentimientos_de_culpa':7,'Ideación_suicida':6,
        'Restricción_alimentaria':9,'Descontrol_alimentario':2,'Abuso_de_sustancias':3,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':5,'Aislamiento_social':7,'Conductas_evitativas':8
    },
    'Bulimia nerviosa': {
        'Ansiedad':6,'Estado_ánimo_bajo':7,'Anhedonia':6,'Problemas_de_sueño':5,'Fatiga':5,'Pensamientos_intrusivos':5,
        'Miedos_específicos':4,'Comportamiento_compulsivo':4,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':8,
        'Irritabilidad':5,'Cambios_de_humor':5,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':8,'Ideación_suicida':5,
        'Restricción_alimentaria':3,'Descontrol_alimentario':9,'Abuso_de_sustancias':4,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':4,'Aislamiento_social':6,'Conductas_evitativas':5
    },
    'Trastorno por atracón': {
        'Ansiedad':5,'Estado_ánimo_bajo':6,'Anhedonia':5,'Problemas_de_sueño':4,'Fatiga':5,'Pensamientos_intrusivos':4,
        'Miedos_específicos':3,'Comportamiento_compulsivo':3,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':6,
        'Irritabilidad':4,'Cambios_de_humor':5,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':7,'Ideación_suicida':3,
        'Restricción_alimentaria':2,'Descontrol_alimentario':8,'Abuso_de_sustancias':3,'Despersonalización':2,'Desrealización':2,
        'Hipervigilancia':3,'Aislamiento_social':5,'Conductas_evitativas':4
    },
    'Trastorno límite de la personalidad': {
        'Ansiedad':7,'Estado_ánimo_bajo':7,'Anhedonia':6,'Problemas_de_sueño':6,'Fatiga':5,'Pensamientos_intrusivos':6,
        'Miedos_específicos':4,'Comportamiento_compulsivo':4,'Flashbacks':3,'Alucinaciones':2,'Delirios':2,'Autoestima_baja':7,
        'Irritabilidad':8,'Cambios_de_humor':9,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':6,'Ideación_suicida':7,
        'Restricción_alimentaria':3,'Descontrol_alimentario':4,'Abuso_de_sustancias':5,'Despersonalización':4,'Desrealización':4,
        'Hipervigilancia':5,'Aislamiento_social':6,'Conductas_evitativas':5
    },
    'Trastorno antisocial de la personalidad': {
        'Ansiedad':3,'Estado_ánimo_bajo':3,'Anhedonia':4,'Problemas_de_sueño':3,'Fatiga':3,'Pensamientos_intrusivos':3,
        'Miedos_específicos':2,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':2,
        'Irritabilidad':8,'Cambios_de_humor':5,'Dificultad_de_concentración':4,'Sentimientos_de_culpa':1,'Ideación_suicida':2,
        'Restricción_alimentaria':1,'Descontrol_alimentario':3,'Abuso_de_sustancias':7,'Despersonalización':2,'Desrealización':2,
        'Hipervigilancia':4,'Aislamiento_social':3,'Conductas_evitativas':2
    },
    'Trastorno narcisista de la personalidad': {
        'Ansiedad':4,'Estado_ánimo_bajo':3,'Anhedonia':3,'Problemas_de_sueño':3,'Fatiga':3,'Pensamientos_intrusivos':3,
        'Miedos_específicos':2,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':2,'Autoestima_baja':2,
        'Irritabilidad':6,'Cambios_de_humor':5,'Dificultad_de_concentración':4,'Sentimientos_de_culpa':2,'Ideación_suicida':2,
        'Restricción_alimentaria':2,'Descontrol_alimentario':2,'Abuso_de_sustancias':4,'Despersonalización':2,'Desrealización':2,
        'Hipervigilancia':3,'Aislamiento_social':3,'Conductas_evitativas':3
    },
    'Trastorno evitativo de la personalidad': {
        'Ansiedad':8,'Estado_ánimo_bajo':6,'Anhedonia':5,'Problemas_de_sueño':5,'Fatiga':5,'Pensamientos_intrusivos':6,
        'Miedos_específicos':7,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':7,
        'Irritabilidad':4,'Cambios_de_humor':5,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':5,'Ideación_suicida':4,
        'Restricción_alimentaria':2,'Descontrol_alimentario':3,'Abuso_de_sustancias':3,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':5,'Aislamiento_social':8,'Conductas_evitativas':9
    },
    'Trastorno dependiente de la personalidad': {
        'Ansiedad':7,'Estado_ánimo_bajo':5,'Anhedonia':4,'Problemas_de_sueño':4,'Fatiga':4,'Pensamientos_intrusivos':5,
        'Miedos_específicos':5,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':6,
        'Irritabilidad':3,'Cambios_de_humor':4,'Dificultad_de_concentración':4,'Sentimientos_de_culpa':5,'Ideación_suicida':3,
        'Restricción_alimentaria':2,'Descontrol_alimentario':2,'Abuso_de_sustancias':3,'Despersonalización':2,'Desrealización':2,
        'Hipervigilancia':4,'Aislamiento_social':4,'Conductas_evitativas':7
    },
    'TDAH': {
        'Ansiedad':5,'Estado_ánimo_bajo':4,'Anhedonia':3,'Problemas_de_sueño':4,'Fatiga':4,'Pensamientos_intrusivos':4,
        'Miedos_específicos':3,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':4,
        'Irritabilidad':5,'Cambios_de_humor':5,'Dificultad_de_concentración':9,'Sentimientos_de_culpa':3,'Ideación_suicida':2,
        'Restricción_alimentaria':2,'Descontrol_alimentario':3,'Abuso_de_sustancias':4,'Despersonalización':2,'Desrealización':2,
        'Hipervigilancia':4,'Aislamiento_social':3,'Conductas_evitativas':4
    },
    'Trastorno del espectro autista': {
        'Ansiedad':6,'Estado_ánimo_bajo':4,'Anhedonia':4,'Problemas_de_sueño':4,'Fatiga':4,'Pensamientos_intrusivos':4,
        'Miedos_específicos':5,'Comportamiento_compulsivo':5,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':4,
        'Irritabilidad':5,'Cambios_de_humor':4,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':3,'Ideación_suicida':3,
        'Restricción_alimentaria':3,'Descontrol_alimentario':2,'Abuso_de_sustancias':2,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':5,'Aislamiento_social':6,'Conductas_evitativas':6
    },
    'Distimia (Trastorno depresivo persistente)': {
        'Ansiedad':5,'Estado_ánimo_bajo':8,'Anhedonia':7,'Problemas_de_sueño':5,'Fatiga':5,'Pensamientos_intrusivos':5,
        'Miedos_específicos':3,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':7,
        'Irritabilidad':5,'Cambios_de_humor':5,'Dificultad_de_concentración':6,'Sentimientos_de_culpa':6,'Ideación_suicida':5,
        'Restricción_alimentaria':3,'Descontrol_alimentario':3,'Abuso_de_sustancias':4,'Despersonalización':2,'Desrealización':2,
        'Hipervigilancia':3,'Aislamiento_social':6,'Conductas_evitativas':5
    },
    'Trastorno por consumo de alcohol': {
        'Ansiedad':5,'Estado_ánimo_bajo':6,'Anhedonia':5,'Problemas_de_sueño':7,'Fatiga':7,'Pensamientos_intrusivos':4,
        'Miedos_específicos':3,'Comportamiento_compulsivo':3,'Flashbacks':2,'Alucinaciones':2,'Delirios':2,'Autoestima_baja':5,
        'Irritabilidad':6,'Cambios_de_humor':5,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':7,'Ideación_suicida':4,
        'Restricción_alimentaria':2,'Descontrol_alimentario':3,'Abuso_de_sustancias':9,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':3,'Aislamiento_social':5,'Conductas_evitativas':4
    },
    'Trastorno por consumo de opioides': {
        'Ansiedad':5,'Estado_ánimo_bajo':7,'Anhedonia':6,'Problemas_de_sueño':7,'Fatiga':8,'Pensamientos_intrusivos':5,
        'Miedos_específicos':3,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':2,'Delirios':2,'Autoestima_baja':6,
        'Irritabilidad':5,'Cambios_de_humor':5,'Dificultad_de_concentración':4,'Sentimientos_de_culpa':7,'Ideación_suicida':5,
        'Restricción_alimentaria':2,'Descontrol_alimentario':4,'Abuso_de_sustancias':9,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':3,'Aislamiento_social':5,'Conductas_evitativas':4
    },
    'Trastorno por consumo de estimulantes': {
        'Ansiedad':7,'Estado_ánimo_bajo':5,'Anhedonia':4,'Problemas_de_sueño':8,'Fatiga':4,'Pensamientos_intrusivos':5,
        'Miedos_específicos':3,'Comportamiento_compulsivo':3,'Flashbacks':2,'Alucinaciones':3,'Delirios':3,'Autoestima_baja':4,
        'Irritabilidad':7,'Cambios_de_humor':6,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':5,'Ideación_suicida':4,
        'Restricción_alimentaria':2,'Descontrol_alimentario':4,'Abuso_de_sustancias':9,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':4,'Aislamiento_social':4,'Conductas_evitativas':4
    },
    'Trastorno de síntomas somáticos': {
        'Ansiedad':7,'Estado_ánimo_bajo':6,'Anhedonia':5,'Problemas_de_sueño':5,'Fatiga':6,'Pensamientos_intrusivos':5,
        'Miedos_específicos':4,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':6,
        'Irritabilidad':4,'Cambios_de_humor':5,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':6,'Ideación_suicida':4,
        'Restricción_alimentaria':3,'Descontrol_alimentario':3,'Abuso_de_sustancias':3,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':5,'Aislamiento_social':5,'Conductas_evitativas':5
    },
    'Trastorno de ansiedad por enfermedad': {
        'Ansiedad':9,'Estado_ánimo_bajo':5,'Anhedonia':4,'Problemas_de_sueño':6,'Fatiga':5,'Pensamientos_intrusivos':7,
        'Miedos_específicos':8,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':1,'Delirios':1,'Autoestima_baja':5,
        'Irritabilidad':5,'Cambios_de_humor':4,'Dificultad_de_concentración':6,'Sentimientos_de_culpa':5,'Ideación_suicida':3,
        'Restricción_alimentaria':2,'Descontrol_alimentario':2,'Abuso_de_sustancias':3,'Despersonalización':3,'Desrealización':3,
        'Hipervigilancia':7,'Aislamiento_social':4,'Conductas_evitativas':8
    },
    'Trastorno de despersonalización/desrealización': {
        'Ansiedad':6,'Estado_ánimo_bajo':5,'Anhedonia':5,'Problemas_de_sueño':5,'Fatiga':5,'Pensamientos_intrusivos':5,
        'Miedos_específicos':4,'Comportamiento_compulsivo':2,'Flashbacks':2,'Alucinaciones':2,'Delirios':2,'Autoestima_baja':5,
        'Irritabilidad':4,'Cambios_de_humor':4,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':4,'Ideación_suicida':3,
        'Restricción_alimentaria':2,'Descontrol_alimentario':2,'Abuso_de_sustancias':3,'Despersonalización':9,'Desrealización':9,
        'Hipervigilancia':5,'Aislamiento_social':5,'Conductas_evitativas':5
    },
    'Trastorno de identidad disociativo': {
        'Ansiedad':7,'Estado_ánimo_bajo':5,'Anhedonia':5,'Problemas_de_sueño':6,'Fatiga':5,'Pensamientos_intrusivos':6,
        'Miedos_específicos':4,'Comportamiento_compulsivo':2,'Flashbacks':4,'Alucinaciones':3,'Delirios':3,'Autoestima_baja':6,
        'Irritabilidad':5,'Cambios_de_humor':6,'Dificultad_de_concentración':5,'Sentimientos_de_culpa':5,'Ideación_suicida':4,
        'Restricción_alimentaria':2,'Descontrol_alimentario':3,'Abuso_de_sustancias':3,'Despersonalización':7,'Desrealización':7,
        'Hipervigilancia':5,'Aislamiento_social':5,'Conductas_evitativas':5
    },
}

df = pd.DataFrame.from_dict(data, orient='index', columns=sintomas)
df.to_csv('trastornos_sintomas_estimados.csv', encoding='utf-8-sig')

