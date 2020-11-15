var coverPage = document.getElementById('cover_page')

window.onload = (event) => {
  var newNode = document.createElement('input')
  var referenceNode = document.getElementById('div_id_publisher').childNodes[3];
  var parentNode = document.getElementById('div_id_publisher');

  newNode.setAttribute('id', 'id_publisher_placeholder');
  newNode.setAttribute('required', '');
  newNode.setAttribute('class','textinput textInput form-control');
  newNode.setAttribute('maxlength', '128');
  newNode.setAttribute('type', 'text');
  newNode.setAttribute('name', 'publisher_placeholder');

  parentNode.insertBefore(newNode, referenceNode);
  referenceNode.setAttribute('hidden', '');
  referenceNode.childNodes[1].value = 0;
  document.getElementById('id_publisher').options[1].setAttribute('selected', '');
  document.getElementById('id_publisher').options[0].removeAttribute('selected');
  document.getElementById('id_publisher').removeAttribute('required');
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

$("#id_publisher_placeholder").change(function() {
  document.getElementById('id_publisher').options[1].setAttribute('selected', '');
  document.getElementById('id_publisher').options[0].removeAttribute('selected');
});
