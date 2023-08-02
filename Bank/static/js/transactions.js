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
    

});
