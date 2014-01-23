function get_fullscreen_checkbox() {
  var fullscreen_checkbox = document.getElementById('fullscreen');
  return fullscreen_checkbox;
}

function get_url_textfield() {
  var url_textfield = document.getElementById('url');
  return url_textfield;
}

function toggle_fullscreen() {
  var url_textfield = get_url_textfield();
  var fullscreen_checkbox = get_fullscreen_checkbox();

  if (fullscreen_checkbox.checked)
    url_textfield.value = url_textfield.value + '/f';
  else
    url_textfield.value = url_textfield.value.slice(0, -2);
}

function update_fullscreen() {
  var url = get_url_textfield().value;
}

function setup_fullscreen_checkbox() {
  var fullscreen_checkbox = get_fullscreen_checkbox();
  fullscreen_checkbox.addEventListener('click', toggle_fullscreen);
}

function setup_url_textfield() {
  var url_textfield = document.getElementById('fullscreen');
  url_textfield.addEventListener('keyup', update_fullscreen);
}

window.addEventListener('load', function() {
  setup_fullscreen_checkbox();
  setup_url_textfield();
  toggle_fullscreen();
});
