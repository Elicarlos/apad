import string
import secrets
def validarticket():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(6))
    return  {
        'codigo': 12345,
        'cpf': '123.321.222-59',
        'nome': 'Marcus Vinicius Morais de Sousa',
        'horário': '11:30AM',
        'data': '09/12/2022',
        'local': 'Banco do Nordeste',},

