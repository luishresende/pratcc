import json
import datetime

from django.shortcuts import render
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse, JsonResponse
from tccs.models import TccWork, Teacher, TccDocuments, TccCommittee
from django.utils.timezone import localdate


# Create your views here.
def index(request):
    name = request.session.get('name', 'Usuário')

    response = tccs_status_geral(request)  # retorna JsonResponse
    data = json.loads(response.content)    # transforma o conteúdo JSON em dict

    context = {
        'name': name,
        **data,  # passa os dados do JSON pro template
    }

    return render(request, 'dashboard/index.html', context)

def report(request):
    year = request.GET.get('year')
    semester = request.GET.get('semester')

    if not year or not semester:
        return JsonResponse({'success': False, 'message': 'É necessário informar o ano e o semestre.'}, status=400)

    tccs = TccWork.objects.filter(year=year, semester=semester).select_related('student_ra', 'teacher_advisor_ma', 'teacher_cosupervisor_ma')

    if tccs.count() == 0:
        return JsonResponse({'success': False, 'message': 'Nenhum TCC encontrado para o perído especificado.'}, status=400)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_tccs_{year}_{semester}.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    styles = getSampleStyleSheet()
    style_title = styles['Heading1']
    style_title.fontName = 'Helvetica-Bold'
    style_title.fontSize = 18
    style_title.alignment = 1  # center

    style_subtitle = styles['Heading2']
    style_subtitle.fontName = 'Helvetica-Bold'
    style_subtitle.fontSize = 14
    style_subtitle.alignment = 0  # right

    style_text = styles['Normal']
    style_text.fontName = 'Helvetica'
    style_text.fontSize = 12

    def draw_title():
        title_text = f"Trabalhos de Conclusão de Curso {year}/{semester}"
        p = Paragraph(title_text, style_title)
        w, h = p.wrap(width - 4 * cm, height)
        p.drawOn(c, 2 * cm, height - 2 * cm - h)
        return h

    y = height - 3 * cm  # posição inicial abaixo do título

    title_height = draw_title()
    y -= (title_height + 1*cm)  # ajusta espaço depois do título

    for tcc in tccs:
        # Título do TCC
        p_title = Paragraph(f"Título: {tcc.title}", style_subtitle)
        w, h = p_title.wrap(width - 4 * cm, y)
        if y - h < 2 * cm:  # Verifica espaço para nova página
            c.showPage()
            title_height = draw_title()
            y = height - 2 * cm - title_height - 1*cm

        p_title.drawOn(c, 2 * cm, y - h)
        y -= (h + 0.3 * cm)

        # Fase
        p_phase = Paragraph(f"Fase: {tcc.tcc_num}", style_text)
        w, h = p_phase.wrap(width - 4 * cm, y)
        p_phase.drawOn(c, 2 * cm, y - h)
        y -= (h + 0.2 * cm)

        # Aluno
        p_student = Paragraph(f"Aluno: {tcc.student_ra.name}", style_text)
        w, h = p_student.wrap(width - 4 * cm, y)
        p_student.drawOn(c, 2 * cm, y - h)
        y -= (h + 0.2 * cm)

        # Orientador
        p_advisor = Paragraph(f"Orientador: {tcc.teacher_advisor_ma.name}", style_text)
        w, h = p_advisor.wrap(width - 4 * cm, y)
        p_advisor.drawOn(c, 2 * cm, y - h)
        y -= (h + 0.2 * cm)

        # Coorientador (se existir)
        if tcc.teacher_cosupervisor_ma:
            p_cosupervisor = Paragraph(f"Coorientador: {tcc.teacher_cosupervisor_ma.name}", style_text)
            w, h = p_cosupervisor.wrap(width - 4 * cm, y)
            p_cosupervisor.drawOn(c, 2 * cm, y - h)
            y -= (h + 0.2 * cm)

        # Espaço entre TCCs
        y -= 0.8 * cm

        # Se ficar muito perto do rodapé, nova página
        if y < 2 * cm:
            c.showPage()
            title_height = draw_title()
            y = height - 2 * cm - title_height - 1*cm

    c.save()
    return response


def tccs_status_geral(request):
    today = localdate()

    # 1. TCCs que ainda não têm um TccCommittee
    tccs_sem_committee = TccWork.objects.filter(tcccommittee__isnull=True)

    lista_pendentes = [
        {
            'id': tcc.tcc_id,
            'titulo': tcc.title,
            'dias_restantes': None
        }
        for tcc in tccs_sem_committee
    ]

    # 2. TCCs com committee, mas sem carta de autorização
    committees_pendentes = TccCommittee.objects.filter(
        authorization_letter_submitted=False,
        defense_date__gte=today
    ).select_related('tccw')

    for committee in committees_pendentes:
        today = datetime.date.today()
        dias_restantes = (committee.defense_date.date() - today).days if committee.defense_date else None

        lista_pendentes.append({
            'id': committee.tccw.tcc_id,
            'titulo': committee.tccw.title,
            'dias_restantes': dias_restantes,
        })

    # Total de TCCs
    total_tccs = TccWork.objects.count()

    # Período mais recente
    if total_tccs:
        ultimo_periodo = TccWork.objects.order_by('-year', '-semester').values('year', 'semester').first()
        tccs_periodo_recente = TccWork.objects.filter(
            year=ultimo_periodo['year'],
            semester=ultimo_periodo['semester']
        ).count()
    else:
        tccs_periodo_recente = 0

    # Monografias não entregues
    monografias_pendentes = TccDocuments.objects.filter(end_monograph=False).count()

    # Termos de autorização pendentes (apenas com committee criado)
    termos_pendentes = TccCommittee.objects.filter(authorization_letter_submitted=False).count()

    return JsonResponse({
        'pendentes_carta_autorizacao': lista_pendentes,
        'total_tccs': total_tccs,
        'tccs_periodo_mais_recente': tccs_periodo_recente,
        'monografias_nao_entregues': monografias_pendentes,
        'termos_autorizacao_pendentes': termos_pendentes,
    })

