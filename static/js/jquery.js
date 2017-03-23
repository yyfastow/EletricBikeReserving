/**
 * Created by yosef on 2/28/2017.
 */

$(document).ready(function() {
   
    $(".dropdownform-button").click(function() {
        $Form = $(this).siblings(".dropdownform");
        if ($Form.css("display") == "none") {
            $Form.show();
        } else {
            $Form.hide();
        }
    });

     $(".add-address-button").click(function() {
        $Form = $(".add-address-form");
        if ($Form.css("display") == "none") {
            $Form.show();
        } else {
            $Form.hide();
        }
    });

    $(".add-card-button").click(function() {
        $Form = $(".add-card-form");
        if ($Form.css("display") == "none") {
            $Form.show();
        } else {
            $Form.hide();
        }
    });
    
});
