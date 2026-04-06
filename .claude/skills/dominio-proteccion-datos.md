# Skill: Dominio Proteccion de Datos

## Cuando cargar
ACTIVAR cuando: analista-dominio trabaja en dominio "proteccion_datos"
NO ACTIVAR cuando: solo se busca legislacion (usar investigador-legal)

## Normativa principal

| Ley | Abreviatura | BOE |
|-----|-------------|-----|
| LO 3/2018, de Proteccion de Datos y Garantia de Derechos Digitales | LOPDGDD | BOE-A-2018-16673 |
| Reglamento (UE) 2016/679 General de Proteccion de Datos | RGPD | DOUE-L-2016-80807 |
| Ley 34/2002, de Servicios de la Sociedad de la Informacion (LSSI) | LSSI | BOE-A-2002-13758 |
| RD 1720/2007, Reglamento LOPD (vigente parcialmente) | RLOPD | BOE-A-2008-979 |
| Ley 25/2007, conservacion de datos comunicaciones electronicas | LCD | BOE-A-2007-18243 |

## Terminologia clave

- **Datos personales**: Toda informacion sobre una persona fisica identificada o identificable (art. 4.1 RGPD)
- **Tratamiento**: Cualquier operacion sobre datos personales: recogida, registro, organizacion, conservacion, consulta, difusion, supresion (art. 4.2 RGPD)
- **Responsable del tratamiento**: Quien determina los fines y medios del tratamiento (art. 4.7 RGPD)
- **Encargado del tratamiento**: Quien trata datos por cuenta del responsable (art. 4.8 RGPD, art. 28 RGPD, art. 33 LOPDGDD)
- **Delegado de Proteccion de Datos (DPD/DPO)**: Figura obligatoria en determinados supuestos que supervisa el cumplimiento (art. 37 RGPD, art. 34 LOPDGDD)
- **Base de legitimacion**: Fundamento juridico que habilita el tratamiento (art. 6 RGPD): consentimiento, contrato, obligacion legal, interes vital, interes publico, interes legitimo
- **Consentimiento**: Manifestacion de voluntad libre, especifica, informada e inequivoca (art. 4.11 RGPD)
- **Categorias especiales de datos**: Datos sensibles: origen etnico, opiniones politicas, convicciones religiosas, afiliacion sindical, datos geneticos, biometricos, salud, orientacion sexual (art. 9 RGPD)
- **Evaluacion de Impacto (EIPD)**: Analisis previo obligatorio cuando el tratamiento entrana alto riesgo (art. 35 RGPD)
- **Registro de actividades de tratamiento (RAT)**: Documentacion interna de todos los tratamientos (art. 30 RGPD)
- **Violacion de seguridad (brecha)**: Incidente que afecta la confidencialidad, integridad o disponibilidad de datos personales (art. 4.12 RGPD)

## Articulos mas consultados

### RGPD — Reglamento (UE) 2016/679
1. **art. 5**: Principios del tratamiento (licitud, lealtad, transparencia, limitacion de finalidad, minimizacion, exactitud, limitacion de conservacion, integridad y confidencialidad)
2. **art. 6**: Licitud del tratamiento (bases de legitimacion)
3. **art. 7**: Condiciones del consentimiento (carga de la prueba, retirada facil)
4. **art. 9**: Tratamiento de categorias especiales de datos (prohibicion general + excepciones)
5. **art. 12-14**: Informacion al interesado (transparencia, contenido del deber de informar)
6. **art. 15-22**: Derechos de los interesados (acceso, rectificacion, supresion, limitacion, portabilidad, oposicion, decisiones automatizadas)
7. **art. 25**: Proteccion de datos desde el diseno y por defecto
8. **art. 28**: Encargado del tratamiento (contrato obligatorio, contenido minimo)
9. **art. 30**: Registro de actividades de tratamiento
10. **art. 33-34**: Notificacion de brechas (72h a la autoridad, sin dilacion al interesado si alto riesgo)
11. **art. 35-36**: Evaluacion de impacto y consulta previa
12. **art. 37-39**: Delegado de proteccion de datos
13. **art. 83**: Condiciones para sanciones (hasta 20M EUR o 4% facturacion global)

### LOPDGDD — LO 3/2018 (BOE-A-2018-16673)
1. **art. 6-7**: Consentimiento de menores (14 anos en Espana)
2. **art. 8-10**: Tratamiento por obligacion legal, interes publico, interes legitimo
3. **art. 11**: Transparencia e informacion (modelo por capas)
4. **art. 12-18**: Derechos digitales en el ambito laboral
5. **art. 33**: Encargado del tratamiento (desarrollo del art. 28 RGPD)
6. **art. 34**: DPD obligatorio (lista de supuestos adicionales a los del RGPD)
7. **art. 73-74**: Infracciones (tipificacion detallada en derecho espanol)
8. **art. 89-97**: Derechos digitales (desconexion digital, videovigilancia laboral, geolocalizacion)

## Trampas comunes

### Consentimiento explicito vs implicito (art. 6-7 RGPD)
- **Error**: Asumir que el consentimiento siempre debe ser explicito
- **Realidad**: El consentimiento debe ser siempre inequivoco (accion afirmativa clara), pero solo se exige explicito para: categorias especiales de datos (art. 9.2.a RGPD), transferencias internacionales (art. 49.1.a RGPD), y decisiones automatizadas con efectos juridicos (art. 22.2.c RGPD). Para el resto, basta consentimiento inequivoco mediante accion afirmativa (marcar una casilla, aceptar un enlace), pero NUNCA mediante inaccion, casillas premarcadas o silencio (considerando 32 RGPD). Importante: si la base de legitimacion es el contrato, el interes legitimo o una obligacion legal, no se necesita consentimiento.

### Registro de actividades de tratamiento: obligatorio para casi todos (art. 30 RGPD)
- **Error**: Creer que solo las grandes empresas deben tener RAT
- **Realidad**: El art. 30.5 RGPD exime a empresas de menos de 250 empleados SOLO si el tratamiento no es habitual. En la practica, toda empresa que trate datos de empleados, clientes o proveedores de forma habitual (es decir, todas) debe mantener el RAT. La AEPD ha confirmado este criterio. El RAT debe contener: nombre y datos del responsable, finalidades, categorias de interesados y datos, destinatarios, transferencias internacionales, plazos de conservacion, y medidas de seguridad.

### DPO obligatorio: cuando y quien (art. 37 RGPD + art. 34 LOPDGDD)
- **Error**: Creer que el DPO solo es obligatorio para el sector publico
- **Realidad**: Es obligatorio para: (1) autoridades y organismos publicos (excepto tribunales), (2) tratamiento a gran escala de categorias especiales de datos, (3) observacion habitual y sistematica a gran escala. Ademas, el art. 34 LOPDGDD anade supuestos obligatorios en Espana: centros docentes, prestadores de servicios de comunicaciones electronicas, entidades financieras, aseguradoras, distribuidores de energia, operadores de juego, empresas de seguridad privada, y federaciones deportivas. El DPO puede ser interno o externo, persona fisica o juridica, y debe tener independencia funcional.

### Informacion por capas (art. 11 LOPDGDD)
- **Error**: Dar toda la informacion de proteccion de datos en un unico bloque
- **Realidad**: La LOPDGDD permite el modelo de informacion por capas (art. 11): primera capa basica (identidad responsable, finalidad, derechos, enlace a segunda capa) y segunda capa completa (toda la informacion del art. 13-14 RGPD). La primera capa puede ser verbal, en cartel, o en enlace visible. Es especialmente util para formularios, videovigilancia y recogida telefonica.

### Brechas de seguridad: plazos y obligaciones (arts. 33-34 RGPD)
- **Error**: Notificar siempre a los interesados
- **Realidad**: La notificacion a la AEPD (72 horas) es obligatoria siempre que haya riesgo para derechos y libertades. La comunicacion a los interesados solo es obligatoria cuando el riesgo es ALTO. Si se han aplicado medidas que hagan ininteligibles los datos (cifrado), puede no ser necesaria la comunicacion al interesado aunque haya brecha. Se debe documentar TODA brecha internamente, se notifique o no.

### Videovigilancia laboral (art. 89 LOPDGDD + jurisprudencia TEDH)
- **Error**: Instalar camaras en el trabajo sin informar a los trabajadores
- **Realidad**: Se debe informar previamente a los trabajadores de la instalacion de camaras (art. 89.1 LOPDGDD). Sin embargo, el art. 89.2 permite que la captacion de imagenes se use como prueba de incumplimiento laboral si se acredita que habia cartel informativo visible. La grabacion de audio junto con video requiere justificacion adicional. Prohibida la videovigilancia en vestuarios, aseos y zonas de descanso.

## Cross-references frecuentes

- RGPD art. 6 (bases de legitimacion) -> LOPDGDD arts. 8-10 desarrollan interes publico, obligacion legal e interes legitimo en el contexto espanol
- RGPD art. 28 (encargado) -> LOPDGDD art. 33 detalla el contenido del contrato de encargado y la subcontratacion
- RGPD art. 37 (DPO) -> LOPDGDD art. 34 amplia los supuestos obligatorios en Espana
- RGPD art. 83 (sanciones) -> LOPDGDD arts. 70-78 tipifican infracciones y graduan sanciones en derecho espanol
- LOPDGDD art. 89-97 (derechos digitales laborales) -> conectan con ET art. 20 bis (derechos digitales del trabajador)
- RGPD art. 9 (datos sensibles) -> para datos de salud laboral, conecta con LPRL art. 22 (vigilancia salud)
- LSSI art. 21 (comunicaciones comerciales) -> se complementa con RGPD art. 6 para determinar la base de legitimacion del marketing directo (consentimiento vs interes legitimo del considerando 47 RGPD)
- RGPD art. 35 (EIPD) -> la AEPD publica listas de tratamientos que requieren EIPD obligatoria (guia AEPD)
