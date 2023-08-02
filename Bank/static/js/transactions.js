$(function () {
    const amount = $("#amount");

    $("#amount").change(function () {
        if (Number(amount.val()) < 10) {
            this.value = "10"
        }
    });


    $("#deposit-btn").click(function (e) {
        e.preventDefault();
        
        document.getElementById("pin").focus()
        $("#deposit-submit-btn").text(`Deposit $${amount.val()}`)
    });
    

});
