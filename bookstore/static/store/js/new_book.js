var coverPage = document.getElementById('cover_page')

window.onload = (event) => {
  var labels = document.getElementsByTagName('LABEL');
  for (var i = 0; i < labels.length; i++) {
    if (labels[i].htmlFor != '') {
      var elem = document.getElementById(labels[i].htmlFor);
      if (elem)
        elem.label = labels[i];
    }
  }
  document.getElementById('id_featured').label.setAttribute('class', 'form-check-label ml-4')
}

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      coverPage.src = e.target.result;
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

$("#id_image").change(function() {
  readURL(this);
});
