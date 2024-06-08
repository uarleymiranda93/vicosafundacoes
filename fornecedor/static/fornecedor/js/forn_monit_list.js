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

var tabela_monit = function() {
    var kt_monit = function() {
        
        var table = $('#kt_monit');
        
        // Destrói a instância existente do DataTable, se houver
        if ($.fn.DataTable.isDataTable('#kt_monit')) {
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
                url: '/fornecedor/monit_list/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                    // d.forn_id = $("#forn_id").val();
                },
            },
            order: [[ 5, 'asc' ]],
            columns: [
                {data: 'forn_nome'},
                {data: 'forn_monit_qld'},
                {data: 'forn_monit_pont'},
                {data: 'forn_monit_val'},
                {data: 'forn_monit_sup'},
                {data: 'forn_monit_id'},
                {data: null, responsivePriority: -1},
            ],
            columnDefs: [
                {
                    targets: [1, 2, 3, 4],
                    className: 'text-center',
                    render: function(data, type, row) {
                        if (data === true) {
                            return '<span class="text-success">OK</span>';
                        } else if (data === false) {
                            return '<span class="text-danger">NC</span>';
                        } else {
                            return ''; // Retorna vazio se data for null
                        }
                    }
                },
                {
                    targets: [-1],
                    orderable: false,
                    render: function(data, type, row) {
                        return '\
                            <button type="button" onclick="monit_edt(' + row.forn_monit_id + ')" class="btn btn-light-success btn-icon btn-circle"\
                                data-toggle="tooltip" data-placement="bottom" value="update" title="Editar">\
                                <i class="flaticon-edit"></i>\
                            </button> \
                        ';
                    },
                },
            ],
        });  
    };

    return {
        //main function to initiate the module
        init: function() {
            kt_monit();
        },
    };
}();

jQuery(document).ready(function() {
    tabela_monit.init()
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e){
        $($.fn.dataTable.tables(true)).DataTable()
           .columns.adjust();
     });
});

function monit_salvar(){
    var frm_monit = new FormData(document.getElementById('frm_monit'));
    $.ajax({
        method: 'POST',
        url: '/fornecedor/monit_edt/',
        data: frm_monit,
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
            $('#kt_monit').DataTable().ajax.reload();
            $('#frm_monit_modal').modal('hide');
            Swal.close();
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        Swal.close();
        console.log(jqXHR);
        Swal.fire("Ops! Algo deu errado!", jqXHR.responseJSON.aviso, "error");
    });
}

function monit_edt(forn_monit_id){
    $.getJSON('/fornecedor/monit_atb/',
        {
            forn_monit_id: forn_monit_id
        }
    ).done(function (item) {
        $('#aba_cont').show();
        $('#aba_aval').show();
        $('#forn_monit_id').val(item.forn_monit_id);
        $('#forn_nome').val(item.forn_nome);
        $('#forn_cnpj').val(item.forn_cnpj);
        $('#forn_ies').val(item.forn_ies);
        $('#forn_desc').val(item.forn_desc);
        
        $('#cat_imp').empty();
            var cat_imp = new Option(item.cat_imp_nome,item.cat_imp_id,true,true);
        $('#cat_imp').append(cat_imp).trigger('change');

        $('#cat_tip').empty();
            var cat_tip = new Option(item.cat_tip_nome,item.cat_tip_id,true,true);
        $('#cat_tip').append(cat_tip).trigger('change');

        $('#forn_btn_salvar').val('update');
        $('#frm_monit_modal').modal('show');
        tabela_ctt.init()
        tabela_aval.init()
    })
    .fail(function (jqxhr, settings, ex) {
        exibeDialogo(result.responseText, tipoAviso.ERRO);
    });
}
