// Credit to https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html for fantastic instructions on how to do this!
// Custom JS to perform AJAX to CRUD certifications table for each user.

$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-certification").modal("show");
        },
        success: function (data) {
          $("#modal-certification .modal-content").html(data.html_form);
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
            $("#certification-table tbody").html(data.html_certification_list);
            $("#modal-certification").modal("hide");
          }
          else {
            $("#modal-certification .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };
  
  
    /* Binding */
  
    // Create certification
    $(".js-create-certification").click(loadForm);
    $("#modal-certification").on("submit", ".js-certification-create-form", saveForm);
  
    // Update certification
    $("#certification-table").on("click", ".js-edit-certification", loadForm);
    $("#modal-certification").on("submit", ".js-certification-edit-form", saveForm);
  
    // Delete certification
    $("#certification-table").on("click", ".js-delete-certification", loadForm);
    $("#modal-certification").on("submit", ".js-certification-delete-form", saveForm);
  });