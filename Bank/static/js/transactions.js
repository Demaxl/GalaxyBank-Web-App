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

        document.getElementById("pin").focus();
        $(".transact-submit-btn").text(`${action} $${amount.val()}`)
    });

    $("#receiver").on("input", function () {
        const val = this.value
        const apiURL = $(this).data("api-url")
        if (val.length < 3) return;

       
        $.get(apiURL, `user=${val}`, function (data, textStatus, jqXHR) {
                $(".suggested-receivers a").remove();
                
                if (Object.keys(data).length == 0) {
                    $(".suggested-receivers").append(`<a href="#" class="list-group-item list-group-item-action disabled" aria-current="true">
                                                        <div class="d-flex w-100 justify-content-start">
                                                            No matching results..  
                                                        </div>
                                                    </a>  `)
                }
                for (const user in data) {
                    $(".suggested-receivers").append(`<a href="#" class="list-group-item list-group-item-action" aria-current="true">
                                                        <div class="d-flex w-100 justify-content-start">
                                                            <img src="${data[user][1]}" alt="user image" width="45" height="45" class="rounded-circle">
                                                            <button type="button" class="btn">${ data[user][0] } (${ user })</button>    
                                                        </div>
                                                    </a>  `)
                }
            },
        );
    });
});
