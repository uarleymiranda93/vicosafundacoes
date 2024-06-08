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
            order: [[ 5, 'asc' ]],
            columns: [
                {data: 'forn_nome'},
                {data: 'cat_aval_nome'},
                {data: 'forn_aval_dta'},
                {data: 'pes_nome'},
                {data: 'forn_aval_evid'},
                {data: 'forn_aval_id'},
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
            paging: false,
            language: {
                info: "", 
                processing:     "Processamento em andamento...",
                search:         "Pesquisar:",
                // infoFiltered:   "(Filtrados de MAX registros)",
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
            order: [[ 5, 'asc' ]],
            columns: [
                {data: null, responsivePriority: 0},
                {data: 'cat_aval_item_nome', responsivePriority: 1},
                {data: 'aval_item_nota', responsivePriority: 2},
                {data: 'aval_item_grau', responsivePriority: 3},
                {data: null, responsivePriority: 4},
                {data: 'aval_item_id', responsivePriority: 5},
            ],
            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                    className: 'checkble',
                    render: function(data, type, row) {
                        return '<input type="checkbox" class="checkble">';
                    }
                },
                {
                    targets: 4,
                    orderable: false,
                    className: 'text-center',
                    render: function(data, type, row) {
                        return (parseFloat(row.aval_item_grau * 10)).toFixed(1);
                    },
                },
                {
                    targets: [1, 2, 3, 4, 5], // Especifique as colunas que deseja centralizar
                    className: 'text-center' // Aplica a classe de estilo CSS
                },
            ],
            footerCallback: function(row, data, start, end, display) {
                var api = this.api();
                var sum = api
                    .column(3, { page: 'current' })
                    .data()
                    .reduce(function(acc, value) {
                        var valorNumerico = parseFloat(value); // Converte para número
                    if (!isNaN(valorNumerico)) { // Verifica se é um número válido
                        return acc + valorNumerico;
                    } else {
                        return acc; // Se não for um número válido, mantém o valor acumulado sem alteração
                    }
                }, 0);
                var indiceAvaliacao = (sum * 10).toFixed(1) + '%';
                $(api.column(3).footer()).html('Pontuação Total:'+ '<br>Índice de Avaliação: ');
                $(api.column(4).footer()).html(  (sum * 10).toFixed(1) + '<br>' + indiceAvaliacao);
            },
            // Adiciona uma função para criar atributos data-id para cada linha
            createdRow: function(row, data, dataIndex) {
                $(row).attr('data-id', data.aval_item_id);
            }
        });  
    };

    return {
        //main function to initiate the module
        init: function() {
            kt_aval_item();
        },
    };
}();

function edt_aval_div(){
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

function abrir_modal_itens() {
    // Verifica se nenhum checkbox está marcado
    var anyChecked = $('#kt_aval_item tbody').find('input.checkble:checked').length > 0;
    if (!anyChecked) {
        Swal.fire({
            icon: 'warning',
            title: 'Atenção!',
            text: 'Por favor, selecione pelo menos um item.',
            confirmButtonText: 'OK'
        });
        return;
    }

    // Define o evento de clique para o botão de salvar
    $('#item_btn_salvar').click(function() {
        // // Verifica se pelo menos um checkbox está selecionado
        var checkedRows = $('#kt_aval_item tbody').find('input.checkble:checked').closest('tr'); // Encontra todas as linhas com checkboxes marcados
        // Array para armazenar os IDs das linhas selecionadas
        var selectedIds = [];

        // Itera sobre cada linha selecionada para extrair o ID
        checkedRows.each(function() {
            var rowId = $(this).data('id');
            selectedIds.push(rowId);
        });

        // Chama a função item_edt_div apenas se houver IDs selecionados
        if (selectedIds.length > 0) {
            item_edt_div(selectedIds);
        }
    });
    
    $('#frm_itens_modal').modal('show');
}

jQuery(document).ready(function() {
    tabela_aval.init()
    pesq_pessoa('#pes')
    pesq_cat_aval('#cat_aval')
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e){
        $($.fn.dataTable.tables(true)).DataTable()
           .columns.adjust();
     });

    var table = $('#kt_aval_item').DataTable();
    $('#kt_aval_item').on('change', 'input.checkble:first', function() {
        var isChecked = $(this).prop('checked');
        // Marca ou desmarca todos os checkboxes nas linhas com base no estado do checkbox "selecionar tudo"
        $('#kt_aval_item tbody').find('input.checkble').prop('checked', isChecked);
    });


});


function item_edt_div(selectedIds) {
    // Crie um FormData e adicione os IDs selecionados
    var frm_item = new FormData(document.getElementById('frm_item'));
    frm_item.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
    for (var i = 0; i < selectedIds.length; i++) {
        frm_item.append('aval_item_id', selectedIds[i]);
        frm_item.append('forn_aval_id', $('#forn_aval_id'));
    }

    // Faça a solicitação AJAX para editar os itens no banco de dados
    $.ajax({
        method: 'POST',
        url: '/fornecedor/item_edt_div/',
        data: frm_item,
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
    .done(function(data, textStatus, jqXHR) {
        if (jqXHR.status === 200 && jqXHR.readyState === 4) {
            $('#kt_aval_item').DataTable().ajax.reload();
            $('#frm_itens_modal').modal('hide');
            Swal.close();
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        Swal.close();
        console.log(jqXHR);
        Swal.fire("Ops! Algo deu errado!", jqXHR.responseJSON.aviso, "error");
    });
}

function aval_salvar(){
    var frm_aval = new FormData(document.getElementById('frm_aval'));

    $.ajax({
        method: 'POST',
        url: '/fornecedor/aval_edt/',
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
        console.log(item)
        $('#forn_aval_id').val(item.forn_aval_id);

        $('#forn').empty();
            var forn = new Option(item.forn_nome,item.forn,true,true);
        $('#forn').append(forn).trigger('change');

        if(item.cat_aval){
            $('#cat_aval').empty();
                var cat_aval = new Option(item.cat_aval_nome,item.cat_aval,true,true);
            $('#cat_aval').append(cat_aval).trigger('change');
        }else{
            var cat_aval = new Option('', '', false, true); // Opção vazia
            $('#cat_aval').empty().append(pes).trigger('change');
        }
        
        if (item.pes) {
            $('#pes').empty();
            var pes = new Option(item.pes_nome, item.pes, true, true);
            $('#pes').append(pes).trigger('change');
        } else {
            var pes = new Option('', '', false, true); // Opção vazia
            $('#pes').empty().append(pes).trigger('change');
        }
        
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
