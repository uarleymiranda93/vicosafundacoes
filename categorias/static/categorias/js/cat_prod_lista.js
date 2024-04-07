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

function isValidColor(color) {
    // Implemente sua lógica para validar a cor aqui
    // Por exemplo, você pode usar expressões regulares ou outras técnicas de validação
    return /^#[0-9A-F]{6}$/i.test(color); // Verifica se a cor está no formato "#RRGGBB"
}

var tab_cat_prod = function() {
    var kt_cat_prod = function() {
        
        var table = $('#kt_cat_prod');
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
                search:         "cat_prodquisar:",
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
                url: '/categorias/cat_prod_lista/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                },
            },
            order: [[ 0, 'asc' ]],
            columns: [
                {data: 'cat_prod_id'},
                {data: 'cat_prod_nome'},
                {data: 'cat_prod_cor'},
                {data: 'cat_prod_ativo'},
                {data: null, responsivePriority: -1},
            ],
            columnDefs: [
                {
                targets: [2],
                type: "text",
                render: function(data) {
                    if (data.startsWith('#') && (data.length === 7 || data.length === 4)) {
                        return '<div style="width: 30px; height: 30px; background-color: ' + data + ';"></div>';
                    } else {
                        return data;
                    }
                }
                },  
                {
                    targets: [3],
                    type: "text",
                    render: function(data) {
                        if (data === true) {
                            return '<span class="btn btn-text-success btn-hover-light-success font-weight-bold mr-2">Sim</span>';
                        } else {
                            return '<span class="btn btn-text-danger btn-hover-light-danger font-weight-bold mr-2">Não</span>';
                        }
                    },
                },                
                {
                    targets: [-1],
                    orderable: false,
                    render: function(data, type, row) {
                        return '\
                            <button type="button" onclick="cat_prod_edt(' + row.cat_prod_id + ')" class="btn btn-light-success btn-icon btn-circle"\
                                data-toggle="tooltip" data-placement="bottom" value="update" title="Editar">\
                                <i class="flaticon-edit"></i>\
                            </button> \
                            <button type="button" onclick="cat_prod_del(' + row.cat_prod_id + ')" class="btn btn-light-danger btn-icon btn-circle"\
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
            kt_cat_prod();
        },
    };
}();



jQuery(document).ready(function() {
    tab_cat_prod.init()
    
});

function abrir_modal_cat_prod(){
    $('#cat_prod_btn_salvar').val('insert');
    $('#cat_prod_nome').val('');
    $('#cat_prod_cor').val('');
    $('#cat_prod_ativo').prop('checked', false);
    $('#frm_cat_prod_modal').modal('show');
}

function cat_prod_add(){
    var url
    if($('#cat_prod_btn_salvar').val() == 'update'){
        url = '/categorias/cat_prod_edt/'
    }else{
        url = '/categorias/cat_prod_add/'
    }

    var frm_cat_prod = new FormData(document.getElementById('frm_cat_prod'));

    $.ajax({
        method: 'POST',
        url: url,
        data: frm_cat_prod,
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
            $('#kt_cat_prod').DataTable().ajax.reload();
            $('#frm_cat_prod_modal').modal('hide');
            Swal.close();
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        Swal.close();
        console.log(jqXHR);
        Swal.fire("Ops! Algo deu errado!", jqXHR.responseJSON.aviso, "error");
    });
}

function cat_prod_edt(cat_prod_id){
    $.getJSON('/categorias/cat_prod_atb/',
        {
            id:cat_prod_id
        }
    ).done(function (item) {
        $('#cat_prod_id').val(item.cat_prod_id);
        $('#cat_prod_nome').val(item.cat_prod_nome);
        $('#cat_prod_cor').val(item.cat_prod_cor);
        if (item.cat_prod_ativo) {
            $('#cat_prod_ativo').prop('checked', true);
        } else {
            $('#cat_prod_ativo').prop('checked', false);
        }
        $('#cat_prod_btn_salvar').val('update');
        $('[href="#kt_tab_pane_1"]').tab('show');
        $('#frm_cat_prod_modal').modal('show');
    })
    .fail(function (jqxhr, settings, ex) {
        exibeDialogo(result.responseText, tipoAviso.ERRO);
    });
}

function cat_prod_del(cat_prod_id) {
    Swal.fire({
        title: "Deseja executar esta operação?",
        text: "O registro " + cat_prod_id + " será removido permanentemente.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Ok, desejo remover!",
        cancelButtonText: "Não, cancelar!",
        reverseButtons: true
    }).then(function(result) {
        if (result.value) {
            var dados = new FormData();
                dados.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
                dados.append("cat_prod_id",cat_prod_id);
            $.ajax({
                method: 'POST',
                url:'/categorias/cat_prod_del/',
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
                    $('#kt_cat_prod').DataTable().ajax.reload();
                    $('#frm_cat_prod_modal').modal('hide');
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