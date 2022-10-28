$("document").ready(function(){
    //Filter by Work Order
    $("#WOFilterButton").on('click', function(e){
        var wo_num = $("#wo_filter").val();
        var filter_out = JSON.stringify({"wo_num": wo_num, "status": 'Open', "manager": ""})
        $.ajax({
            url: "/orderFilter",
            type: "POST",
            contentType: "application/json",
            data: filter_out
        }).done(function(data) {
            liItem = `<li><span>Wo#: ` + wo_num + `</span>
                     <a id="removeFilter"><i class="fa fa-remove"></i></a></li>`
                      
            //Update Filter List
            $("#filterList").html(liItem);

            //Update Order Table
            $("#orderTable").html(data);

            $("#wo_filter").val("");
            
        });
    });

    //Filter by Status
    $("#status_filter").on('change', function(e){
        var status = $("#status_filter").val();
        var filter_out = JSON.stringify({"wo_num": "", "status": status, "manager": ""})
        $.ajax({
            url: "/orderFilter",
            type: "POST",
            contentType: "application/json",
            data: filter_out
        }).done(function(data) {
            liItem = `<li><span>Status: ` + status + `</span>
                     <a id="removeFilter"><i class="fa fa-remove"></i></a></li>`;
                      
            $("#filterList").html(liItem);

            $("#orderTable").html(data);
            $("#status_filter").val("");
            
        });
    });

    //Filter by Manager
    $("#manager_filter").on('change', function(e){
        var manager = $("#manager_filter").val();
        var filter_out = JSON.stringify({"wo_num": "", "status": "Open", "manager": manager})
        console.log(filter_out)
        $.ajax({
            url: "/orderFilter",
            type: "POST",
            contentType: "application/json",
            data: filter_out
        }).done(function(data) {
            liItem = `<li><span>Manager: ` + status + `</span>
                     <a id="removeFilter"><i class="fa fa-remove"></i></a></li>`;
                      
            $("#filterList").html(liItem);

            $("#orderTable").html(data);
            $("#manager_filter").val("");
            
        });
    });

    //Remove Filters
    $("#filterListDiv").on('click', '#removeFilter', function(e){
        console.log(e.target)
        var filter_out = JSON.stringify({"wo_num": "", "status": "Open", "manager": ""})
        $.ajax({
            url: "/orderFilter",
            type: "POST",
            contentType: "application/json",
            data: filter_out
        }).done(function(data) {
            liItem = `<li><span>Status: Open</span></li>`;
                      
            $("#filterList").html(liItem);

            $("#orderTable").html(data);

        e.preventDefault();
            
        });
    });

    //Change Status Switch
    $("#mainDiv").on('change', ".changeStatus", function(e){
        var wo_num = $(this).attr('wo_id');
        var status = $("#statusUpdate"+wo_num).val();
        var output = JSON.stringify({"wo_num": wo_num, "status": status});
        $.ajax({
            url: "/updateStatus",
            type: "POST",
            contentType: "application/json",
            data: output
        }).done(function(data) {

            $("#row"+wo_num).fadeOut(1000).fadeIn(1000);
        });
    });

    //Change Next Date Value
    $("#mainDiv").on('submit', ".changeDate", function(e){
        var wo_num = $(this).attr('wo_id');
        var date = $("#nextDateUpdate"+wo_num).val();
        var output = JSON.stringify({"wo_num": wo_num, "date": date});
            $.ajax({
            url: "/updateDate",
            type: "POST",
            contentType: "application/json",
            data: output
        }).done(function(data) {

            $("#row"+wo_num).fadeOut(1000).fadeIn(1000);
        });
        e.preventDefault();
    });
});