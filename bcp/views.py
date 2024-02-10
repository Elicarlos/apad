from cupom.models import Cupom
from participante.models import DocumentoFiscal, Profile
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from participante.forms import DocumentoFiscalEditForm
from cryptography.fernet import Fernet
# from django.contrib.staticfiles.templatetags.staticfiles import static
from django.templatetags.static import static
try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO

# def regulamento(request):
#     return render(request, static('web/regulamento.pdf'))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def print_barcode_embed_example(request, id_, template='cupons_impressos.html'):
    """
    This is a test page showing how you can embed a request to print a barcode
    """
    doc = get_object_or_404(DocumentoFiscal, id=id_)
    if not doc.status and not request.user.is_staff:
        return render(request, 'lojista/dashboard.html')
    doc_form = DocumentoFiscalEditForm(instance=doc)
    new_doc = doc_form.save(commit=False)
    new_doc.key = Fernet.generate_key()
    new_doc.status = False
    new_doc.save()
    bcp_url = reverse('bcp:print_qrcode', kwargs = {'id_': id_,})
    context = { 'bcp_url': bcp_url, 'doc':doc, }
    return render(request, template, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def print_qrcode(request, id_, template='print.html'):
    """
    This page causes the browser to request the barcode be printed
    """
    doc = get_object_or_404(DocumentoFiscal, id=id_)
    doc_form = DocumentoFiscalEditForm(instance=doc)
    new_doc = doc_form.save(commit=False)
    new_doc.status = False
    new_doc.save()
    pdf_url = reverse('bcp:generate', kwargs = {'id_': id_, })
    context = { 'pdf_url': pdf_url, }
    return render(request, template, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def print_barcode(request, id_, template='print.html'):
    """
    This page causes the browser to request the barcode be printed
    """
    doc = get_object_or_404(DocumentoFiscal, id=id_)
    doc_form = DocumentoFiscalEditForm(instance=doc)
    new_doc = doc_form.save(commit=False)
    new_doc.status = False
    new_doc.save()
    doc = get_object_or_404(DocumentoFiscal, id=id_)
    pdf_url = reverse('bcp:generate', kwargs = {'id_': id_,})
    context = { 'pdf_url': pdf_url, 'doc':doc }
    return render(request, template, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def generate(request, id_,  barcode_type='Standard39', auto_print=True):
    """
     Returns a PDF Barcode using ReportLab
    """

    from reportlab.graphics.shapes import String, Drawing
    from reportlab.pdfgen import canvas
    from reportlab.graphics import renderPDF
    from reportlab.graphics.barcode import qr
    from reportlab.pdfbase import pdfdoc
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.utils import ImageReader
    from django.utils.dateformat import DateFormat
    from datetime import datetime


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s.pdf' % (id_,)

    # Config

    import bcp.settings as bcp_settings
    font_size = bcp_settings.FONT_SIZE
    bar_height = bcp_settings.BAR_HEIGHT
    bar_width = bcp_settings.BAR_WIDTH
    font_name = bcp_settings.FONT_NAME
    font_path = bcp_settings.FONT_PATH
    font_bold = bcp_settings.FONT_PATH_BOLD
    font_name_bold = bcp_settings.FONT_BOLD
    image_path = bcp_settings.IMAGE_PATH
    # image_pop = bcp_settings.IMAGE_POP
    image_rede = bcp_settings.IMAGE_REDE
    image_master = bcp_settings.IMAGE_MASTER
    image_cdl = bcp_settings.IMAGE_CDL
    #image_marko = bcp_settings.IMAGE_MARKO
    doc = get_object_or_404(DocumentoFiscal, id=id_)
    cupons = Cupom.objects.filter(documentoFiscal=doc)
    profile = get_object_or_404(Profile, user=doc.user)
    # If this is extended to different barcode types, then these options will need to be specified differently, eg not all formats support checksum.


    # Register the font
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    pdfmetrics.registerFont(TTFont(font_name_bold, font_bold))

    # Set JS to Autoprint document
    if auto_print:
        pdfdoc.PDFCatalog.OpenAction = '<</S/JavaScript/JS(this.print\({bUI:false,bSilent:true,bShrinkToFit:true}\);)>>'
        pdfdoc.PDFInfo.title = 'Liquida Teresina 2023' # nicety :)

    # lineUp = String(105, 212, "_______________________________________________________", textAnchor='middle', fontSize=font_size)
    # title = String(105, 196, "** LIQUIDA TERESINA 2018 **", textAnchor='middle', fontSize=12)
    # lineTop = String(105, 190, "_______________________________________", textAnchor='middle', fontName=font_name, fontSize=font_size)
    # lineTitle = String(105, 171, "_______________________________________", textAnchor='middle', fontName=font_name, fontSize=font_size)
    # dadosParticipante = String(105, 177, "Dados do Participante", textAnchor='middle', fontSize=font_size)
    # nome = String(30, 160, "Nome:", textAnchor='middle', fontSize=font_size)
    # nomeParticipante = String(70, 160, '{}'.format(doc.user), textAnchor='middle', fontSize=font_size)
    # cpf = String(27, 145, "CPF:", textAnchor='middle', fontSize=font_size)
    # cidade = String(31, 130, "Cidade:", textAnchor='middle', fontSize=font_size)
    # estado = String(150, 130, "Estado:", textAnchor='middle', fontSize=font_size)
    # bairro = String(30, 115, "Bairro:", textAnchor='middle', fontSize=font_size)
    # fone = String(147, 115, "Fone:", textAnchor='middle', fontSize=font_size)
    # loja = String(48, 100, "Comprou na loja?", textAnchor='middle', fontSize=font_size)
    # vendedor = String(155, 100, "Vendedor:", textAnchor='middle', fontSize=font_size)
    # data = String(147, 70, "Data:", textAnchor='middle', fontSize=font_size)
    # cupom = String(140, 50, "Cupom", textAnchor='middle', fontSize=15)
    # lineBottom = String(105, 8, "_____________________________________________________", textAnchor='middle',  fontSize=font_size)
    # c.add(lineUp)
    # c.add(title)
    # c.add(lineTop)
    # c.add(dadosParticipante)
    # c.add(lineTitle)
    # c.add(nome)
    # c.add(nomeParticipante)
    # c.add(cpf)
    # c.add(cidade)
    # c.add(estado)
    # c.add(bairro)
    # c.add(fone)
    # c.add(loja)
    # c.add(vendedor)
    # c.add(data)
    # c.add(cupom)

    # c.add(lineBottom)


    buffer = BytesIO() # buffer for the output

    c = canvas.Canvas(buffer)
    for cupom in cupons:
        cupom.dataImpressao = datetime.now()
        code = cupom.get_info()
        qr_code = qr.QrCodeWidget(code)
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        x = width
        y = height
        d = Drawing(100, 100, transform=[240./width, 0, 0, 240./height, 0, 0])
        d.add(qr_code)
        c.setFont(font_name, 30)
        c.drawImage(image_path, 200, 683, mask='auto') 
        c.drawImage(image_rede, 35, 750, mask='auto')
        # c.drawImage(image_pop, 450, 670, mask='auto')
        c.drawImage(image_master, 400, 730, mask='auto')
        c.drawImage(image_cdl, 70, 90, mask='auto')

        #c.drawImage(image_marko, 40, 50, mask='auto')
        c.setFont(font_name, 20)
        c.drawString(20, 660, '_______________________________________________________')
        # c.drawString(70, 810, "** Liquida Teresina 2023 **")

        c.setFont(font_name_bold, 23)
        c.drawString(150, 630, "Dados do Participante")
        c.setFont(font_name, 20)
        c.drawString(40, 550, "Nome:")
        c.setFont(font_name_bold, 20)
        c.drawString(115, 550, '{}'.format(profile.nome))
        c.setFont(font_name, 20)
        c.drawString(40, 580, "CPF:")
        c.setFont(font_name_bold, 20)
        c.drawString(95, 580, '{}'.format(profile.CPF))
        c.setFont(font_name, 20)
        c.drawString(40, 520, "Cidade:")
        c.setFont(font_name_bold, 20)
        c.drawString(115, 520, '{}'.format(profile.cidade))
        c.setFont(font_name, 20)
        c.drawString(330, 520, "Estado:")
        c.setFont(font_name_bold, 20)
        c.drawString(410, 520, '{}'.format(profile.estado))
        c.setFont(font_name, 20)
        c.drawString(40, 490, "Bairro:")
        c.setFont(font_name_bold, 20)
        c.drawString(115, 490, '{}'.format(profile.bairro))
        c.setFont(font_name, 20)
        c.drawString(330, 490, "Fone:")
        c.setFont(font_name_bold, 20)
        c.drawString(390, 490, '{}'.format(profile.foneCelular1))
        c.setFont(font_name, 20)
        c.drawString(40, 460 , "Comprou na loja?")
        c.setFont(font_name_bold, 20)
        c.drawString(40, 430, '{}'.format(cupom.documentoFiscal.lojista))
        c.setFont(font_name, 20)
        c.drawString(330, 460, "Vendedor:")
        c.setFont(font_name_bold, 20)
        c.drawString(330, 430, '{}'.format(cupom.documentoFiscal.vendedor))
        c.setFont(font_name, 20)
        c.drawString(100, 390, "Qual a maior campanha de premios do Piauí?")
        c.setFont(font_name_bold, 20)
        c.drawString(100, 360, "(X) Liquida Teresina 2023")
        # c.drawString(340, 360, "( ) Outra")
        c.setFont(font_name, 20)
        c.drawString(40, 320, "Data:")
        c.setFont(font_name_bold, 20)
        df = DateFormat(cupom.documentoFiscal.dataDocumento)
        c.drawString(100, 320, '{}'.format(df.format('d/m/Y')))
        c.setFont(font_name, 40)
        c.drawString(80, 250, "CUPOM")
        c.setFont(font_name_bold, 45)
        c.drawString(100, 200, '{}'.format(cupom.id))
        c.drawString(20, 7  , "_____________________________________________________")
        c.setFont(font_name_bold, 20)
        c.drawString(150, 15, "SRE/ME N° 06.028066/2023")
        renderPDF.draw(d, c, 320, 80)
        c.showPage()

    c.save()

     # write PDF to buffer
    # Get the value of the StringIO buffer and write it to the response.
    pdf = buffer.getvalue()

    buffer.close()

    response.write(pdf)

    return response
