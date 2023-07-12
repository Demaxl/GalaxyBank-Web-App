$(function () {
    $("#old-pin, #new-pin, #confirm-new-pin").on("input", function () {
        this.value = this.value.replace(/[^0-9]/g, ''); 
    });

    $("#changePinForm").submit(function (e) {
        e.preventDefault();
        const oldPin = $("#old-pin").val();
        const newPin = $("#new-pin").val();
        const confirmPin = $("#confirm-new-pin").val();
        const changePinBtn = $("#change-pin-btn");
        var invalid = false;

        

        if (newPin !== confirmPin) {
            $("#confirm-new-pin").addClass("is-invalid");
            invalid = true;
        } else {
            $("#confirm-new-pin").removeClass("is-invalid");
        }

        if (newPin === oldPin) {
            $("#new-pin").addClass("is-invalid");
            invalid = true;
        } else {
            $("#new-pin").removeClass("is-invalid");
        }

        if (!invalid) {
            $("#old-pin").removeClass("is-invalid");

            changePinBtn.html(`<span class="spinner-border spinner-border-lg"></span>`).attr("disabled", true);

            const data = {
                oldPin: oldPin,
                newPin: newPin,
            }

            $.ajax({
                type: "put",
                url: $(this).data("api-url"),
                headers: { "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val()},
                data: JSON.stringify(data),

                success: function (response, status, xhr) {
                   $("#pin-modal-cancel-btn").click();
                   $("main").prepend( 
                    `<div class="alert alert-success alert-dismissible fade show">
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        Payment PIN change successful!</div>
                    `
                    )
                
                },

                error: function (xhr, status, error) {
                    var data = xhr.responseJSON;
                    $("#old-pin + div.invalid-feedback").text(data.error);
                    $("#old-pin").addClass("is-invalid");
                }
            });

            changePinBtn.html("Change PIN");
            changePinBtn.attr("disabled", false);
        }
        

    });
    
   




});