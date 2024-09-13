//$(document).ready(function() {
//    function updateEmptyFormIDs(element,totalForms){
//    var thisInput = element
//    //get current form input name
//    var currentName = element.attr('name');
//
//    // replace prefix with actual number
//    var newName = currentName.replace(/__prefix__/g, totalForms)
//    thisInput.attr('name', newName)
//    thisInput.attr('id', "id_" + newName)
//
//    // creat new form  row id
//    var newFormRow = element.closest(".new-form-row");
//    var newRowID = "row_id_" + newName;
//    newFormRow.attr("id", newRowID);
//
//    //create form-froup id
//    var newFormGroup = element.closest(".form-group");
//    var newFormGroupID = "div_id_" + newName;
//    newFormGroup.attr("id", newFormGroupID);
//
//    //create new dropzone id
//    var newDropzone = element.closest(".dropzone");
//    var newDropzoneID = "custom-dropzone-widget-" + newName;
//    newDropzone.attr("id", newDropzoneID);
//
//    //create new peti id
//    var newPeti = element.closest(".dropzone").find('.peti');
//    var newPetiID = "preview_" + newName;
//    newPeti.attr("id", newPetiID);
//
//    // add clas fopr newbasic animations
//    newFormRow.addClass("new-parent-row");
//
//    // update form group id
//    var parentDiv = element.parent();
//    parentDiv.attr("id", "parent_id_" + newName)
//
//    // update label id
//    var inputLabel  = parentDiv.find("label")
//    inputLabel.attr("for", "id_"  + newName)
//
//    return newFormRow
//
//};
$('#education-link').addClass('active');

// add date-field
var formId = "id_form-TOTAL_FORMS";
var totalForms = parseInt($('#' + formId).val());
for( i=0; i < totalForms; i++){
    $( "#id_form-" + i + "-certificate_date").datepicker({
      changeYear: true,
      dateFormat: "dd/mm/yy",
    }).attr("placeholder", "dd/mm/yyyy");
}
$(document).ready(function() {
    function updateEmptyFormIDs(element,totalForms){
    var thisInput = element
    //get current form input name
    var currentName = element.attr('name')


    // replace prefix with actual number
    var newName = currentName.replace(/__prefix__/g, totalForms)
    thisInput.attr('name', newName)
    thisInput.attr('id', "id_" + newName)

    // create new form  row id
    var newFormRow = element.closest(".new-form-row");
    var newRowID = "row_id_" + newName;
    newFormRow.attr("id", newRowID);

    // add class for new basic animations
    newFormRow.addClass("new-parent-row");

    // update form group id
    var parentDiv = element.parent();
    parentDiv.attr("id", "parent_id_" + newName)

    // update label id
    var inputLabel  = parentDiv.find("label")
    inputLabel.attr("for", "id_"  + newName)

    return newFormRow

    };

    $('.add-new-form').click(function(e) {
    e.preventDefault()

    var formId = "id_form-TOTAL_FORMS";
    var totalForms = parseInt($('#' + formId).val());
    $('#form-head').html('Training Certificate-' + (totalForms + 1));

    var emptyRow = $("#empty-row").clone();

    //remove id from new form
    emptyRow.attr("id", null)

    if (totalForms<=2){
        var newFormRow;
        emptyRow.find("input, select, textarea").each(function() {
            newFormRow = updateEmptyFormIDs($(this), totalForms)
        })
        emptyRow.html(emptyRow.html().replace(/__prefix__/g,totalForms));

        $(".new-form-row:last").after(newFormRow);

        $('#' + 'id_form-TOTAL_FORMS').val(totalForms + 1);
        }else{
            $('.add-new-form').addClass('disabled')
        }
        $( "#id_form-" + totalForms + "-certificate_date").datepicker({
          changeYear: true,
          dateFormat: "dd/mm/yy",
        }).attr("placeholder", "dd/mm/yyyy");

    })
})

//    $('.add-new-form').click(function(e) {
//        e.preventDefault()
//        var formId = "id_form-TOTAL_FORMS";
//        var totalForms = parseInt($('#' + formId).val());
//        var currentXName = $('#empty-row').find('.drop_script_class').attr('id');
//        var currentWidgetname = $('#empty-row').find('.drop_script_class').attr('data-widgetname');
//        var newXName = currentXName.replace(/__prefix__/g, totalForms)
//        var newWidgetName = currentWidgetname.replace(/__prefix__/g, totalForms)
//
//        var dropscript = `
//            <script class="">
//                document.getElementById('`+ newXName +`').addEventListener('change', function(){
//                let fileReference = document.getElementById('`+ newXName +`').files && document.getElementById('`+ newXName +`').files[0];
//
//                if(fileReference){
//                    var reader = new FileReader();
//                    reader.onload = (event) => {
//                    document.getElementById('preview_`+ newWidgetName +`').src = event.target.result;
//                    document.getElementById('preview_`+ newWidgetName +`').innerHTML = '<div><i class="mdi mdi-file-document-outline menu-icon"></i><br><p>'+ fileReference.name +'</p></div>';
//                    }
//                    reader.readAsDataURL(fileReference);
//                }
//                })
//            </script>
//        `
//
//        var emptyRow = $("#empty-row").clone();
//        emptyRow.find(".drop_script_class").html(dropscript);
//
//        emptyRow.attr("id", null);
//
//        var newFormRow;
//
//        emptyRow.find("input, select, textarea").each(function() {
//            newFormRow = updateEmptyFormIDs($(this), totalForms)
//        })
//        newFormRow.closest('.drop_script_class').remove();
//        $(".new-form-row:last").after(newFormRow);
//
//        $('#' + 'id_form-TOTAL_FORMS').val(totalForms + 1);
//        $('#parent_id_form-'+ (totalForms) +'-id').find('#form-head').text('Document-' + (totalForms + 1));
//    })