const stripe = Stripe("pk_live_51NOPgRK9OtnDAoGtR0b7h81IaiQSmPnu0F55GAR7AWmfdvX7dO5pkpayJWCRLNDmSH4gjhInQ3AvlKyzTpSAOywJ00mxXzFwnY");

function gaga_payment_init() {
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
}

document.addEventListener("DOMContentLoaded", () => {
    gaga_payment_init();
});