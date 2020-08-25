// Credit to https://simpleisbetterthancomplex.com/tutorial/2016/11/15/how-to-implement-a-crud-using-ajax-and-json.html for fantastic instructions on how to do this!
// Custom JS to perform AJAX to CRUD skills table for each user.

$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-skill").modal("show");
        },
        success: function (data) {
          $("#modal-skill .modal-content").html(data.html_form);
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
            $("#skill-table tbody").html(data.html_skill_list);
            $("#modal-skill").modal("hide");
          }
          else {
            $("#modal-skill .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };
  
  
    /* Binding */
  
    // Create skill
    $(".js-create-skill").click(loadForm);
    $("#modal-skill").on("submit", ".js-skill-create-form", saveForm);
  
    // Update skill
    $("#skill-table").on("click", ".js-edit-skill", loadForm);
    $("#modal-skill").on("submit", ".js-skill-edit-form", saveForm);
  
    // Delete skill
    $("#skill-table").on("click", ".js-delete-skill", loadForm);
    $("#modal-skill").on("submit", ".js-skill-delete-form", saveForm);
  });