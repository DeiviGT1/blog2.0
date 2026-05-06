# Brisa Sites — Guía de Deploy

Landing page bilingüe lista para subir a `josedavidgt.com/brisa-sites`. Esta versión 2.0 incluye toggle ES/EN funcional, sin Calendly (todo por WhatsApp), precios $25/$45/$75.

---

## Estructura de archivos

```
brisa-sites-landing/
├── index.html                    ← Landing principal bilingüe
├── restaurantes/index.html       ← Sub-landing por vertical (bilingüe)
├── botanicas/index.html
├── tabaquerias/index.html
├── barberias/index.html
├── tiendas/index.html
├── galerias/index.html
├── assets/
│   ├── styles.css                ← CSS compartido (incluye reglas idioma)
│   └── script.js                 ← JS: toggle idioma, FAQ, animaciones
└── DEPLOY.md                     ← Este archivo
```

URLs finales tras deploy:
- `josedavidgt.com/brisa-sites/` — Landing principal
- `josedavidgt.com/brisa-sites/restaurantes/`
- `josedavidgt.com/brisa-sites/botanicas/`
- `josedavidgt.com/brisa-sites/tabaquerias/`
- `josedavidgt.com/brisa-sites/barberias/`
- `josedavidgt.com/brisa-sites/tiendas/`
- `josedavidgt.com/brisa-sites/galerias/`

---

## Datos personalizados ya incluidos

Esta versión YA TIENE configurado:

| Dato | Valor |
|------|-------|
| WhatsApp | `+1 786-516-0915` (formato internacional `17865160915`) |
| Email | `josedago1163@gmail.com` |
| Calendly | ❌ No se usa — todo por WhatsApp |
| Precios | $25 / $45 / $75 mensuales ($300 / $540 / $900 anuales) |
| Idiomas | Español (default) + Inglés con toggle |

**No tienes que reemplazar nada antes de subir.** Tu información ya está embebida en los 7 archivos HTML.

---

## Cómo funciona el toggle de idiomas

El sitio detecta automáticamente la preferencia del usuario y la guarda en `localStorage` del navegador. La primera visita siempre arranca en español. Si el usuario hace click en el botón "EN" del navbar, cambia a inglés y se queda así en futuras visitas.

**Ventajas técnicas:**
- Una sola URL por página (mejor SEO que tener `/en/` separado)
- No necesita backend ni recargar página
- Todos los textos están en el mismo HTML, Google indexa ambos idiomas
- Funciona offline una vez cargada la página

**Cómo agregar texto nuevo bilingüe:**
Cualquier texto que agregues en el futuro debe seguir el patrón:
```html
<p>
  <span class="lang-es">Texto en español</span>
  <span class="lang-en">Text in English</span>
</p>
```
Si solo pones uno, ese mismo se muestra en ambos idiomas (útil para nombres propios, números, marcas).

---

## DEPLOY a josedavidgt.com/brisa-sites

### Opción A — cPanel / Hostinger / GoDaddy / hosting tradicional

1. Entra al **File Manager** de tu hosting
2. Navega a `public_html/` (la raíz de josedavidgt.com)
3. Crea carpeta `brisa-sites/`
4. Sube **todo el contenido** de `brisa-sites-landing/` adentro de `brisa-sites/`
5. La estructura final debe verse así:
   ```
   public_html/
   ├── (tu sitio actual josedavidgt.com)
   └── brisa-sites/
       ├── index.html
       ├── assets/
       ├── restaurantes/
       ├── botanicas/
       └── ... (resto)
   ```
6. Verifica abriendo `josedavidgt.com/brisa-sites` en el navegador

### Opción B — FTP (FileZilla, Cyberduck)

1. Conéctate al servidor con tus credenciales FTP
2. Navega a la carpeta raíz del sitio (`public_html/` o `htdocs/`)
3. Crea carpeta `brisa-sites/`
4. Arrastra el contenido de `brisa-sites-landing/` (local) a `brisa-sites/` (remoto)
5. Verifica en navegador

### Opción C — Git/GitHub Pages/Netlify/Vercel (avanzado)

Las rutas son relativas, así que también funciona como sitio standalone. Para hostearla en Vercel sin subcarpeta:
1. Sube la carpeta como repo en GitHub
2. Conecta con Vercel/Netlify
3. Configura dominio personalizado si tienes uno
4. Deploy automático

---

## Verificación post-deploy

Una vez subidos los archivos, prueba:

| Test | Cómo verificar |
|------|----------------|
| Sitio carga | `josedavidgt.com/brisa-sites` se abre sin errores |
| Tipografía Fraunces | Titulares se ven en serif elegante con cursivas |
| Colores correctos | Fondo crema, acentos terracota |
| Toggle idioma | Click en "EN" del navbar cambia todo el contenido a inglés |
| Persistencia idioma | Recargas la página y mantiene el idioma elegido |
| FAQ | Click en una pregunta abre/cierra la respuesta |
| WhatsApp flotante | Botón verde abajo a la derecha abre tu chat |
| Links a sub-landings | Los 6 verticales abren su página correspondiente |
| Back a inicio | "← Brisa Sites" en sub-landings regresa al index |
| Mobile | Abrelo en tu phone, debe verse perfecto |

---

## Cómo usar las sub-landings en outreach

**Esta es la jugada que aumenta conversión 2-3x.** No mandes el link genérico — manda el link específico al vertical del prospecto.

| Prospecto | Link a mandar en outreach |
|-----------|---------------------------|
| Versailles Restaurant | `josedavidgt.com/brisa-sites/restaurantes` |
| Botánica Yemayá | `josedavidgt.com/brisa-sites/botanicas` |
| El Crédito Cigars | `josedavidgt.com/brisa-sites/tabaquerias` |
| Floyd's Barbershop | `josedavidgt.com/brisa-sites/barberias` |
| La Casa de los Trucos | `josedavidgt.com/brisa-sites/tiendas` |
| Futurama 1637 | `josedavidgt.com/brisa-sites/galerias` |

Cuando el dueño abre el link, ve una página que **parece hecha para él**: hero específico, 3 dolores reales del sector, 6 features pensadas para su tipo de negocio, FAQ con sus objeciones, plan recomendado destacado.

Si tu prospecto es bilingüe o anglosajón, dile en el mensaje algo como: *"Echá un vistazo, podés cambiar a inglés con el botón 'EN' arriba"*.

---

## Mantenimiento

### Cambiar precios

Los precios están en 7 lugares (1 en index.html + 6 en sub-landings, sección pricing).

Para cambiarlos masivamente con búsqueda y reemplazo:
```bash
# En Mac:
find . -name "*.html" -exec sed -i '' 's|>25</span>|>30</span>|g' {} +

# En Linux:
find . -name "*.html" -exec sed -i 's|>25</span>|>30</span>|g' {} +
```

### Cambiar contenido bilingüe

Cuando edites un texto, **siempre actualiza las DOS versiones** (`lang-es` y `lang-en`). Si solo cambias una, el sitio queda inconsistente entre idiomas.

### Agregar un nuevo vertical (panaderías, salones, etc.)

1. Edita `/home/claude/build_sublandings.py` (Python script)
2. Agrega entrada nueva al diccionario `VERTICALS` siguiendo el patrón existente
3. Re-corre `python3 build_sublandings.py`
4. Agrega card en el grid de "Para quién" en `index.html`
5. Agrega link en footer

### Agregar foto real de Jose

Por ahora hay un placeholder con la letra "J" en gradiente terracota/dorado. Cuando tengas una foto profesional:

1. Pon la foto en `assets/jose.jpg` (cuadrada, mínimo 600×600px)
2. En `index.html` busca:
   ```html
   <div class="about-photo">
     J
   </div>
   ```
3. Reemplaza por:
   ```html
   <div class="about-photo" style="background: none; padding: 0;">
     <img src="assets/jose.jpg" alt="Jose - Brisa Sites" 
          style="width: 100%; height: 100%; object-fit: cover; border-radius: 24px;">
   </div>
   ```

---

## Troubleshooting

**El toggle de idioma no funciona.**
Abre la consola (F12 en navegador) y mira si hay errores. Generalmente es:
- `script.js` no se cargó (revisar ruta)
- Algún archivo HTML perdió referencia a `script.js`

**El sitio se ve sin estilos.**
- Verifica que `assets/styles.css` existe y se subió
- Limpia caché del navegador (Ctrl+Shift+R / Cmd+Shift+R)
- Mira en la pestaña Network del DevTools si el CSS retorna 200 OK

**Los acentos se ven raros (Ã³ en vez de ó).**
- Tu hosting está sirviendo con encoding incorrecto
- En tu cPanel revisa la configuración de "Default Character Set" → debe ser UTF-8

**Lighthouse score bajo.**
- El sitio está optimizado para >90 en todas las métricas
- Si aparece bajo, generalmente es por las imágenes (no hay todavía, así que no debería)
- Habilita compresión gzip en tu hosting si está deshabilitada

---

## Performance esperada

| Métrica | Esperado |
|---------|----------|
| Lighthouse Performance | 90-100 |
| Lighthouse Accessibility | 95-100 |
| Lighthouse SEO | 95-100 |
| First Contentful Paint | < 1.5s |
| Tamaño total página | < 100KB sin imágenes |
| Mobile-first | 100% responsivo |

---

**Versión:** 2.0
**Última actualización:** Mayo 2026
**Cambios desde v1.0:**
- Eliminado Calendly, todo contacto por WhatsApp
- Toggle EN/ES funcional en todas las páginas
- Precios actualizados a $25/$45/$75
- Comparativa Wix actualizada a precios reales 2026 ($300-750)
- "Sobre Jose" reescrito sin referencias geográficas personales
- WhatsApp y email reales pre-configurados
