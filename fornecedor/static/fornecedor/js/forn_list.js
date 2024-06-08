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
    var selectedIds = []; // Array para armazenar os IDs das linhas selecionadas

    var kt_forn = function() {
        var table = $('#kt_forn').DataTable({
            responsive: true,
            processing: true,
            pageLength: 10,
            paging: false,
            language: {
                processing:     "Processamento em andamento...",
                search:         "Pesquisar:",
                lengthMenu:     "MENU registros por página",
                info:           "Mostrando de _START_ até _END_ de _TOTAL_ registros",
                infoEmpty:      "Mostrando 0 até 0 de 0 registros",
                infoFiltered:   "(Filtrados de _MAX_ registros)",
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
                url: '/fornecedor/forn_list/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                },
            },
            order: [[ 9, 'asc' ]],
            columns: [
                {data: null, responsivePriority: 0},
                {data: 'forn_nome'},
                {data: 'cat_tip_nome'},
                {data: 'cat_imp_nome'},
                {data: 'forn_desc'},
                {data: 'forn_cont'},
                {data: 'forn_cnpj'},
                {data: 'forn_ies'},
                {data: 'forn_nf'},
                {data: 'forn_id'},
                {data: null, responsivePriority: -1},
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
                    targets: [3],
                    render: function(data, type, row) {
                        return '\
                            <span class="rounded-lg p-3 font-weight-boldest" style="background-color:'+row.cat_imp_cor +'; color:'+row.cat_imp_nome+'">'+data+'</span>\
                        ';
                    }
                },
                {
                    targets: [8],
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
                    targets: [5], // Índice da coluna para os detalhes dos contatos
                    render: function(data, type, row) {
                        var html = '';
                        for (var i = 0; i < data.length; i++) {
                            html += '<div>' + data[i].forn_ctt_nome + ' ' + data[i].forn_ctt_tel + '</div>';
                        }
                        return html;
                    }
                }, 
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
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'csvHtml5',
                    text: 'CSV',
                    className: 'dropdown-item',
                    action: function (e, dt, button, config) {
                        var selectedRowsData = dt.rows({ selected: true }).data(); // Obtém os dados das linhas selecionadas
                        var selectedIds = selectedRowsData.map(function(row) {
                            console.log(row.forn_id)
                            return row.forn_id; // Supondo que cada linha tenha um campo 'id'
                            
                        });
            
                        $.ajax({
                            url: '/fornecedor/relatorio_aprov/',
                            type: 'POST',
                            data: (function() {
                                var dados = new FormData();
                                dados.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
                                dados.append("forn_ids", selectedIds);
                                return dados;
                            })(),
                            processData: false, // Não processar os dados como uma string
                            contentType: false, // Não configurar o tipo de conteúdo
                            success: function(response) {
                                // Processamento dos dados de resposta, se necessário
                                // Em seguida, exporta os dados obtidos para CSV
                                var data = response.dados; // Supondo que a resposta contém os dados a serem exportados
                                var csvData = ''; // String para armazenar os dados CSV
                        
                                // Aqui você precisa formatar os dados conforme necessário para CSV
                                // Você pode usar loops ou funções de formatação, dependendo da estrutura dos seus dados
                        
                                // Após formatar os dados, você pode criar um blob CSV e iniciará o download
                                var blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
                                if (navigator.msSaveBlob) { // IE 10+
                                    navigator.msSaveBlob(blob, 'data.csv');
                                } else {
                                    var link = document.createElement("a");
                                    if (link.download !== undefined) { // feature detection
                                        var url = URL.createObjectURL(blob);
                                        link.setAttribute("href", url);
                                        link.setAttribute("download", 'data.csv');
                                        link.style.visibility = 'hidden';
                                        document.body.appendChild(link);
                                        link.click();
                                        document.body.removeChild(link);
                                    }
                                }
                            },
                            error: function(xhr, status, error) {
                                console.error(xhr.responseText);
                            }
                        });
                    }
                }
            ]
        });  

        // Adiciona um evento de mudança para os checkboxes dentro da tabela
        // table.on('change', 'input[type="checkbox"]', function(){
        //     var checkbox = $(this);
        //     var row = checkbox.closest('tr');
        //     var data = table.row(row).data(); // Modificado para 'table.row(row).data()'
            
        //     // Verifica se o checkbox está marcado ou não e adiciona ou remove o ID da linha selecionada do array selectedIds
        //     if(checkbox.prop('checked')){
        //         selectedIds.push(data.forn_id);
        //     } else {
        //         var index = selectedIds.indexOf(data.forn_id);
        //         if(index !== -1){
        //             selectedIds.splice(index, 1);
        //         }
        //     }
        // });

        // begin first table
        // table.on('processing.dt', function (e, settings, processing) {
        //     if (processing) {
        //         Toast.fire({
        //             icon: 'success',
        //             title: 'Sucesso! Carregando os dados ...'
        //         });
        //     } else {
        //         Toast.close();
        //     }
        // });
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
        
        // Destrói a instância existente do DataTable, se houver
        if ($.fn.DataTable.isDataTable('#kt_ctt')) {
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
                url: '/fornecedor/ctt_list/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                    d.forn_id = $("#forn_id").val();
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
                    d.forn_id = $("#forn_id").val();
                },
            },
            order: [[ 0, 'asc' ]],
            columns: [
                {data: 'forn_aval_id'},
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
                        return moment(data).format("DD/MM/YYYY")
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

jQuery(document).ready(function() {
    tabela_forn.init()
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e){
        $($.fn.dataTable.tables(true)).DataTable()
           .columns.adjust();
     });

    pesq_impacto('#cat_imp')
    pesq_tipo('#cat_tip')
    pesq_cat_aval('#cat_aval')
    pesq_pessoa('#pes')

    $('#forn_cnpj').mask('00.000.000/0000-00', {reverse: true});
    $('#forn_ctt_tel').mask('(00) 00000-0000');

    $('#kt_forn').on('change', 'input.checkble:first', function() {
        var isChecked = $(this).prop('checked');
        // Marca ou desmarca todos os checkboxes nas linhas com base no estado do checkbox "selecionar tudo"
        $('#kt_forn tbody').find('input.checkble').prop('checked', isChecked);
    });
});

function abrir_modal_forn(){
    $('#forn_btn_salvar').val('insert');
    $('#aba_cont').hide();
    $('#aba_aval').hide();
    $('#frm_forn').trigger ('reset');
    $('#cat_imp').val('').trigger('change'); 
    $('#cat_tip').val('').trigger('change'); 
    $('#pes').val('').trigger('change'); 
    $('#forn_nome').val('');
    $('#forn_cnpj').val('');
    $('#forn_ies').val('');
    $('#frm_forn_modal').modal('show');
}

function abrir_modal_ctt(){
    $('#ctt_btn_salvar').val('insert');
    $('#frm_ctt').trigger ('reset');
    $('#forn_ctt_nome').val('');
    $('#forn_ctt_tel').val('');
    $('#forn_ctt_email').val('');
    $('#forn_ctt_ativo').prop('checked', false);
    $('#frm_ctt_modal').modal('show');
}

// function abrir_modal_aval(){
//     $('#aval_btn_salvar').val('insert');
//     $('#frm_aval').trigger ('reset');
//     $('#cat_aval').val('').trigger('change'); 
//     $('#pes').val('').trigger('change'); 
//     // $('#forn_ava_nome').val('');
//     // $('#forn_ctt_tel').val('');
//     // $('#forn_ctt_email').val('');
//     // $('#forn_ctt_ativo').prop('checked', false);
//     $('#frm_aval_modal').modal('show');
// }

function forn_add(){
    var url
    if($('#forn_btn_salvar').val() == 'update'){
        url = '/fornecedor/forn_edt/'
    }else{
        url = '/fornecedor/forn_add/'
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
    $.getJSON('/fornecedor/forn_atb/',
        {
            forn_id: forn_id
        }
    ).done(function (item) {
        $('#aba_cont').show();
        $('#aba_aval').show();
        $('#forn_id').val(item.forn_id);
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
        // KTDatatablesDataSourceProdutoArquivo.init();
        $('[href="#kt_tab_pane_1"]').tab('show');
        $('#frm_forn_modal').modal('show');
        tabela_ctt.init()
        tabela_aval.init()
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
                url: '/fornecedor/forn_del/',
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
        url = '/fornecedor/ctt_edt/'
    }else{
        url = '/fornecedor/ctt_add/'
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
    $.getJSON('/fornecedor/ctt_atb/',
        {
            forn_ctt_id: forn_ctt_id
        }
    ).done(function (item) {
        $('#forn_ctt_id').val(item.forn_ctt_id);
        $('#forn_ctt_nome').val(item.forn_ctt_nome);
        $('#forn_ctt_tel').val(item.forn_ctt_tel);
        $('#forn_ctt_email').val(item.forn_ctt_email);
        $('#forn_ctt_ativo').prop('checked', item.forn_ctt_ativo);
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
                url: '/fornecedor/ctt_del/',
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

// function gerarexcel() {
//     // Verifica se pelo menos um checkbox está selecionado
    
//     var checkedRows = $('#kt_forn tbody').find('input.checkble:checked').closest('tr'); // Encontra todas as linhas com checkboxes marcados
//     var selectedIds = [];
//     console.log(selectedIds)

//     // Itera sobre cada linha selecionada para extrair o ID
//     checkedRows.each(function() {
//         var rowId = $(this).find('td:last-child').text().trim(); // Captura o ID da última coluna e remove espaços em branco
//         console.log('ID da linha:', rowId);
//         selectedIds.push(rowId);
//     });

//     console.log('IDs selecionados:', selectedIds);

//     // Verifica se algum ID foi selecionado
//     if (selectedIds.length === 0) {
//         Swal.fire({
//             icon: 'warning',
//             title: 'Atenção!',
//             text: 'Por favor, selecione pelo menos um item.',
//             confirmButtonText: 'OK'
//         });
//         return;
//     }

//     // Chama a URL 'relatorio_aprov/' passando os IDs selecionados
//     $.ajax({
//         url: 'relatorio_aprov/',
//         type: 'POST',
//         data: {
//             selectedIds: selectedIds,
//             csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
//         },
//         success: function(response) {
//             // Se a chamada for bem-sucedida, você pode redirecionar o usuário para fazer o download do arquivo Excel
//             window.location.href = 'relatorio_aprov/';
//         },
//         error: function(xhr, status, error) {
//             // Em caso de erro, você pode lidar com isso aqui
//             console.error(xhr.responseText);
//         }
//     });
// }