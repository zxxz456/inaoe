<!--
README.md
========================


Descripcion:
------------
Presentacion del Seminario de Metodologia sobre etica en la
investigacion cientifica, armada con el capitulo 10 de Pruzan, el
capitulo 13 de Dawson y el informe del comite de IA del MIT


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       26/11/2026      Creation


-->

# Ética en la investigación científica

Presentación en Quarto (reveal.js) para el Seminario de Metodología. Cruza tres fuentes, cada una con su escala:

- **Pruzan (2016)**, *Research Methodology: The Aims, Practices and Ethics of Science*, capítulo 10 "Ethics and Responsibility in Scientific Research" y las menciones de ética en los capítulos 4 a 7. Es la fuente principal: los principios, las guías de integridad y los casos.
- **Dawson (2002)**, *Practical Research Methods*, capítulo 13 "How to be an Ethical Researcher" y la sección de ética de la observación participante. Aporta el trato con los participantes.
- **Comité del MIT (2026)**, *Report of MIT's Ad Hoc Committee on AI Use in Teaching, Learning, and Research Training*. Aporta la ética de usar IA al investigar.

La plantilla es la de `esquizo/presentacion`: tema serif, fondo crema, títulos con subrayado teal, secciones numeradas y portada en teal oscuro. Cada color es una fuente en toda la presentación: teal Pruzan, magenta Dawson y ámbar el MIT. La fuente exacta de cada diapositiva, con sección y página, va al pie.

## Contenido

Son 25 diapositivas de contenido en seis secciones, más las referencias. La columna son los cinco temas que comparten las tres fuentes:

1. **La ética en la ciencia.** Por qué hablar de ética, las tres fuentes, qué entendemos por ética y las tres áreas donde Pruzan ubica la conducta sin base ética.
2. **Respeto y consentimiento.** El trato con quien participa, el consentimiento informado, el consentimiento aplicado a los datos (incluidos los de entrenamiento de la IA) y el dilema del doble ciego.
3. **Integridad.** Fabricación, falsificación y plagio; integridad de los datos; las prácticas dañinas que no llegan a fraude; autoría y conflicto de interés.
4. **Honestidad y transparencia.** Investigación abierta contra encubierta, el caso de Steve, engaño y coerción (Milgram y el trabajo de campo) y la declaración del uso de IA.
5. **Responsabilidad.** Investigación básica contra aplicada, benéfica contra dañina, y la tentación de la especialización.
6. **De evitar a promover.** La contraparte positiva de cada falta, normas en lugar de vigilancia, y por qué la ética se aprende.

Las notas del presentador son un guion corto en español; se abren con la tecla `s`.

Se omite lo que las fuentes traen desactualizado o equivocado: la ley británica de protección de datos de 1998 que cita Dawson, las cifras de Turnitin de 2013 que da Pruzan y la década que Pruzan le asigna a los experimentos de Milgram.

## Archivos

```
presentacion_etica/
├── README.md
├── EticaInvestigacion.qmd      presentacion en Quarto
└── EticaInvestigacion.html     presentacion compilada, autocontenida
```

## Cómo verla y regenerarla

```bash
cd seminario1/presentacion_etica
xdg-open EticaInvestigacion.html        # la version compilada
quarto render EticaInvestigacion.qmd    # vuelve a generar el html
quarto preview EticaInvestigacion.qmd   # en vivo
```

No hay figuras generadas ni imágenes: todo el contenido vive en el `.qmd`.

<!--
############################### END OF README.MD ###############################
################################################################################
-->
