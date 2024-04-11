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

var tabela_aval = function() {
    var kt_aval = function() {
        
        var table = $('#kt_aval');
        
        // Destrói a instância existente do DataTable, se houver
        if ($.fn.DataTable.isDataTable('#kt_aval')) {
            table.DataTable().destroy();
        }

        // Inicializa o DataTable novamente com as novas configurações
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
                url: '/fornecedor/aval_list/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                    // d.forn_id = $("#forn_id").val();
                },
            },
            order: [[ 0, 'asc' ]],
            columns: [
                {data: 'forn_aval_id'},
                {data: 'forn_nome'},
                {data: 'cat_aval_nome'},
                {data: 'forn_aval_dta'},
                {data: 'pes_nome'},
                {data: 'forn_aval_evid'},
                {data: null, responsivePriority: -1},
            ],
            columnDefs: [
                {
                    targets:[2],
                    render:function(data, type, row){
                        if(data){
                            return moment(data).format("DD/MM/YYYY")
                        }else{
                            return ''
                        }
                        
                    }

                }, 
                {
                    targets: [-1],
                    orderable: false,
                    render: function(data, type, row) {
                        return '\
                            <button type="button" onclick="aval_edt(' + row.forn_aval_id + ')" class="btn btn-light-success btn-icon btn-circle"\
                                data-toggle="tooltip" data-placement="bottom" value="update" title="Editar">\
                                <i class="flaticon-edit"></i>\
                            </button> \
                            <button type="button" onclick="aval_del(' + row.forn_aval_id + ')" class="btn btn-light-danger btn-icon btn-circle"\
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
            kt_aval();
        },
    };
}();

var tabela_aval_item = function() {
    var kt_aval_item = function() {
        
        var table = $('#kt_aval_item');
        
        // Destrói a instância existente do DataTable, se houver
        if ($.fn.DataTable.isDataTable('#kt_aval')) {
            table.DataTable().destroy();
        }

        // Inicializa o DataTable novamente com as novas configurações
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
                url: '/fornecedor/aval_item_list/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                    d.forn_aval_id = $("#forn_aval_id").val();
                },
            },
            order: [[ 0, 'asc' ]],
            columns: [
                {data: 'aval_item_id'},
                {data: 'cat_aval_item_nome'},
                {data: 'aval_item_grau'},
                {data: 'aval_item_nota'},
                {data: null},
                {data: null, responsivePriority: -1},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    orderable: false,
                    render: function(data, type, row) {
                        return '\
                            <button type="button" onclick="aval_edt(' + row.forn_aval_id + ')" class="btn btn-light-success btn-icon btn-circle"\
                                data-toggle="tooltip" data-placement="bottom" value="update" title="Editar">\
                                <i class="flaticon-edit"></i>\
                            </button> \
                            <button type="button" onclick="aval_del(' + row.forn_aval_id + ')" class="btn btn-light-danger btn-icon btn-circle"\
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
            kt_aval_item();
        },
    };
}();

function abrir_modal_aval(){
    $('#aval_btn_salvar').val('insert');
    $('#frm_aval').trigger ('reset');
    $('#cat_aval').val('').trigger('change'); 
    $('#pes').val('').trigger('change'); 
    // $('#forn_ava_nome').val('');
    // $('#forn_ctt_tel').val('');
    // $('#forn_ctt_email').val('');
    // $('#forn_ctt_ativo').prop('checked', false);
    $('#frm_aval_modal').modal('show');
}

jQuery(document).ready(function() {
    tabela_aval.init()

});


function aval_add(){
    var url;

    if($('#aval_btn_salvar').val() == 'update'){
        url = '/fornecedor/aval_edt/'
    }else{
        url = '/fornecedor/aval_add/'
    }

    var frm_aval = new FormData(document.getElementById('frm_aval'));
        frm_aval.append('forn_id',$('#forn_id').val())

    $.ajax({
        method: 'POST',
        url: url,
        data: frm_aval,
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
            $('#kt_aval').DataTable().ajax.reload();
            $('#frm_aval_modal').modal('hide');
            Swal.close();
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        Swal.close();
        console.log(jqXHR);
        Swal.fire("Ops! Algo deu errado!", jqXHR.responseJSON.aviso, "error");
    });
}

function aval_edt(forn_aval_id){
    $.getJSON('/fornecedor/aval_atb/',
        {
            forn_aval_id: forn_aval_id
        }
    ).done(function (item) {
        $('#forn_aval_id').val(item.forn_aval_id);

        $('#cat_aval').empty();
            var cat_aval = new Option(item.cat_aval_nome,item.cat_aval,true,true);
        $('#cat_aval').append(cat_aval).trigger('change');

        $('#pes').empty();
            var pes = new Option(item.pes_nome,item.pes,true,true);
        $('#pes').append(pes).trigger('change');

        $('#forn_aval_evid').val(item.forn_aval_evid);
        $('#forn_aval_dta').val(moment(item.forn_aval_dta).format("YYYY-MM-DD"));
        $('#aval_btn_salvar').val('update');
        $('#frm_aval_modal').modal('show');
        tabela_aval_item.init()
    })
    .fail(function (jqxhr, settings, ex) {
        exibeDialogo(result.responseText, tipoAviso.ERRO);
    });
}

function aval_del(forn_aval_id) {
    Swal.fire({
        title: "Deseja executar esta operação?",
        text: "O registro " + forn_aval_id + " será removido permanentemente.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Ok, desejo remover!",
        cancelButtonText: "Não, cancelar!",
        reverseButtons: true
    }).then(function(result) {
        if (result.value) {
            var dados = new FormData();
                dados.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
                dados.append("forn_aval_id", forn_aval_id);

            $.ajax({
                method: 'POST',
                url: '/fornecedor/aval_del/',
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
                    $('#kt_aval').DataTable().ajax.reload();
                    $('#frm_aval_modal').modal('hide');
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
