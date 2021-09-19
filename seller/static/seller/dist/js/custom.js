var btnUpload = $("#upload_file"),
		btnOuter = $(".button_outer");
	btnUpload.on("change", function(e){
		var ext = btnUpload.val().split('.').pop().toLowerCase();
		if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1) {
			$(".error_msg").text("Not an Image...");
		} else {
			$(".error_msg").text("");
			btnOuter.addClass("file_uploading");
			setTimeout(function(){
				btnOuter.addClass("file_uploaded");
			},3000);
			var uploadedFile = URL.createObjectURL(e.target.files[0]);
			setTimeout(function(){
				$("#uploaded_view").append('<img src="'+uploadedFile+'" />').addClass("show");
			},3500);
		}
	});
	$(".file_remove").on("click", function(e){
		$("#uploaded_view").removeClass("show");
		$("#uploaded_view").find("img").remove();
		btnOuter.removeClass("file_uploading");
		btnOuter.removeClass("file_uploaded");
	});

function calculateprice(){
	var mrp=document.getElementById('mrp').value
	var discount=document.getElementById('discount').value
	document.getElementById('discountedprice').value=mrp*(100-discount)/100
}


function getLocation() {
	if (navigator.geolocation) {
	  navigator.geolocation.getCurrentPosition(showPosition);
	} else { 
		document.getElementById('longitude').value=0;
		document.getElementById('latitude').value=0;
	}
  }

  function showPosition(position) {
	document.getElementById('longitude').value=position.coords.longitude;
	document.getElementById('latitude').value=position.coords.latitude;
  }