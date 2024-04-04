"use strict";

$.fn.dataTable.Api.register('column().title()', function() {
    return $(this.header())[0].dataset.field;
}); 

const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});

var tabela_forn = function() {
    var kt_forn = function() {
        
        var table = $('#kt_forn');
        // begin first table
        table.on('processing.dt', function (e, settings, processing) {
            if (processing) {
                Toast.fire({
                    icon: 'success',
                    title: 'Sucesso! Carregando os dados ...'
                });
            } else {
                Toast.close();
            }
        }).DataTable({
            responsive: true,
            processing: true,
            pageLength: 10,
            paging: false,
            language: {
                processing:     "Processamento em andamento...",
                search:         "Pesquisar:",
                lengthMenu:     "MENU registros por página",
                info:           "Mostrando de START até END de TOTAL registros",
                infoEmpty:      "Mostrando 0 até 0 de 0 registros",
                infoFiltered:   "(Filtrados de MAX registros)",
                infoPostFix:    "",
                loadingRecords: "Carregando registros...",
                zeroRecords:    "Nenhum registro encontrado",
                emptyTable:     "Nenhum registro encontrado",
                paginate: {
                    first:      "Primeiro",
                    previous:   "Anterior",
                    next:       "Avançar",
                    last:       "Último"
                },
                aria: {
                    sortAscending:  ": Ordenar coluna por ordem crescente",
                    sortDescending: ": Ordenar coluna por ordem decrescente"
                }
            },
            ajax: {
                url: '/vicosafundacoes/forn_list/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                },
            },
            order: [[ 0, 'asc' ]],
            columns: [
                {data: 'forn_id'},
                {data: 'forn_nome'},
                // {data: },
                {data: 'forn_cnpj'},
                {data: 'forn_ies'},
                {data: null, responsivePriority: -1},
            ],
            columnDefs: [
                // {
                //     targets:[2,3],
                //     type:"date-eu",
                //     render:function(data)
                //     {
                //         return data ? moment(data).format('DD/MM/YYYY') : '';
                //     },
                // },
                {
                    targets: [-1],
                    orderable: false,
                    render: function(data, type, row) {
                        return '\
                            <button type="button" onclick="forn_edt(' + row.forn_id + ')" class="btn btn-light-success btn-icon btn-circle"\
                                data-toggle="tooltip" data-placement="bottom" value="update" title="Editar">\
                                <i class="flaticon-edit"></i>\
                            </button> \
                            <button type="button" onclick="forn_del(' + row.forn_id + ')" class="btn btn-light-danger btn-icon btn-circle"\
                                data-toggle="tooltip" data-placement="bottom" title="Remover">\
                                <i class="flaticon-delete"></i>\
                            </button>\
                        ';
                    },
                },
            ],
        });  
    };

    return {
        //main function to initiate the module
        init: function() {
            kt_forn();
        },
    };
}();



jQuery(document).ready(function() {
    tabela_forn.init()
    
});

function abrir_modal_forn(){
    $('#forn_btn_salvar').val('insert');
    $('#aba_cont').hide();
    $('#frm_forn_modal').modal('show');
}

function forn_add(){
    alert($('#forn_btn_salvar').val())
    var url
    if($('#forn_btn_salvar').val() == 'update'){
        url = '/vicosafundacoes/forn_edt/'
        alert("aqui1")
    }else{
        url = '/vicosafundacoes/forn_add/'
    }

    var frm_forn = new FormData(document.getElementById('frm_forn'));

    $.ajax({
        method: 'POST',
        url: url,
        data: frm_forn,
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
            $('#kt_forn').DataTable().ajax.reload();
            $('#frm_forn_modal').modal('hide');
            Swal.close();
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        Swal.close();
        console.log(jqXHR);
        Swal.fire("Ops! Algo deu errado!", jqXHR.responseJSON.aviso, "error");
    });
}

function forn_edt(forn_id){
    $.getJSON('/vicosafundacoes/forn_atb/',
        {
            forn_id: forn_id
        }
    ).done(function (item) {
        $('#aba_cont').show();
        $('#forn_id').val(item.forn_id);
        $('#forn_nome').val(item.forn_nome);
        $('#forn_cnpj').val(item.forn_cnpj);
        $('#forn_ies').val(item.forn_ies);
        $('#forn_btn_salvar').val('update');
        // KTDatatablesDataSourceProdutoArquivo.init();
        $('[href="#kt_tab_pane_1"]').tab('show');
        $('#frm_forn_modal').modal('show');
    })
    .fail(function (jqxhr, settings, ex) {
        exibeDialogo(result.responseText, tipoAviso.ERRO);
    });
}

function forn_del(forn_id) {
    Swal.fire({
        title: "Deseja executar esta operação?",
        text: "O registro " + forn_id + " será removido permanentemente.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Ok, desejo remover!",
        cancelButtonText: "Não, cancelar!",
        reverseButtons: true
    }).then(function(result) {
        if (result.value) {
            var dados = new FormData();
                dados.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
                dados.append("forn_id", forn_id);

            $.ajax({
                method: 'POST',
                url: '/vicosafundacoes/forn_del/',
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
                    $('#kt_forn').DataTable().ajax.reload();
                    $('#frm_forn_modal').modal('hide');
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