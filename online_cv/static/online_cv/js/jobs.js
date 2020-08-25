// Credit to https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html for fantastic instructions on how to do this!
// Custom JS to perform AJAX to CRUD jobs table for each user.

$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-job").modal("show");
        },
        success: function (data) {
          $("#modal-job .modal-content").html(data.html_form);
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
            $("#job-table tbody").html(data.html_job_list);
            $("#modal-job").modal("hide");
          }
          else {
            $("#modal-job .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };
  
  
    /* Binding */
  
    // Create job
    $(".js-create-job").click(loadForm);
    $("#modal-job").on("submit", ".js-job-create-form", saveForm);
  
    // Update job
    $("#job-table").on("click", ".js-edit-job", loadForm);
    $("#modal-job").on("submit", ".js-job-edit-form", saveForm);
  
    // Delete job
    $("#job-table").on("click", ".js-delete-job", loadForm);
    $("#modal-job").on("submit", ".js-job-delete-form", saveForm);
  });