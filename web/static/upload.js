var LoadFile = function (event,out_id) {
            var reader = new FileReader();
            reader.onload = function () {
                var output = document.getElementById('output_'+out_id);
                output.src = reader.result;
            };
            reader.readAsDataURL(event.target.files[0]);
        };