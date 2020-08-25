// Credit to https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html for fantastic instructions on how to do this!
// Custom JS to perform AJAX to CRUD interests table for each user.

$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-interest").modal("show");
        },
        success: function (data) {
          $("#modal-interest .modal-content").html(data.html_form);
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
            $("#interest-table tbody").html(data.html_interest_list);
            $("#modal-interest").modal("hide");
          }
          else {
            $("#modal-interest .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };
  
  
    /* Binding */
  
    // Create interest
    $(".js-create-interest").click(loadForm);
    $("#modal-interest").on("submit", ".js-interest-create-form", saveForm);
  
    // Update interest
    $("#interest-table").on("click", ".js-edit-interest", loadForm);
    $("#modal-interest").on("submit", ".js-interest-edit-form", saveForm);
  
    // Delete interest
    $("#interest-table").on("click", ".js-delete-interest", loadForm);
    $("#modal-interest").on("submit", ".js-interest-delete-form", saveForm);
  });