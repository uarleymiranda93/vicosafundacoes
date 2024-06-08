from django.shortcuts import get_object_or_404
from vicosafundacoes.models import Pessoa

def user_session(request):
    usuario_id = request.user.id
    pessoa_associada = get_object_or_404(Pessoa, pes_adm_id=usuario_id)
    return pessoa_associada.pes_id