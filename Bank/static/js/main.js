function message(text, type) {
    $("main").prepend( 
        `<div class="alert alert-${type} alert-dismissible fade show">
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            ${text}
        </div>`)
};


$(function () {
    $(".transaction-list li, .transaction-amount-div").each(function (index, element) {
        // element == this
        const amount = $(this).find(".transaction-amount");
        const type = $(this).find(".transaction-type").data("alert");

        amount.text(function (i, original) {
            return `${(type == "Credit") ? "+":"-"}${original}`
        })
        
        amount.addClass(`text-${ (type == "Credit") ? "success":"danger" }`);
    });
    


    $("#old-pin, #new-pin, #confirm-new-pin #pin").on("input", function () {
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
                   message("Payment PIN changed successfully!", "success");
                
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
    

    $(".profile-image").change(function (e) { 
        var file = this.files[0];

        if (!file.type.startsWith("image")) {
            return
        }

        const img = document.createElement("img");
        img.classList.add("card-img-top", "rounded-circle");
        img.style = "width:250px";
        img.alt = "Profile Image";

        img.src = URL.createObjectURL(file)

        $(".image-container img").remove()

        $(".image-container").prepend(img)
        
    });
    
    $(".image-container").click(function () {
        this.getElementsByClassName("profile-image")[0].click()
        
    })

    $("#create-profile-form").submit(function (e) { 
        const newPin = $(this).find("#new-pin").val();
        const confirmPin = $(this).find("#confirm-new-pin").val();
        const submitBtn = $(this).find("button")
        var invalid = false;

        

        if (newPin !== confirmPin) {
            $(this).find("#confirm-new-pin").addClass("is-invalid");
            invalid = true;
        } else {
            $(this).find("#confirm-new-pin").removeClass("is-invalid");
        }

        if (!invalid) {

            submitBtn.html(`<span class="spinner-border spinner-border-lg"></span>`).attr("disabled", true);
           
            // submitBtn.html("Create Profile");
            // submitBtn.attr("disabled", false);
        } else {
            return false;
        }
        
    });

});