from cryptography.fernet import Fernet
from django.contrib.auth.decorators import login_required, user_passes_test

masterkey = "'jpvBrLzACz-NHI12Z5Yo7UTOC90fSLLM0Lp84SW_Pmw='"

def tokenGen(code):
    f = Fernet(masterkey)
    return f.encrypt(code)
