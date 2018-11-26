/**
 * Created by DevMiau on 27-Oct-18.
 */
 $("#checkbox").change(function(){
            if(this.checked){
                $("#submit_button").prop("disabled", false);
            } else {
                $("#submit_button").prop("disabled", true);
            }
        });