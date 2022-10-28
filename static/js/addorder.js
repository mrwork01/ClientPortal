$("document").ready(function(){
	$("#companySelect").on('change', function(e){
		var company = $("#companySelect").val();
		data = JSON.stringify({"company": company});
		$.ajax({
			url: "/dynDrop",
			type: "POST",
			contentType: "application/json",
			data: data
		}).done(function(data) {

			$("#managerSelect").empty();

			$.each(data, function(i,v){
				$("#managerSelect").append(new Option(v,v));
				console.log(v);

			});
		});
	});
})