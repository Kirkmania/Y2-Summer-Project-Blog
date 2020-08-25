// Credit to https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html for fantastic instructions on how to do this!
// Custom JS to perform AJAX to CRUD educations table for each user.

$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-education").modal("show");
        },
        success: function (data) {
          $("#modal-education .modal-content").html(data.html_form);
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
            $("#education-table tbody").html(data.html_education_list);
            $("#modal-education").modal("hide");
          }
          else {
            $("#modal-education .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };
  
  
    /* Binding */
  
    // Create education
    $(".js-create-education").click(loadForm);
    $("#modal-education").on("submit", ".js-education-create-form", saveForm);
  
    // Update education
    $("#education-table").on("click", ".js-edit-education", loadForm);
    $("#modal-education").on("submit", ".js-education-edit-form", saveForm);
  
    // Delete education
    $("#education-table").on("click", ".js-delete-education", loadForm);
    $("#modal-education").on("submit", ".js-education-delete-form", saveForm);
  });