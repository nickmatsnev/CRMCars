function showFile(e) {
    var files = e.target.files;
    for (var i = 0, f; f = files[i]; i++) {
      if (!f.type.match('image.*')) continue;
      var fr = new FileReader();
      fr.onload = (function(theFile) {
        return function(e) {
          var li = document.createElement('li');
          li.innerHTML = "<img width='" + 250 +"' src='" + e.target.result + "' />";
          document.getElementById('list').insertBefore(li, null);
        };
      })(f);
 
      fr.readAsDataURL(f);
    }
  }
 
  document.getElementById('files').addEventListener('change', showFile, false);