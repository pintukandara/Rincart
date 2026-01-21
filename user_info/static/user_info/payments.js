document.addEventListener("DOMContentLoaded", function () {
    const payBtn = document.getElementById("rzp-button1");

    if (!payBtn) return; // If button not found, exit

    const cfg = window.razorpayConfig;

    const options = {
        key: cfg.key,
        amount: cfg.amount,
        currency: "INR",
        name: "RinCart",
        description: "Test Transaction",
        image: "https://example.com/your_logo",
        order_id: cfg.order_id,
        callback_url: cfg.callback_url,
        prefill: {
            name: cfg.user,
            email: "pintukandara124@gmail.com",
            contact: "9815937658",
        },
        notes: {
            address: "Razorpay Corporate Office",
        },
        theme: {
            color: "#3399cc",
        },
    };

    const rzp1 = new Razorpay(options);

    payBtn.addEventListener("click", function (e) {
        e.preventDefault(); // ✅ stop any accidental form submit
        console.log("Opening Razorpay Checkout...");
        rzp1.open();
    });
});
