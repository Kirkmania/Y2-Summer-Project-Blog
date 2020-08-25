// Credit to https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html for fantastic instructions on how to do this!
// Custom JS to perform AJAX to CRUD languages table for each user.

$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-language").modal("show");
      },
      success: function (data) {
        $("#modal-language .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#language-table tbody").html(data.html_language_list);
          $("#modal-language").modal("hide");
        }
        else {
          $("#modal-language .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create language
  $(".js-create-language").click(loadForm);
  $("#modal-language").on("submit", ".js-language-create-form", saveForm);

  // Update language
  $("#language-table").on("click", ".js-edit-language", loadForm);
  $("#modal-language").on("submit", ".js-language-edit-form", saveForm);

  // Delete language
  $("#language-table").on("click", ".js-delete-language", loadForm);
  $("#modal-language").on("submit", ".js-language-delete-form", saveForm);
});