$(function () {
    const amount = $("#amount");
    $("#amount").change(function () {
        if (Number(amount.val()) < 10) {
            this.value = "10"
        }
    });


    $(".transact-btn").click(function (e) {
        e.preventDefault();
        
        const action = this.dataset.action;

        if (action == "Transfer") {
            if (!$("#receiver").hasClass("is-valid")) {
                $("#receiver").addClass("is-invalid");
                return
            }
        }

        document.getElementById("pin").focus();
        $(".transact-submit-btn").text(`${action} $${amount.val()}`)

        $("#trigger-pin-modal").click();
        $("#pin").focus()
    });

    

    $("#receiver").on("input change", function () {
        const val = this.value;
        const apiURL = $(this).data("api-url");
        const requestUser = $(this).data("requestUser");
        // if (val.length < 2) return;

        $("#receiver").removeClass("is-valid")

       
        $.get(apiURL, `user=${val}&requestUser=${requestUser}`, function (data, textStatus, jqXHR) {
                $(".suggested-receivers a").remove();
                
                if (Object.keys(data).length == 0) {
                    $(".suggested-receivers").append(`<a href="#" class="list-group-item list-group-item-action disabled" aria-current="true">
                                                        <div class="d-flex w-100 justify-content-start">
                                                            No matching results..  
                                                        </div>
                                                    </a>`);
                    $("#receiver").addClass("is-invalid");
                    $("#receiver").removeClass("is-valid");

                    
                }
                for (const user in data) {
                    $(".suggested-receivers").append(`<a href="javascript:void(0)" class="list-group-item list-group-item-action suggested-user-btn" data-user=${user} aria-current="true">
                                                        <div class="d-flex w-100 justify-content-start">
                                                            <img src="${data[user][1]}" alt="user image" width="45" height="45" class="rounded-circle">
                                                            <button type="button" class="btn">${ data[user][0] } (${ user })</button>    
                                                        </div>
                                                    </a>  `)
                };
                $(".suggested-user-btn").click(function (e) {
                    $("#receiver").val($(this).data("user"));
                    $(".suggested-receivers a").remove();
                    $("#receiver").addClass("is-valid");
                    $("#receiver").removeClass("is-invalid");
                
                })
            },
        );
    });

});
