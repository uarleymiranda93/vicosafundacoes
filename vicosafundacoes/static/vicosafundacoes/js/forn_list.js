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

var tabela_ctt = function() {
    var kt_ctt = function() {
        
        var table = $('#kt_ctt');
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
                url: '/vicosafundacoes/ctt_list/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                },
            },
            order: [[ 0, 'asc' ]],
            columns: [
                {data: 'forn_ctt_id'},
                {data: 'forn_ctt_nome'},
                {data: 'forn_ctt_tel'},
                {data: 'forn_ctt_email'},
                {data: 'forn_ctt_ativo'},
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
                    targets: [4], // índice da coluna 'ativo'
                    render: function ( data, type, row ) {
                        if (data) {
                            return '<i class="fa fa-check-circle text-success"></i>'; // ícone verde para true
                        } else {
                            return '<i class="fa fa-times-circle text-danger"></i>'; // ícone vermelho para false
                        }
                    }
                }, 
                {
                    targets: [-1],
                    orderable: false,
                    render: function(data, type, row) {
                        return '\
                            <button type="button" onclick="ctt_edt(' + row.forn_ctt_id + ')" class="btn btn-light-success btn-icon btn-circle"\
                                data-toggle="tooltip" data-placement="bottom" value="update" title="Editar">\
                                <i class="flaticon-edit"></i>\
                            </button> \
                            <button type="button" onclick="ctt_del(' + row.forn_ctt_id + ')" class="btn btn-light-danger btn-icon btn-circle"\
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
            kt_ctt();
        },
    };
}();


jQuery(document).ready(function() {
    tabela_forn.init()

    pesq_impacto('#cat_imp')
    pesq_tipo('#cat_tip')
    
});

function abrir_modal_forn(){
    $('#forn_btn_salvar').val('insert');
    $('#aba_cont').hide();
    $('#forn_nome').val('');
    $('#forn_cnpj').val('');
    $('#forn_ies').val('');
    $('#frm_forn_modal').modal('show');
}

function abrir_modal_ctt(){
    $('#ctt_btn_salvar').val('insert');
    $('#forn_ctt_nome').val('');
    $('#forn_ctt_tel').val('');
    $('#forn_ctt_email').val('');
    $('#forn_ctt_ativo').prop('checked', false);
    $('#frm_ctt_modal').modal('show');
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
        tabela_ctt.init()
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

function ctt_add(){
    var url;

    if($('#ctt_btn_salvar').val() == 'update'){
        url = '/vicosafundacoes/ctt_edt/'
    }else{
        url = '/vicosafundacoes/ctt_add/'
    }

    var frm_ctt = new FormData(document.getElementById('frm_ctt'));
        frm_ctt.append('forn_id',$('#forn_id').val())

    $.ajax({
        method: 'POST',
        url: url,
        data: frm_ctt,
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
            $('#kt_ctt').DataTable().ajax.reload();
            $('#frm_ctt_modal').modal('hide');
            Swal.close();
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        Swal.close();
        console.log(jqXHR);
        Swal.fire("Ops! Algo deu errado!", jqXHR.responseJSON.aviso, "error");
    });
}

function ctt_edt(forn_ctt_id){
    $.getJSON('/vicosafundacoes/ctt_atb/',
        {
            forn_ctt_id: forn_ctt_id
        }
    ).done(function (item) {
        $('#forn_ctt_id').val(item.forn_ctt_id);
        $('#forn_ctt_nome').val(item.forn_ctt_nome);
        $('#forn_ctt_tel').val(item.forn_ctt_tel);
        $('#forn_ctt_email').val(item.forn_ctt_email);
        $('#forn_ctt_ativo').val(item.forn_ctt_ativo);
        $('#ctt_btn_salvar').val('update');
        $('#frm_ctt_modal').modal('show');
    })
    .fail(function (jqxhr, settings, ex) {
        exibeDialogo(result.responseText, tipoAviso.ERRO);
    });
}

function ctt_del(forn_ctt_id) {
    Swal.fire({
        title: "Deseja executar esta operação?",
        text: "O registro " + forn_ctt_id + " será removido permanentemente.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Ok, desejo remover!",
        cancelButtonText: "Não, cancelar!",
        reverseButtons: true
    }).then(function(result) {
        if (result.value) {
            var dados = new FormData();
                dados.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
                dados.append("forn_ctt_id", forn_ctt_id);

            $.ajax({
                method: 'POST',
                url: '/vicosafundacoes/ctt_del/',
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
                    $('#kt_ctt').DataTable().ajax.reload();
                    $('#frm_ctt_modal').modal('hide');
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