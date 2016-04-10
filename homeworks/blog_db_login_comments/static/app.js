/**
 *
 * Created by user on 08.04.16.
 */
'use strict';

(function (window, document, $) {

    var PrepareComments = function (data) {
        var comments = "";
        for (var key in data) {
            var item = data[key];
            comments += '<p class="blog-post-meta">added at ' +
                item['datetime'] + '</p>' +
                item['content'];
        }
        return comments;
    };

    var ShowComments = function () {
        var article_id = $(this).parent('div.blog-post').attr('value');
        $.ajax({
            context: this,
            type: "GET",
            url: "http://127.0.0.1:5000/ajax/" + article_id,
            dataType: "json",
            success: function (response) {
                $(this).siblings('div.comments').empty();
                $(this).siblings('div.comments').append(PrepareComments(response));
            }
        });
        $(this).siblings('.new_comment').show();
    };

    var SendComment = function () {
        var article_id = $(this).parent().parent('div.blog-post').attr('value');
        console.log(article_id);
        var content = $(this).siblings('input:text');
        var content_json = JSON.stringify({'content': content.val()});
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/ajax/" + article_id,
            data: content_json,
            processData: false,
            contentType: 'application/json'
        });
        content.val("");
        var context = $(this).parent().siblings('button.comments');
        ShowComments.call(context);
    };


    $(document).ready(function () {
        $('button.comments').click(function () {
            ShowComments.call(this);
        });
        $('button.add_comment').click(function () {
            SendComment.call(this);
        });
    });
})(window, document, jQuery);