const stripe = Stripe("pk_live_51NOPgRK9OtnDAoGtR0b7h81IaiQSmPnu0F55GAR7AWmfdvX7dO5pkpayJWCRLNDmSH4gjhInQ3AvlKyzTpSAOywJ00mxXzFwnY");

function gaga_payment_init() {
    document.querySelector("#payment-form").addEventListener("submit", handleSubmit);
    const btns = document.querySelectorAll(".payment-btn");
    btns.forEach(btn => {
        btn.addEventListener("click", e => {
            create_order(e);
        });
    });
}

function async_fetch(e) {
    const request_data = new FormData();
    const prod_id = e.target.getAttribute("value");
    request_data.append('prod_id', prod_id);
    fetch("/create_order/", {
        method: "POST",
        body: request_data,
    })
        .then(response => response.json())
        .then((response) => {
            location.href = response.url;
            // window.open(response.url, '_blank').focus();
        });
}

async function create_order(e) {
    const prod_id = e.target.getAttribute("value");
    const request_data = new FormData();
    request_data.append('prod_id', prod_id);

    const response = await fetch("/gaga_intent/", {
        method: "POST",
        body: request_data,
    });

    const { clientSecret, price, } = await response.json();
    const appearance = {
        theme: 'stripe',
    };
    const paymentElementOptions = {
        layout: "tabs",
    };
    elements = stripe.elements({ appearance, clientSecret });
    const paymentElement = elements.create("payment", paymentElementOptions);
    paymentElement.mount("#payment-element");

    const myModal = new bootstrap.Modal('#gagaModal', {});
    myModal.show();
}

async function handleSubmit(e) {
    e.preventDefault();
    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            // Make sure to change this to your payment completion page
            return_url: "https://www.asuperdomain.com/pay_success/",
            receipt_email: 'mzhu@classgaga.com',
        },
    });

    // This point will only be reached if there is an immediate error when
    // confirming the payment. Otherwise, your customer will be redirected to
    // your `return_url`. For some payment methods like iDEAL, your customer will
    // be redirected to an intermediate site first to authorize the payment, then
    // redirected to the `return_url`.
    if (error.type === "card_error" || error.type === "validation_error") {
        showMessage(error.message);
    } else {
        showMessage("An unexpected error occurred.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    gaga_payment_init();
});