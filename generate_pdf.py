import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable
)

BRAIN_DIR = r"C:\Users\MAAIC\.gemini\antigravity-ide\brain\5016e227-5393-472f-9f96-7dc8f4b7e708"
PROJECT_DIR = r"c:\Users\MAAIC\OneDrive\Documentos\django"
PDF_PATH = os.path.join(PROJECT_DIR, "Reporte_Practica_Django_DRF_JWT_Usuarios.pdf")

def create_report():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1e293b'),
        alignment=1, # Center
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0f172a'),
        backColor=colors.HexColor('#f1f5f9'),
        borderPadding=6,
        spaceAfter=6
    )

    link_style = ParagraphStyle(
        'RepoLink',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2563eb'),
        alignment=1,
        spaceAfter=15
    )

    story = []

    # Header / Title Banner
    story.append(Paragraph("REPORTE DE PRÁCTICA: DJANGO, DRF, JWT Y USUARIOS", title_style))
    story.append(Paragraph("Adaptación, Corrección de Seguridad y Documentación con Swagger UI", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0f766e'), spaceAfter=10))

    # Meta Info Table
    repo_url = "https://github.com/Mikyzxx/djiango"
    meta_data = [
        [Paragraph("<b>Repositorio GitHub:</b>", body_style), Paragraph(f'<a href="{repo_url}"><font color="#2563eb">{repo_url}</font></a>', body_style)],
        [Paragraph("<b>Proyecto Base:</b>", body_style), Paragraph("<b>tienda_online</b> (Plataforma E-Commerce con Catálogo y Usuarios)", body_style)],
        [Paragraph("<b>Campo Extra en Usuario:</b>", body_style), Paragraph("<b>telefono</b> (Visible en Admin, Serializer y Swagger)", body_style)],
        [Paragraph("<b>Tiempo de Vida del Token:</b>", body_style), Paragraph("<b>ACCESS_TOKEN_LIFETIME = 60 minutos</b> (1 hora)", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[160, 380])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1: Cambios y Adaptaciones
    story.append(Paragraph("1. Cambios y Adaptaciones Implementadas", h1_style))
    cambios_text = (
        "<b>1. Nombre de Proyecto y Swagger:</b> En cumplimiento con la indicación de no utilizar 'restaurante', "
        "se integró el módulo de usuarios dentro del proyecto <b>tienda_online</b>. El título configurado en "
        "Swagger es <b>'Tienda Online API'</b> con versión <code>v1</code> y esquema OpenAPI 2.0.<br/>"
        "<b>2. Campo Personalizado en el Modelo:</b> Se agregó el campo <code>telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')</code>. "
        "Se configuró el <code>UserAdmin</code> para mostrarlo tanto en el listado como en los formularios de edición y alta.<br/>"
        "<b>3. Expiración de Tokens JWT:</b> En <code>settings.py</code> se configuró SimpleJWT mediante "
        "<code>SIMPLE_JWT = {'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), ...}</code>."
    )
    story.append(Paragraph(cambios_text, body_style))
    story.append(Spacer(1, 6))

    # Section 2: Correcciones de Seguridad
    story.append(Paragraph("2. Identificación y Corrección de Fallas de Seguridad del Manual", h1_style))
    seguridad_text = (
        "<b>Falla 1: Fuga de Hash de Contraseña en Respuestas API</b><br/>"
        "<i>Problema:</i> En el manual (pág. 9), <code>UserSerializer</code> definía <code>fields = [..., 'password', ...]</code> "
        "sin marcarlo como de solo lectura. En consecuencia, todas las consultas a <code>/api/v1/users/</code>, <code>/api/v1/users/{id}/</code> "
        "y <code>/api/v1/auth/me/</code> exponían el hash de las contraseñas de los usuarios en formato JSON.<br/>"
        "<i>Solución:</i> Se configuró <code>extra_kwargs = {'password': {'write_only': True, 'required': False}}</code>, "
        "impidiendo que el serializador retorne contraseñas bajo ninguna circunstancia.<br/><br/>"
        "<b>Falla 2: Robo/Sobrescritura Accidental de Contraseña en Actualización Parcial</b><br/>"
        "<i>Problema:</i> En el manual (pág. 10), el método <code>partial_update</code> contenía:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>if 'password' in request.data: ... else: request.data['password'] = request.user.password</code><br/>"
        "Al actualizar un usuario sin enviar contraseña (por ejemplo, cambiar su teléfono o nombre), se le asignaba "
        "la contraseña de <code>request.user</code> (el administrador que hacía la petición). La víctima quedaba bloqueada "
        "y pasaba a tener la clave del administrador.<br/>"
        "<i>Solución:</i> Se eliminó la cláusula <code>else</code>. Si no se envía contraseña en la petición, "
        "la contraseña existente del usuario permanece inalterada."
    )
    story.append(Paragraph(seguridad_text, body_style))

    # Page break for Visual Evidences
    story.append(PageBreak())

    # Section 3: Evidencias Fotográficas
    story.append(Paragraph("3. Evidencias de Ejecución y Validación", h1_style))

    # Evidencia 1: Swagger
    story.append(Paragraph("Evidencia 1: Swagger UI con Endpoints de la Tienda Online API", h2_style))
    story.append(Paragraph("Se visualizan los endpoints agrupados de <code>auth</code>, <code>users</code>, <code>products</code> y <code>categories</code>, con el título y descripción personalizados.", body_style))
    img1_path = os.path.join(BRAIN_DIR, "evidencia_1_swagger_endpoints.png")
    if os.path.exists(img1_path):
        story.append(Image(img1_path, width=7*inch, height=3.5*inch))
    story.append(Spacer(1, 10))

    # Evidencia 2: Obtención de Token
    story.append(Paragraph("Evidencia 2: Obtención del Token JWT (POST /api/v1/auth/token/)", h2_style))
    story.append(Paragraph("Petición exitosa enviando <code>email</code> y <code>password</code> con respuesta 200 OK y entrega de <code>access</code> y <code>refresh</code> tokens.", body_style))
    img2_path = os.path.join(BRAIN_DIR, "evidencia_2_token_response.png")
    if os.path.exists(img2_path):
        story.append(Image(img2_path, width=7*inch, height=3.2*inch))

    story.append(PageBreak())

    # Evidencia 3: Auth Me
    story.append(Paragraph("Evidencia 3: Consulta de Datos Personales (GET /api/v1/auth/me/)", h2_style))
    story.append(Paragraph("Respuesta 200 OK con los datos del usuario autenticado. Se verifica que <b>incluye el campo extra 'telefono'</b> y que el <b>hash de la contraseña está ausente</b>.", body_style))
    img3_path = os.path.join(BRAIN_DIR, "evidencia_3_auth_me_response.png")
    if os.path.exists(img3_path):
        story.append(Image(img3_path, width=7*inch, height=3.3*inch))
    story.append(Spacer(1, 10))

    # Evidencia 4: Prueba de Seguridad Password
    story.append(Paragraph("Evidencia 4: Prueba de que Editar Usuario Sin Contraseña NO Cambia su Contraseña", h2_style))
    story.append(Paragraph("Validación en vivo del endpoint PATCH: el hash del usuario permanece intacto, no adquiere la clave del administrador, y el usuario continúa autenticándose con su clave original.", body_style))
    img4_path = os.path.join(BRAIN_DIR, "evidencia_4_seguridad_password.png")
    if os.path.exists(img4_path):
        story.append(Image(img4_path, width=7*inch, height=4.2*inch))

    story.append(PageBreak())

    # Evidencia 5: Django Admin
    story.append(Paragraph("Evidencia 5 (Adicional): Campo Extra 'Teléfono' en Django Admin", h2_style))
    story.append(Paragraph("Panel de administración de Django demostrando el registro del modelo <code>User</code> con el campo personalizado <code>telefono</code> en la sección de Información Personal.", body_style))
    img_admin_path = os.path.join(BRAIN_DIR, "evidencia_admin_user_telefono.png")
    if os.path.exists(img_admin_path):
        story.append(Image(img_admin_path, width=7*inch, height=3.5*inch))
    story.append(Spacer(1, 12))

    # Section 4: Conclusiones
    story.append(Paragraph("4. Resumen de Pruebas Automatizadas", h1_style))
    tests_summary = (
        "Se implementó una suite completa de pruebas unitarias automatizadas (<code>users/tests.py</code> y <code>products/tests.py</code>), "
        "totalizando <b>15 pruebas unitarias exitosas (Ran 15 tests, OK)</b>:<br/>"
        "• Verificación de <code>USERNAME_FIELD = 'email'</code> y campo extra <code>telefono</code>.<br/>"
        "• Verificación de configuración de <code>ACCESS_TOKEN_LIFETIME</code> (60 min).<br/>"
        "• Autenticación JWT y generación de tokens de acceso y refresco.<br/>"
        "• Protección estricta del hash de contraseña en <code>/api/v1/auth/me/</code> y CRUD de usuarios.<br/>"
        "• Inmutabilidad de contraseña durante peticiones PATCH/PUT sin campo de contraseña.<br/>"
        "• Cifrado seguro mediante <code>make_password</code> cuando se envía una nueva contraseña explícita."
    )
    story.append(Paragraph(tests_summary, body_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#94a3b8'), spaceAfter=8))
    story.append(Paragraph("<b>Enlace de Entrega GitHub:</b> <a href='https://github.com/Mikyzxx/djiango'><font color='#2563eb'>https://github.com/Mikyzxx/djiango</font></a>", link_style))

    doc.build(story)
    print(f"PDF generado exitosamente en: {PDF_PATH}")

if __name__ == "__main__":
    create_report()
