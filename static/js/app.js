$(document).ready(function() {
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
        $.fn.dataTable.tables({
            visible: true,
            api: true
        }).columns.adjust();
    });

    $('table.table').DataTable({
        searching: true,
        responsive: true,
        "autoWidth": true,
        "scrollCollapse": true,
        "scrollY": "350px",
        "scrollX": true,
        "order": [
            [0, "desc"]
        ]
    });

    // Apply a search to the second table for the demo
    $('#myTable2').DataTable().search('bdatHSD_007').draw();
});

$("#create-tweet").click(function() {
    $("#tweetModal").modal("show");
});
$("#create-reddit").click(function() {
    $("#redditModal").modal("show");
});
$('#closeTwitter').click(function() {
    $("#tweetModal").modal("hide");
});
$('#closeReddit').click(function() {
    $("#redditModal").modal("hide");
});


$(document).ready(function() {
    $("form#twitterForm").submit(function(event) {
        event.preventDefault();
        var text = $("#editor").val();
        $.ajax({
            type: "POST",
            contentType: "application/json;charset=UTF-8",
            url: "http://localhost:5000/tweet",
            data: JSON.stringify({
                'tweet': text
            }),
            dataType: "json",
            cache: false,
            success: function() {
                alert('success');
            }
        });
    });
    $("form#redditForm").submit(function(event) {
        event.preventDefault();
        var text = $("#editor1").val();
        $.ajax({
            type: "POST",
            contentType: "application/json;charset=UTF-8",
            url: "http://localhost:5000/reddit",
            data: JSON.stringify({
                'reddit': text
            }),
            dataType: "json",
            cache: false,
            success: function() {
                alert('success');
            }
        });
    });
});

jQuery(document).ready(function($) {
    $('#example').DataTable({
        searching: true,
        responsive: true,
        "autoWidth": true,
        "scrollCollapse": true,
        "scrollY": "440px",
        "scrollX": true,
    });
    var table = $('#myTable1').DataTable();
    $('#myTable1 tbody').on('click', 'tr', function() {
        //console.log(table.row(this).data());
        $(".modal-body div span").text("");
        $(".timeCreated span").text(table.row(this).data()[0]);
        $(".author span").text(table.row(this).data()[1]);
        $(".title span").text(table.row(this).data()[2]);
        $(".score span").text(table.row(this).data()[3]);
        $(".comments span").text(table.row(this).data()[4]);
        $(".post span").text(table.row(this).data()[5]);
        $(".link span").text(table.row(this).data()[6]);
        $("#myModal").modal("show");
    });

    var table1 = $('#myTable2').DataTable();
    $('#myTable2 tbody').on('click', 'tr', function() {
        //console.log(table.row(this).data());
        $(".modal-body div span").text("");
        $(".timeCreated span").text(table1.row(this).data()[0]);
        $(".author span").text(table1.row(this).data()[1]);
        $(".title span").text(table1.row(this).data()[2]);
        $(".score span").text(table1.row(this).data()[3]);
        $(".comments span").text(table1.row(this).data()[4]);
        $(".post span").text(table1.row(this).data()[5]);
        $(".link span").text(table1.row(this).data()[6]);
        $("#myModal2").modal("show");
    });
    $('#closemodal').click(function() {
        $("#myModal").modal("hide");
    });
    $('#closemodal2').click(function() {
        $("#myModal2").modal("hide");
    });
});