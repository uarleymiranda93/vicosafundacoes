function pesq_impacto(field){
    $(field).select2({
        width: "100%",
        allowClear: true,
        placeholder: "Pesquise aqui...",
        language: {
            "noResults": function(){
                return "Nenhum resultado encontrado";
            }
        },
        escapeMarkup: function (markup) {
            return markup;
        },
        ajax: {
            url: '/categorias/pesq_impacto/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                var query = {
                    term: params.term,
                }
                return query;
            },
            processResults: function (data) {
                return {
                    results: $.map(data, function (item) {
                        return {
                            text: item.cat_imp_nome,
                            id: item.cat_imp_id,
                            value: item.cat_imp_id,
                            value : item.cat_imp_cor,
                        }
                    })
                };
            },
            transport: function (params, success, failure) {
                var $request = $.ajax(params);
                $request.then(success);
                $request.fail(failure);
                return $request;
            }
        }
    });
}


function pesq_status(field){
    $(field).select2({
        width: "100%",
        allowClear: true,
        placeholder: "Pesquise aqui...",
        language: {
            "noResults": function(){
                return "Nenhum resultado encontrado";
            }
        },
        escapeMarkup: function (markup) {
            return markup;
        },
        ajax: {
            url: '/categorias/pesq_status/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                var query = {
                    term: params.term,
                }
                return query;
            },
            processResults: function (data) {
                return {
                    results: $.map(data, function (item) {
                        return {
                            text: item.cat_sta_nome,
                            id: item.cat_sta_id,
                            value: item.cat_sta_id,
                            value : item.cat_sta_cor,
                        }
                    })
                };
            },
            transport: function (params, success, failure) {
                var $request = $.ajax(params);
                $request.then(success);
                $request.fail(failure);
                return $request;
            }
        }
    });
}


function pesq_tipo(field){
    $(field).select2({
        width: "100%",
        allowClear: true,
        placeholder: "Pesquise aqui...",
        language: {
            "noResults": function(){
                return "Nenhum resultado encontrado";
            }
        },
        escapeMarkup: function (markup) {
            return markup;
        },
        ajax: {
            url: '/categorias/pesq_tipo/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                var query = {
                    term: params.term,
                }
                return query;
            },
            processResults: function (data) {
                return {
                    results: $.map(data, function (item) {
                        return {
                            text: item.cat_tip_nome,
                            id: item.cat_tip_id,
                            value: item.cat_tip_id,
                            value : item.cat_tip_cor,
                        }
                    })
                };
            },
            transport: function (params, success, failure) {
                var $request = $.ajax(params);
                $request.then(success);
                $request.fail(failure);
                return $request;
            }
        }
    });
}


function pesq_produto(field){
    $(field).select2({
        width: "100%",
        allowClear: true,
        placeholder: "Pesquise aqui...",
        language: {
            "noResults": function(){
                return "Nenhum resultado encontrado";
            }
        },
        escapeMarkup: function (markup) {
            return markup;
        },
        ajax: {
            url: '/categorias/pesq_produto/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                var query = {
                    term: params.term,
                }
                return query;
            },
            processResults: function (data) {
                return {
                    results: $.map(data, function (item) {
                        return {
                            text: item.cat_prod_nome,
                            id: item.cat_prod_id,
                            value: item.cat_prod_id,
                            value : item.cat_prod_cor,
                        }
                    })
                };
            },
            transport: function (params, success, failure) {
                var $request = $.ajax(params);
                $request.then(success);
                $request.fail(failure);
                return $request;
            }
        }
    });
}