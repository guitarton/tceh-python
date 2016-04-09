/**
 *
 * Created by user on 08.04.16.
 */

(function (window, document, $) {

    var AjaxGet = function (id) {
        var resp = $.ajax({
            type: "GET",
            url: "http://127.0.0.1:5000/ajax/" + id,
            dataType: "json"
        });
        return resp;
    };

    var AjaxPost = function (id, data) {
        var resp = $.ajax({
            type: 'POST',
            url: "http://127.0.0.1:5000/ajax/" + id,
            data: data,
            dataType: "json"
        });
    };


    //Events:
    $('button.comments').click(function () {
        var article_id = $(this).attr('value');
        //var req = AjaxGet(article_id);
        var id = article_id;
        var req = $.ajax({url: "http://127.0.0.1:5000/ajax/" + 2});
        console.dir(req);
        console.dir(req.readyState);
        console.dir(req.status);


    });


})
(window, document, jQuery);