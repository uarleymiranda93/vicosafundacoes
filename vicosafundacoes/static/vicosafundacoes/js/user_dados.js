function carregarInformacoesUsuario() {
    // Fazendo uma requisição AJAX para obter os dados do usuário da sua API
    fetch('/vicosafundacoes/pes_lista/')
    .then(response => response.json())
    .then(data => {
        // Verifica se a resposta da API contém dados válidos
        if (data && data.dados && data.dados.length > 0) {
            // Obtém os dados do primeiro usuário (supondo que a API retorna uma lista de usuários)
            const usuario = data.dados[0];
            
            // Preenchendo os campos do formulário com os dados do usuário
            document.getElementById("pes_nome").value = usuario.pes_nome;
            document.getElementById("pes_doc").value = usuario.pes_doc;
            document.getElementById("pes_ctt").value = usuario.pes_ctt;
            document.getElementById("pes_email").value = usuario.pes_email;
            document.getElementById("usu_cad_dta").value = usuario.usu_cad_dta;
            document.getElementById("usu_alt_dta").value = usuario.usu_alt_dta;
        } else {
            console.error('Erro ao obter dados do usuário');
        }
    })
    .catch(error => console.error('Erro ao carregar informações do usuário:', error));
}

// Chamando a função para carregar as informações do usuário quando a página carregar
window.onload = function() {
    carregarInformacoesUsuario();
};



function pes_add(){
    var url
    if($('#pes_btn_salvar').val() == 'update'){
        url = '/vicosafundacoes/pes_edt/'
    }else{
        url = '/vicosafundacoes/pes_add/'
    }

    var frm_pes = new FormData(document.getElementById('frm_pes'));

    $.ajax({
        method: 'POST',
        url:url,
        data: frm_pes,
        contentType: false,
        cache: false,
        processData: false,
        beforeSend: function() {
            Swal.fire({
                title: "Carregando os dados",
                text: "Aguarde ...",
                allowOutsideClick: false,
                allowEscapeKey: false,
                allowEnterKey: false,
                didOpen: function() {            
                    Swal.showLoading();
                }
            })
        },
    })
    .done(function(data,  textStatus, jqXHR){
        if (jqXHR.status === 200 && jqXHR.readyState === 4){
            Swal.fire({
                title: "Sucesso!",
                text: "Os dados do usuário foram salvos com sucesso!",
                icon: "success",
                confirmButtonText: "OK",
                onClose: function() {
                    window.location.href = '/vicosafundacoes/';
                }
            });
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        Swal.close();
        console.log(jqXHR);
        Swal.fire("Ops! Algo deu errado!", jqXHR.responseJSON.aviso, "error");
    });
}

// Função para lidar com a seleção da imagem
function handleImageUpload(event) {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('pes_path_img', file);

    // Enviar a imagem ao servidor via AJAX
    $.ajax({
        method: 'POST',
        url: '/vicosafundacoes/pes_add/',
        data: formData,
        contentType: false,
        processData: false,
        success: function(data) {
            // Aqui você pode lidar com a resposta do servidor, como atualizar a imagem exibida
            console.log('Imagem enviada com sucesso!');
        },
        error: function(xhr, status, error) {
            console.error('Erro ao enviar imagem:', error);
        }
    });
}
// Adicionar um ouvinte de evento de mudança ao input de tipo de arquivo
$('#pes_path_img').change(handleImageUpload);



function pes_edt(pes_id) {
    $.getJSON('/vicosafundacoes/pes_atb/',
        {
            id: pes_id
        }
    ).done(function (item) {
        $('#pes_id').val(item.pes_id);
        $('#pes_nome').val(item.pes_nome);
        $('#pes_ctt').val(item.pes_ctt);
        $('#pes_nome_adm').val(item.pes_nome_adm);
        $('#pes_adm_id').val(item.pes_adm_id);

        $('#pes_btn_salvar').val('update');
    })
    .fail(function (jqxhr, settings, ex) {
        exibeDialogo(result.responseText, tipoAviso.ERRO);
    });
}


function pes_del(pes_id) {
    Swal.fire({
        title: "Deseja executar esta operação?",
        text: "O registro " + pes_id + " será removido permanentemente.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Ok, desejo remover!",
        cancelButtonText: "Não, cancelar!",
        reverseButtons: true
    }).then(function(result) {
        if (result.value) {
            var dados = new FormData();
                dados.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
                dados.append("pes_id",pes_id);
            $.ajax({
                method: 'POST',
                url:'/vicosafundacoes/cat_pes_del/',
                data:  dados,
                contentType: false,
                cache: false,
                processData: false,
                beforeSend: function() {
                    Swal.fire({
                        title: "Operação em andamento",
                        text: "Aguarde ...",
                        allowOutsideClick: false,
                        allowEscapeKey: false,
                        allowEnterKey: false,
                        didOpen: function() {            
                            Swal.showLoading();
                        }
                    })
                },
            })
            .done(function(data,  textStatus, jqXHR){
                console.log(jqXHR);
                if (jqXHR.status === 200 && jqXHR.readyState === 4){
                    $('#kt_pes').DataTable().ajax.reload();
                    $('#frm_pes_modal').modal('hide');
                    Swal.close();
                }
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                Swal.close();
                Swal.fire("Ops! Algo deu errado!", jqXHR.responseJSON.aviso, "error");
            });
        }
    });
};